---
name: playwright-interactive
description: Debug and verify local web or Electron apps with a persistent Node REPL and Playwright session, including functional testing, visual QA, and viewport checks. Use for iterative application development when direct Playwright control is available.
---

# Playwright Interactive

Keep browser and Electron handles alive across code changes so iterative debugging stays fast and evidence reflects the current app.

## Runtime and scope

- Use the available persistent Node JavaScript REPL (`mcp__node_repl.js` in this environment). Read its tool documentation before using it; tool names and image-emission APIs can differ between hosts.
- Confirm Playwright resolves from the target project or an available dependency runtime. Use existing dependencies and the project's package manager. Install packages or browser binaries only when needed and authorized for the task.
- Run under the current permissions. Request scoped escalation for an operation that requires it; do not modify global configuration or disable sandboxing as a prerequisite.
- Use direct Playwright for development targets when permitted by the host. When the task requires an existing user browser session or host browser controls, use those supported controls instead; this skill does not override tool restrictions.
- Keep evaluation scoped to the requested application and authorized side effects.

## Workflow

1. Build a compact QA inventory from requested behavior, the implemented controls and states, and the claims you intend to report. Scale coverage to the change and include relevant failure paths.
2. Read [session recipes and QA guidance](references/playwright-workflow.md) for bootstrap code and the applicable web, mobile, or Electron path. Read screenshot normalization details there when emitting screenshots, especially for native windows or high DPI displays.
3. Start or reuse the project's normal dev server in a persistent session and confirm it responds before navigation. Launch Electron through Playwright when testing an Electron development target.
4. Reuse shared handles. Reload for renderer changes; relaunch Electron for main-process, preload, or startup changes. Reset the REPL only to recover a broken kernel.
5. Test the relevant flow with real input and confirm its visible result. Use evaluation for diagnostics, not as a substitute for exercising controls.
6. Inspect visual states separately, including initial and relevant post-interaction views. Check viewport fit with screenshots and region bounds; document scroll metrics alone can miss clipped fixed panes. Use reproducible explicit viewports for routine web checks, and native-window checks when desktop behavior matters. Inspect Electron's initial layout before resizing.
7. Capture evidence from the final state. Report what passed and any unverified behavior without claiming broader coverage than performed.
8. Close owned browser contexts and Electron processes when finished, or deliberately retain them for ongoing work. Never close unrelated user sessions.

## Session invariants

- Reuse named top-level handles such as `browser`, `context`, `page`, `electronApp`, and `appWindow`; avoid repeated redeclarations that conflict with persistent bindings.
- Create a fresh context when changing between an explicit viewport and native-window mode.
- Normalize model-bound screenshots to CSS pixels unless device-pixel fidelity is the subject of the test. Add a clipped screenshot's origin when converting image coordinates into clicks.
- Electron contexts do not reliably support scratch pages. Use main-process `BrowserWindow.capturePage` and `nativeImage.resize` for screenshot normalization, targeting the window under test when several windows exist.
- Visible clipping remains a defect even when numeric scroll checks pass.
