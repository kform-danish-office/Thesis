import {mkdir, copyFile, readFile} from 'node:fs/promises';

// Keep the payload limited to the app and its local font assets.
const files = [
  'index.html', 'styles.css', 'app.js', 'serial.js', 'protocol.js', 'storage.js',
  'calculator.html', 'calculator.css', 'resonance.js', 'resonance-ui.js',
  'resonance-presets.js',
  'fonts/IBMPlexSans-Regular.ttf', 'fonts/IBMPlexSans-Bold.ttf',
  'fonts/IBMPlexMono-Medium.ttf', 'fonts/OFL-IBMPlex.txt',
];

for (const file of files) {
  const source = new URL(file, import.meta.url);
  const destination = new URL(`dist/${file}`, import.meta.url);
  await readFile(source);
  await mkdir(new URL('.', destination), {recursive: true});
  await copyFile(source, destination);
}
console.log(`Built ${files.length} dependency-free application files in dist/.`);
