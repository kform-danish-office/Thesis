# Control-chapter firmware naming

Edited eight files, leaving chapter.tex for the parent. Routine prose and captions now use baseline firmware, the voltage-control path, or V2 firmware rather than unexplained PWR labels. The DMA change is introduced by its behavior, and the V2 port is described as hardware adaptation followed by browser commands and logging.

The controller-development table now uses descriptive stages (Open loop, Blocking feedback, DMA feedback, Final baseline) instead of V0/V1/V2/PWR labels, so software development stages cannot be mistaken for hardware generations. Its implementation and purpose columns are unchanged. The parent’s new identity section retains the exact archived source identifiers for traceability; this section is referenced from the V2 source paragraph.

Timing-resources prose retains the need to identify each run from source, VER and EXPORT, and still notes a mismatch in older notes, without randomly dropping two revision numbers into the discussion. No version is assigned to the later powered V2 bench run.

Numerical quantities, math, labels, citations, source graphics, listing contents, pin assignments, electrical settings, and original newline conventions pass preservation checks (control-terms-checks.json). No build, manifest, GitHub or hardware actions were performed. Edits are frozen.

Files:
- 01_Control_Objectives.tex
- 02_Architecture_Timing.tex
- 07_V2_DMA.tex
- 08_Control_Law.tex
- 11_State_Machine.tex
- 13_Timing_Resources.tex
- 14_Version_Comparison.tex
- 15_PWR_2_Port.tex
