---
name: web-design-engineer
description: Design, build, redesign, or critique polished browser-rendered interfaces and visual artifacts using HTML, CSS, JavaScript, or React. Use for pages, dashboards, interactive prototypes, web animations, HTML slides, and design-system exploration; not back-end or nonvisual coding, or conversion of prose into an article.
---

# Web Design Engineer

Create visually intentional, usable web artifacts. Choose typography, composition, assets, interaction, and motion to serve the audience and brief. Preserve the user's chosen output format and project stack.

## Understand and calibrate

Read supplied screenshots, design files, assets, code, and repository instructions. Extract existing tokens and component conventions from source; use screenshots as evidence of the intended appearance. Verify uncertain product specifications or current brand facts against authoritative sources when those facts affect the design.

Resolve the artifact, audience, visual direction, required interactions, and constraints from available context. Ask only for missing information that materially changes the result. When direction is open, offer a few visibly different approaches with concrete typography, layout, palette, and motion cues, then use the best-supported direction. Avoid a long taste questionnaire.

Classify existing-work changes as extension, redesign preserving the established system, or overhaul. Choose the smallest mode satisfying the request. Preserve routes, data contracts, analytics, forms, accessibility, and brand conventions unless changing them is in scope.

Form a concise design read: artifact, audience, visual language, change mode, and relative levels of visual variation, motion, information density, reliance on assets, and brand fidelity. Use these to make actual choices; numerical scores are optional.

Before choosing tokens, consider narrative role, viewing distance, visual tone, and content capacity. Summarize meaningful palette, type, spacing, radius, elevation, and motion decisions in a short update or established project notes. Reuse an existing system rather than inventing a parallel one.

For exploratory or substantial work, show a viewable early draft with the core composition and clearly identified temporary assets so the user can steer. Continue within the authorized brief; wait when the user explicitly requests staged approval or when a material unresolved choice requires their answer. Routine design decisions do not require repeated approvals.

## Build with care

- Use the project's existing framework, components, icon library, asset pipeline, and styling conventions. For standalone HTML, use CSS custom properties, Grid, and Flexbox. Add libraries only for a concrete need.
- Match brand identity through real logos, product imagery, and interface references when available. Prefer official sources and user-provided assets. Keep useful asset provenance in project notes when it aids reuse. Do not fabricate endorsements, testimonials, product facts, or metrics.
- Use clearly marked placeholders when required material is unavailable. Continue independent work and identify the missing asset; do not present an invented logo or generic silhouette as an authentic product image.
- Make layout, type scale, spacing, and contrast coherent. Avoid decorative filler and repetitive card layouts when they weaken hierarchy. Gradients, familiar fonts, emoji, and rounded corners are choices to evaluate against the brief, not universal bans.
- Use semantic elements, visible focus states, keyboard-operable controls, readable contrast, and appropriate touch targets. Provide relevant empty, error, loading, disabled, and selected states.
- Make responsive behavior deliberate. Check smaller screens and dense content. Use fluid type and container queries where useful and supported by the project.
- Prefer simple CSS transitions for micro-interactions. Use the established animation library or a timeline only when complexity warrants it. Respect reduced motion and provide persistent static feedback for meaningful state changes.
- Keep files and exports consistent with the repo. For standalone global-script demos, namespace shared globals to prevent collisions. Do not impose global `window` exports or inline Babel on module-based React projects.
- Within embedded previews, prefer scrolling the intended pane when `scrollIntoView` would move the outer host unexpectedly. This is a context-specific constraint.
- Add variants or a hidden adjustment panel when requested or useful for design exploration, not as unsolicited product features. Preserve versions using the project's normal version control and file conventions.

Read [artifact patterns](references/artifact-patterns.md) only for the output type at hand. Read [critique and verification](references/critique-and-verification.md) for critique requests or final review.

## Verify and deliver

Run project checks appropriate to the change. Inspect the rendered artifact when appearance, responsiveness, or interaction is central, using supported browser tools or `$playwright-interactive` when available and permitted. Scale testing to the work; do not require a special request to verify visual claims.

Compare against references at matching sizes, exercise critical interactions, and inspect initial and meaningful changed states. Check clipping, overflow, layering, alignment, readability, and viewport fit. Fix observed discrepancies and repeat affected checks. Record verification limits honestly.

Deliver the artifact with a concise statement of the result, meaningful verification, and material gaps. Do not claim a browser or visual pass from source inspection alone.
