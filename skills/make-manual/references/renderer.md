# Portable Markdown renderer

Use `scripts/render_manual.py` when a compact, reproducible PDF is useful. It is self-contained and runs offline. It imports no project-specific code. Python 3.10 or newer is required.

```sh
python -m pip install -r scripts/requirements.txt
python scripts/render_manual.py --source manual.md --output output/manual.pdf
```

Paths on the command line resolve from the working directory. Images in Markdown resolve from the Markdown file's directory. The output directory is created when necessary.

The helper uses US Letter pages, at least 45-point body margins, 10.5-point body text, 10-point table text, and 9.3-point monospace code. Tables wrap and repeat headers. Long code lines wrap; long code blocks can split across pages. Images preserve their aspect ratio and use the printable width, limited to one page's height. Use focused screenshots if a full-screen image makes labels too small.

There is no automatic cover. The first `#` heading appears in the normal page flow. A standalone `---` starts the next page; use one after introductory content only when a separate cover is wanted. Consecutive and trailing page breaks do not create blank pages.

## CLI

Required: `--source PATH`, `--output PATH`.

Optional:

- `--profile PATH`: brand JSON below. Omitting it uses neutral colors and built-in Helvetica/Courier fonts, with no invented organization or logo.
- `--callouts PATH`: per-image sizing and numbered callout JSON below.
- `--title TEXT`: running-header/PDF title; also replaces the first `#` heading. Otherwise the first `#` heading, or source filename, supplies the title.
- `--subtitle TEXT`: second running-header line and PDF subject. It does not insert an extra body heading.
- `--revision TEXT`: footer revision. Otherwise read from a source phrase such as `Document Rev 1.0`.
- `--date TEXT`: footer date in US form, such as `October 23, 2026`. Otherwise use the first date in that form found in the source; omit the footer date when absent.

Metadata overrides affect running furniture and PDF metadata. Except for the first title heading, the source body remains authoritative; update its printed revision/date when those should change too.

## Brand profile

The optional object uses these keys. Relative logo and font paths resolve against the profile JSON's parent directory, not the working directory. Missing optional keys fall back to neutral defaults. Packaged fonts should include their license files.

```json
{
  "organization": "KFORM Systems",
  "colors": {
    "charcoal": "#101416",
    "accent": "#C9AD73",
    "ink": "#242E33",
    "muted": "#586A72",
    "light": "#F4F5F3",
    "line": "#D6DCDA"
  },
  "logo": "kform/kform-logo-inverse.png",
  "fonts": {
    "heading": "kform/BebasNeue-Regular.ttf",
    "body": "kform/IBMPlexSans-Regular.ttf",
    "bold": "kform/IBMPlexSans-Bold.ttf",
    "mono": "kform/IBMPlexMono-Medium.ttf"
  }
}
```

Colors must be six-digit `#RRGGBB`. Font files must be local TrueType files. The header has a dark background, so choose a suitable inverse logo. Accent-filled number circles use charcoal text: use an accent with readable contrast. A font must cover the source's characters; supply an appropriate font profile for scripts unsupported by the neutral built-in fonts.

```sh
python scripts/render_manual.py --source manual.md --output output/manual.pdf \
  --profile assets/kform-profile.json --subtitle "Quick Start Guide" \
  --revision 1.0 --date "October 23, 2026"
```

## Images and callouts

Markdown images are local files. Remote URLs are never fetched. Their alt text becomes the printed caption. Keep the original screenshots/photos unchanged; this helper draws circles, endpoints, and leaders as separate PDF vectors.

```markdown
![Preview example with generated readings.](figures/monitor.png)
```

The optional callout JSON contains an `images` array. Each `image` path resolves against the callout JSON's parent. It must resolve to the same file used by the Markdown. An entry can contain `width_pt` without callouts to size a graph or other inset.

```json
{
  "images": [
    {
      "image": "figures/monitor.png",
      "width_pt": 522,
      "callouts": [
        {"number": 1, "side": "left", "target": [0.08, 0.44]},
        {
          "number": 2,
          "side": "right",
          "target": [0.84, 0.68],
          "marker_y": 0.61,
          "route": [[0.98, 0.61], [0.84, 0.61]]
        }
      ]
    },
    {"image": "figures/graph.png", "width_pt": 470}
  ]
}
```

- `image`: required local file path.
- `width_pt`: optional requested image width, from 40 through 522 points. Defaults to the full printable width. Annotated images reserve 16-point number rails on each side, so their actual image width is at most 490 points. Extremely tall images also scale to fit one page.
- `callouts`: optional array. Numbers must be unique integers from 1 through 99 within that image.
- `side`: required `left` or `right`; the number circle sits in that external rail.
- `target`: required `[x, y]`, normalized from 0 through 1. `[0, 0]` is the image's upper-left corner; `[1, 1]` is its lower-right corner.
- `marker_y`: optional normalized vertical circle position; defaults to the target's y coordinate. Separate nearby circles to avoid collisions.
- `route`: optional normalized `[x, y]` vertices, visited after leaving the circle and before reaching the target. Route leaders through whitespace and terminate at control borders, avoiding UI labels. The helper does not infer interface semantics or detect leader/text collisions.

Use matching numbers in the instructions. Include a clear caption when screenshots contain Preview/generated data. Visually verify each annotation after rendering.

## Supported Markdown and limits

Supported blocks: `#` through `######` headings, paragraphs, flat bullet/numbered lists with continuation lines, fenced code, blockquotes, local images, and simple pipe tables with a separator row. Begin/end each table row with `|`; escape a literal cell pipe as `\|`. Table rows must have matching cell counts. `<br>` supplies a line break inside a cell or paragraph; Markdown's two trailing spaces are collapsed to an ordinary space. Inline support includes bold, italic, code, and Markdown link labels.

Markdown links render as plain labels. No active links or URI annotations are emitted; bare URL text remains printed text. Raw HTML, embedded HTML images, nested lists, footnotes, automatic contents, and advanced Markdown extensions are outside this focused helper. Write those sections plainly or use a more suitable document workflow.

The build checks for active PDF hyperlinks, but a successful build is not visual approval. Render every page with the PDF workflow, inspect screenshots/table wrapping/code/page furniture, and fix clipping, overlaps, unreadable labels, blank pages, or orphan-only pages before delivery. No marker or PDF generation is triggered by importing the module or running `--help`.
