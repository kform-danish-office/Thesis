# Screenshots and numbered callouts

## Capture the real interface

Use the available browser automation workflow for the current app. Prefer a normal, useful screen over a loading state or a diagnostic wall. Capture only what the steps need; crop browser chrome and unrelated personal tabs. Keep navigation in the picture or explain once that the crop shows only the main panel and name the menu used to reach it.

Prefer the application's built-in Preview or an isolated fixture for documentation when staging a real device would change power, routing, stored data, or an active test. Intercept hardware requests in the isolated context. Do not disconnect an active board simply to open Preview: use a separate browser context with no real bridge access. Do not change production code or mask an error to manufacture a connected screenshot.

Use actual user controls to reach the capture state. Wait for fonts and data to settle. If an average takes time to fall to zero after switching off, wait for the displayed state to match the demonstrated operation. For recording, use a neutral session name and show a stopped capture with export available when illustrating export. Keep the graph visible and running when demonstrating monitoring, unless the step specifically explains pausing.

Keep Preview/sample-data labels visible and say that readings are generated examples. Distinguish those screenshots from measurements taken on hardware. Caption the relevant app version and the state that affects a button's label. Never replace an actual screenshot with an AI-generated imitation of a working interface.

## Make them readable in print

Capture at an explicit desktop viewport and suitable device scale (often 2x). Pixel count alone does not make small UI text readable: use focused views and a large printed width. Split a large screen into clearly captioned crops or give it its own page before shrinking the labels. Preserve aspect ratio.

Prefer one primary job per screenshot: readings/graph, power and routing, or recording/export. Do not fill the manual with every setup/debug panel just because it exists.

## Add callouts separately

Keep original PNGs unchanged. Use vector numbered circles and leader lines in the document renderer so numbers stay sharp. Place markers in side/top/bottom rails or whitespace and route leaders around control labels. Point to the actual connector, switch, selection field, or button, rather than an approximate region.

Match the figure numbers to the surrounding instructions. Make clear when numbers restart on a new figure. For a board photo, state the viewpoint and keep it consistent with the switch-direction wording. Do not infer pin 1 or left/right from a mirrored underside picture.

The portable renderer's optional callout format is described in [renderer.md](renderer.md). If the existing project has a callout builder, prefer it and verify the final target positions visually.

## Check the final pages

Render and inspect every page after the final changes. Check that:

- The important labels can be read at the intended print size.
- Preview labels and the state-specific caption remain visible.
- No leader crosses essential text or points to the wrong control.
- Every numbered step refers to the correct visible number.
- Screenshots and board photos are neither stretched nor clipped.
- Headers, footers, revision, date, and page count are correct on every page.
- There are no orphan captions, blank pages, broken tables, or tiny code.

Use PDF text/bounds/image checks as supporting evidence, not a replacement for looking at the rendered pages. If a viewer seems to omit repeated header furniture, inspect the actual PDF/page pixels before changing a renderer that is already correct.
