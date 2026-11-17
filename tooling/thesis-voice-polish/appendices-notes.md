# Appendix voice polish

All ten appendices A–J were read and revised sentence by sentence against the new voice-polish baseline. Source is frozen. Reported builds, processing, and measurements retain natural passive wording. Definitions and software behavior use direct grammar where forced passives obscured the meaning. No first- or second-person narrative pronouns remain.

Representative changes:

- “Two software baselines are retained for the controller development” → “Two firmware versions are included.”
- “USB-C connector output current is measured by neither pin” → “Neither pin measures USB-C connector output current.”
- “The software request is aligned ... without an interrupt being run” → “The software request is aligned ... without an interrupt.”
- “With ... an import is grouped” → the configuration delimiters “bracket an import.”
- “External power or timing measurements are replaced by neither value” → “Neither replaces external power or timing measurements.”
- “Passing results were obtained for the 38 Node tests” → “All 38 Node tests passed.”

The distinction between earlier measurements, frozen PWR-2.0.1 software checks, reported V2 performance, and planned V3 work remains intact. Contribution credit, incomplete records, calibration/timing limits, and the missing calculator UI are preserved. Original UTF-8 source files remain in the editable package; their SHA-256 checksums are recorded in the manifest.

Checks passed against /workspace/tooling/thesis-voice-polish/before for all ten files: exact numeric sequence (including signs and decimal separators), math, LaTeX command/argument sequence, headings, protected figures/tables/captions/listings, source paths, and CRLF/LF sequence. All ten source paths remain present. No build or global manifest was changed.

Frozen source hashes:

- `A_Analytical_Equations.tex`: `217bc883b8cd4cb52d8a91e0b64806abc8f446d5ea24cf31b3312d73c39c9c63`
- `B_Hardware_Documentation.tex`: `7819fd5cfc31c7317f2bada3c647a5f761291b6be41929f189a137f575aa0788`
- `C_Firmware_Documentation.tex`: `e994ec807c895143f46e8ab47c053952a2e7576eaafab40761625f517ade2bc1`
- `D_Modeling_Files.tex`: `c45630ff040c9837eeab7901d1ce57a77e079567e6b348e79510c85d48e90807`
- `E_Experimental_Data.tex`: `18d98683912b9871073c7bd6f90fcdea9d5544fae199f8de859246d90b6f2f37`
- `F_Contribution_Provenance.tex`: `b5cabbd965e996f4c897bca716ec3644f73a749b39de00f1d94a88bc1b5303ff`
- `G_Software_Tools.tex`: `121b098930827b47ac617897f2b462dd57b70fafb5eec2a9558fa31bc6621895`
- `H_Full_Embedded_Source.tex`: `fc241186e4621b12fbe776357d758aa3e49a45d3df79f1512b4a9456c3086406`
- `I_Full_Supporting_Source.tex`: `ea2c563245a08bd0899f2481ce397bc91ccc95ed40f5a4f57b93ac647cf395ec`
- `J_Revised_Plan_Integration.tex`: `c05e89998796472b849b806f291d66f9e52aa887cf5840421fad8b01cd16dd57`

Cross-review is complete with no unresolved findings. Root applied two C corrections: OFF inhibits commanded transfer rather than guaranteeing that stored resonant energy has stopped moving, and ZEROI readings have a software delay between reads rather than an exact sampling interval. The updated C hash above is e994ec807c895143f46e8ab47c053952a2e7576eaafab40761625f517ade2bc1. The reviewer verified both corrections; no source was changed while updating this note.
