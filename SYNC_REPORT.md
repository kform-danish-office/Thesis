# Complete project source sync

This sync adds the available cloud project sources to the repository, alongside the previously published defense presentation. Existing GitHub history and release downloads are retained.

## Included

- `thesis/`: all 566 current source files, including data, photographs, colour schematics, bibliography and code snapshots; `Thesis_V1_V2_V3.pdf` is the existing 490-page compiled thesis.
- `working-source/`: current firmware, browser app, tests, documentation and historical source snapshots. Root firmware and documentation are also updated to the current working-source versions for compatibility.
- `skills/`: all 118 files from the imported user skill collection, including references, assets and scripts.
- `tooling/`: source processing, build helpers, voice instructions, review decisions and validation records. Original absolute cloud paths are retained in historical records.
- `source-archives/`: the approved original thesis and working-source ZIPs, imported skill archive, schematic originals and thermal archive. The three transport slices are omitted because their reconstructed original ZIP is included.
- `presentations/defense/`: the previously published PowerPoint, PDF and ZIP downloads, including the IEC harmonic-current comparison and common-scale adapter photographs. The latest reproducible build source is also extracted into `source/`.
- `local-handoff/`: the existing handoff manifest and package script. The large complete handoff ZIP remains available as a GitHub release asset.

Installed toolchains, dependency folders, caches, temporary build products, credentials, duplicate deployment payloads and duplicate review source snapshots are excluded. `tooling/vercel-payload/.env.local` is excluded.

## Verification

The staged thesis sources are checked byte-for-byte against the current editable thesis. Presentation binaries retain their previously accepted bytes. The new source tree is checked for credential files and key material before publication.

Checks run for this sync:

```sh
cd working-source/web
npm test
npm run build
cd ..
python firmware/test_web_protocol.py
python firmware/test_carrier_storage.py
```

Results: 76 browser tests pass; the browser build emits 15 files; production firmware protocol checks pass for 131 JSON frames; the production flash-journal checks pass all 122 interrupted-append boundaries. No hardware was flashed or configured. The thesis and presentation retain their previously compiled and reviewed PDFs; this sync does not rewrite them.

## Available snapshot limits

The resumed cloud filesystem contains the imported skill collection but does not contain the later custom `thesis-rewrite` and `defense-write` skill folders. Those missing folders are not reconstructed or represented as included. The latest accepted defense source is recovered from its previously published source ZIP. Earlier presentation variants remain in their existing download ZIPs.

See `LOCAL_START.md` for local commands and `project-sync-manifest.json` for file hashes. The selected `/workspace/Thesis` reference checkout is left untouched; the commit is assembled in a separate checkout.
