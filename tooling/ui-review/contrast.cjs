const {chromium}=require('/opt/codex/cua_node/lib/node_modules/playwright');const fs=require('node:fs');
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--no-sandbox']});const result=[];
for(const url of ['/','/calculator.html']){const p=await b.newPage({viewport:{width:1440,height:1000}});await p.goto('http://127.0.0.1:4173'+url);await p.waitForTimeout(100);
result.push(await p.evaluate(()=>{
const rgb=s=>(s.match(/[\d.]+/g)||[]).map(Number);const luminance=s=>{let c=rgb(s).slice(0,3).map(x=>{x/=255;return x<=.04045?x/12.92:((x+.055)/1.055)**2.4});return c[0]*.2126+c[1]*.7152+c[2]*.0722};const ratio=(a,b)=>{let x=luminance(a),y=luminance(b);return(Math.max(x,y)+.05)/(Math.min(x,y)+.05)};
const bg=(e)=>{for(let n=e;n;n=n.parentElement){let c=getComputedStyle(n).backgroundColor;let v=rgb(c);if(v.length<4||v[3]===1)return c}return'rgb(255,255,255)'};
let text=[],boundaries=[],labels=[];
for(const e of document.querySelectorAll('body *')){let s=getComputedStyle(e),r=e.getBoundingClientRect();if(!r.width||!r.height||s.visibility==='hidden'||e.closest('[hidden]')||e.matches(':disabled'))continue;
if([...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim())){let c=ratio(s.color,bg(e)),large=parseFloat(s.fontSize)>=24||(parseFloat(s.fontSize)>=18.67&&parseFloat(s.fontWeight)>=700);if(c<(large?3:4.5))text.push({tag:e.tagName,id:e.id,classes:e.className,text:e.textContent.trim().slice(0,80),ratio:c,color:s.color,bg:bg(e),size:s.fontSize});}
if(e.matches('input,select,textarea,button.button.secondary')){let c=ratio(s.borderTopColor,bg(e.parentElement));if(c<3)boundaries.push({id:e.id,tag:e.tagName,classes:e.className,ratio:c,border:s.borderTopColor,bg:bg(e.parentElement)});}
if(e.matches('input,select,textarea')&&!e.labels?.length&&!e.getAttribute('aria-label')&&!e.getAttribute('aria-labelledby'))labels.push(e.id);
}
return{url:location.pathname,text,boundaries,missingLabels:labels};
}));await p.close()}fs.writeFileSync('/workspace/tooling/ui-review/contrast.json',JSON.stringify(result,null,2));console.log(JSON.stringify(result));await b.close()})();
