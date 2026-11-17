const {chromium}=require('/opt/codex/cua_node/lib/node_modules/playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const out='/workspace/tooling/carrier-timing-review/browser';
function initialize(config={}) {
  const b=window.board={writes:[],enabled:false,pending:false,mode:'VSBONLY',emitTiming:config.emitTiming!==false,
    timingAck:true,timingReadback:true,delay:0,c:{state:0,kind:0,slot:0,duty:0,nlduty:25,preduty:10,offset:0.1,line_ref:325},
    settings:{VSET:28,VON:28,VMAX:32,OVP:36,DMAX:100,OD:10,FEN:10000,LOAD1:50,LOAD2:5,LOAD3:2.5,ACTLOAD:1,NLDUTY:25,AUTOMAX:100,AUTOSTEP:2,AUTOFINE:0.5,AUTOSETTLE:160,AUTOMEAS:100,PREMS:3,PRESETTLE:80,PREMAX:4}};
  const quant=(hz,ns,revision=0)=>{const timer_hz=100000000,period_ticks=2*Math.floor((timer_hz+hz)/(2*hz)),dead_ticks=Math.ceil(ns*timer_hz/1e9);return{requested_hz:hz,actual_hz:Math.floor((timer_hz+period_ticks/2)/period_ticks),requested_dead_ns:ns,actual_dead_ns:Math.ceil(dead_ticks*1e9/timer_hz),timer_hz,period_ticks,dead_ticks,min_hz:500000,max_hz:2000000,min_dead_ns:20,max_dead_ns:200,revision,enabled:b.enabled,busy:[1,2].includes(b.c.state)}};
  b.t=quant(1000000,40);
  let controller,timer,doneTimer;const enc=new TextEncoder();
  const send=x=>{try{controller.enqueue(enc.encode(JSON.stringify(x)+'\n'))}catch{}};
  const timing=(id='')=>{if(b.emitTiming)send({type:'timing',protocol:1,id,timing:{...b.t,enabled:b.enabled,busy:[1,2].includes(b.c.state)}})};
  const sample=()=>send({type:'telemetry',protocol:1,ms:Date.now()%10000000,enabled:b.enabled,mode:b.mode,fault:'NONE',feedback_valid:true,vpri:325,vsec:b.enabled?28:0,current:0,power:0,duty:b.enabled?15:0,adc:[1,2,3],settings:{...b.settings},lease_ms:5000,stream_ms:500,settings_pending:b.pending,calibration:{...b.c}});
  b.send=send;b.sample=sample;b.timing=timing;
  const port={readable:new ReadableStream({start(c){controller=c},cancel(){clearInterval(timer);clearTimeout(doneTimer)}}),
    writable:new WritableStream({write(data){const text=new TextDecoder().decode(data).trim();b.writes.push(text);
      if(text==='WEB HELLO'){send({type:'hello',protocol:1,fw:config.fw||'PWR-2.0.4',board:config.board||'V2 / STM32F410 · browser fixture',capabilities:config.capabilities||['bench_settings_v1','calibration_v1','carrier_timing_v1']});return}
      const match=text.match(/^WEB (\d+) (.*)$/);if(!match)return;const[,id,cmd]=match;
      const finish=()=>{if(cmd.startsWith('STREAM')){clearInterval(timer);if(cmd!=='STREAM 0')timer=setInterval(()=>{sample();timing()},150)}
        if(cmd==='ON')b.enabled=true;
        if(cmd==='OFF'){clearTimeout(doneTimer);b.enabled=false;if([1,2].includes(b.c.state))b.c.state=4}
        if(cmd.startsWith('MODE '))b.mode=cmd.slice(5);
        if(['OPEN','VSBONLY','LINEFF'].includes(cmd))b.mode=cmd;
        if(cmd.startsWith('LOAD '))b.settings.ACTLOAD=Number(cmd.slice(5));
        if(cmd.startsWith('SET ')){const[,key,value]=cmd.split(' ');b.settings[key]=Number(value);b.pending=true}
        if(cmd.startsWith('CAL ')){b.c.state=2;b.c.kind=2;b.c.slot=cmd.endsWith('2')?2:0;b.enabled=true;b.c.duty=15;clearTimeout(doneTimer);doneTimer=setTimeout(()=>{b.c.state=3;b.enabled=false;b.pending=true;b.c.nlduty=28.5;sample();timing()},1000)}
        if(cmd==='SAVE')b.pending=false;
        if(cmd.startsWith('TIMING ')){const[,hz,ns]=cmd.split(' ');b.t=quant(Number(hz),Number(ns),b.t.revision+1);b.pending=true;if(b.timingReadback)timing(id)}
        if(!cmd.startsWith('TIMING ')||b.timingAck)send({type:'ack',id,protocol:1,ok:true,code:cmd.startsWith('CAL ')?'calibration_queued':'OK'});
        sample();if(!cmd.startsWith('TIMING '))timing();
      };
      if(b.delay && cmd!=='OFF' && cmd!=='PING')setTimeout(finish,b.delay);else finish();
    }}),open:async()=>{},close:async()=>{clearInterval(timer);clearTimeout(doneTimer)}};
  Object.defineProperty(navigator,'serial',{value:{requestPort:async()=>port},configurable:true});
}
async function launch(){return chromium.launch({executablePath:'/usr/bin/chromium',args:['--no-sandbox']})}
async function page(browser,config={}){const p=await browser.newPage({viewport:{width:1440,height:1000},acceptDownloads:true});p.errors=[];p.resourceNotes=[];p.on('pageerror',e=>p.errors.push(e.message));p.on('console',m=>{if(m.type()==='error'){const entry=m.text()+' '+m.location().url;if(m.location().url.endsWith('/favicon.ico'))p.resourceNotes.push(entry);else p.errors.push(entry)}});await p.addInitScript(initialize,config);await p.goto('http://127.0.0.1:4173/');await p.evaluate(()=>document.fonts.ready);return p}
async function connect(p){await p.locator('#connect-button').click();await p.waitForFunction(()=>document.querySelector('#connection-label').textContent==='USB connected');await p.waitForTimeout(200)}
async function setup(p){await p.locator('nav a[href="#device-setup"]').click();if(!await p.locator('#carrier-timing').evaluate(e=>e.open))await p.locator('#carrier-timing summary').click()}
async function go(p,view){await p.locator(`nav a[href="#${view}"]`).click();await p.locator(view==='experiments'?'#sessions-view':'#'+view).waitFor({state:'visible'});await p.evaluate(()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve))))}
async function draft(p,hz,ns){await p.locator('#timing-frequency').fill(String(hz));await p.locator('#timing-deadtime').fill(String(ns))}
module.exports={assert,fs,out,initialize,launch,page,connect,setup,go,draft};
