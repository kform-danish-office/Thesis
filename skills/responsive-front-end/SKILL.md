---
name: responsive-front-end
description: Implement responsive front-end screens and flows from supplied screenshots, visual references, or design briefs while reusing the target repository's design system and verifying appearance and behavior in a browser.
---

# Responsive Front-End from References

Turn the user's visual references into working UI in the requested project, preserving its component, styling, routing, state, and data-fetch conventions.

## Establish the visual target

Inspect the supplied screenshots and notes before implementation. Identify the layout, spacing, typography, colors, hierarchy, imagery, visible controls, and relevant interaction states. Treat the user's requirements and references as the source of truth for the intended design.

Inspect repository instructions and the existing screen structure, components, tokens, utilities, icons, and assets. Translate the references into those patterns. Prefer canonical components and tokens, with minimal targeted sizing or spacing adjustments when needed to match the reference. Do not create a parallel design system.

When starting a new project, use the user's chosen stack and establish a coherent component and token layer appropriate to the brief. Do not impose a new stack on an existing project.

Resolve minor visual ambiguities with the simplest implementation consistent with the overall direction and briefly report material assumptions. Ask only when a missing detail materially changes the requested outcome.

## Implement responsive behavior

Match the supplied layout and hierarchy closely at their reference sizes. Derive intermediate layouts from content constraints and existing breakpoints. Keep primary controls usable and text readable on desktop and mobile, including sizes for which no screenshot was supplied.

Preserve the project's routing, state ownership, and data-fetch patterns. Implement the requested controls and visible states, including relevant loading, empty, selected, hover, focus, and error states. Scope changes to the requested screens and flows.

Use existing assets where appropriate; avoid substituting generic layouts or decorative patterns that conflict with the references.

## Verify and refine

Use `$playwright-interactive` when available and direct Playwright control is permitted. Otherwise use the host's supported browser tools and report any verification limits. Follow the active tool documentation and permissions.

- Run the relevant build or project checks.
- Compare actual browser screenshots against the supplied references at matching viewport sizes. Inspect spacing, alignment, typography, hierarchy, colors, imagery, and visible states rather than relying on a successful build.
- Exercise the main interactions with normal input and confirm the visible outcomes.
- Check desktop and mobile layouts, plus an intermediate size when a layout transition warrants it. Investigate overflow, clipping, overlapping elements, unreadable text, and unreachable controls.
- Iterate on observed discrepancies and repeat affected checks. If an ambiguity, missing asset, or environment limitation prevents a match, identify the remaining gap instead of claiming completion.

Report the implemented result, the meaningful checks performed, and any material assumptions or unresolved differences. Include final screenshots when useful for reviewing the work.
