# V2 introduction and story update

Edited only `Chapters/01_Introduction`.

Changes:
- Chapter opening now follows the first G071 prototype through the integrated F410 V2 board.
- Motivation identifies the G071 implementation as the first stage rather than the whole project.
- Goals retain the reported 85 W/15 W shortfall/100 W plan figures while recognizing that V2 has since been operated with its modified tank.
- Control research question now includes carrying the control from the first prototype to V2.
- Contributions and scope include the F410 port, board integration, browser interface and powered tank changes.
- Thesis structure points to V2 hardware, the F410 port, and complete schematic/PCB documentation.
- New `08_V2_Prototype.tex` is included after Project Goals. It introduces `sec:intro-v2` and `tab:intro-v2-specs`.

The new specification table states the verified drawing/controller/PCB facts: F410CBU6, LMG2652RFBR, AMC0330, PA0/PA1/PA2 feedback meanings, MPQ4242, BAC1S12SC, LMR54410 local supplies, four copper layers, archived 1 MHz/40 ns PWR-2.0.1 timing. It does not invent dimensions, copper weight, thickness or ratings.

Later bench operation is described separately: leakage-only tank around 1.66 nF, reported 60 ns software dead time, and reported 95 W thermal run. No continuous output, numerical loss improvement, or ZVS validation is claimed. The older matched 79.89 W result remains tied to modified V1.0. Unresolved drawing values/scaling point to the hardware chapter.

Parent-provided cross-references used: `sec:hw-v2`, `sec:res-v2-testing`, `sec:app-v2-oct27`. No figure reference required.

Edited existing files: chapter.tex, 01_Motivation.tex, 03_Aim_Objectives.tex, 04_Research_Questions.tex, 05_Contributions_Attribution.tex, 06_Scope_Limitations.tex, 07_Thesis_Structure.tex. New file: 08_V2_Prototype.tex. Existing byte newline conventions and final-newline status preserved; new file uses CRLF. No builds/manifests or other source edits.
