# Artifact patterns

## Interactive prototypes

Show the product immediately, with working primary paths. Device frames are useful when they explain the target environment. Include relevant control and feedback states. For requested exploration, vary meaningful layout or interaction choices rather than only recoloring. Keep prototype-only controls outside the product flow or hide them for presentation.

## HTML slides

Use the requested aspect ratio; a 16:9 fixed canvas is a reasonable default for projector presentations. Scale uniformly to the viewport, keeping navigation reachable outside the scaled canvas. Support keyboard navigation without hijacking focused form inputs. Use human-facing slide numbers starting at one. If persisting position, namespace storage and tolerate storage failures. Keep text readable at the intended viewing distance and avoid dense slide copy. Use actual presentation tooling when the user requested an editable presentation format.

## Dashboards and visualizations

Use the project's chart library, or choose a lightweight option appropriate to the complexity. Resize charts with their containers. Make color encoding semantic and provide labels or other noncolor cues. Label sample data; do not imply it is production data. Support themes when required by the product. Remove chart decoration that competes with the information.

## Animation and demos

Start with CSS, then state-based transitions or requestAnimationFrame. Use an established timeline library when choreography requires it. For timeline demos, provide play/pause and scrubbing when useful. Ensure reduced-motion users can understand the result and avoid gratuitous intros that obscure the content.

## Standalone React demos

Prefer the project's bundler when present. Inline React/Babel CDNs are an option only for a suitable throwaway HTML prototype. Verify compatible pinned versions and any integrity hashes from authoritative sources; never invent hashes. Separate script blocks need explicit shared bindings when their compilation scope is isolated. These constraints do not apply to ordinary module imports and exports.
