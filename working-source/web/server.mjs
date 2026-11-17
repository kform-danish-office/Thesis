import http from 'node:http';
import {readFile} from 'node:fs/promises';
const allowed = new Set(['index.html','styles.css','app.js','serial.js','protocol.js','storage.js','calculator.html','calculator.css','resonance.js','resonance-ui.js','resonance-presets.js','fonts/IBMPlexSans-Regular.ttf','fonts/IBMPlexSans-Bold.ttf','fonts/IBMPlexMono-Medium.ttf','fonts/OFL-IBMPlex.txt']);
const types = {html:'text/html; charset=utf-8',js:'text/javascript; charset=utf-8',css:'text/css; charset=utf-8',ttf:'font/ttf',txt:'text/plain; charset=utf-8'};
const config = JSON.parse(await readFile(new URL('./vercel.json',import.meta.url),'utf8'));
const server = http.createServer(async(req,res) => {
  try {
    let file = decodeURIComponent(new URL(req.url,'http://localhost').pathname).slice(1) || 'index.html';
    if (!allowed.has(file)) { res.writeHead(404); res.end('Not found'); return; }
    for(const h of config.headers[0].headers) res.setHeader(h.key,h.value);
    const body = await readFile(new URL(file,import.meta.url));
    res.writeHead(200,{'Content-Type':types[file.split('.').at(-1)],'Content-Length':body.length}); res.end(body);
  } catch { res.writeHead(500); res.end('Unable to load app file'); }
});
server.listen(Number(process.env.PORT || 4173),'127.0.0.1',() => console.log(`Local: http://localhost:${server.address().port}`));
