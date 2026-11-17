const {chromium}=require('/opt/codex/cua_node/lib/node_modules/playwright');
const fs=require('node:fs');
(async()=>{const browser=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--no-sandbox']});let results=[];
for (const [pageName,url] of [['monitor','/'],['calculator','/calculator.html']]) {
 for (const width of [1440,390,320,768]) {
  const page=await browser.newPage({viewport:{width,height:width===1440?1000:844}});
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:4173'+url);await page.evaluate(()=>document.fonts.ready);
  if([1440,390].includes(width)) await page.screenshot({path:`/workspace/tooling/ui-review/final-${pageName}-${width}.png`,fullPage:true});
  const dimensions=await page.evaluate(()=>({width:innerWidth,doc:document.documentElement.scrollWidth,height:document.documentElement.scrollHeight}));
  results.push({pageName,width,dimensions,errors}); await page.close();
 }
}
fs.writeFileSync('/workspace/tooling/ui-review/final-responsive.json',JSON.stringify(results,null,2));console.log(JSON.stringify(results));await browser.close();})();
