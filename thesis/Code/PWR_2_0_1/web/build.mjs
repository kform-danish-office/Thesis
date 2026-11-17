import {mkdir,copyFile,readFile} from 'node:fs/promises';
const files = ['index.html','styles.css','app.js','serial.js','protocol.js','storage.js'];
await mkdir(new URL('./dist/',import.meta.url),{recursive:true});
for (const file of files) { await readFile(new URL(file,import.meta.url)); await copyFile(new URL(file,import.meta.url),new URL(`dist/${file}`,import.meta.url)); }
console.log(`Built ${files.length} dependency-free application files in dist/.`);
