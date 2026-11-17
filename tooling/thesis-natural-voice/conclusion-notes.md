# Discussion, conclusion and appendices wording pass

Read Chapters 11–12 and all appendices. Changes focus on vague or unnatural phrases, long chains of abstract nouns, and repeated audit-style qualification. Factual limits and uncertainty are retained, with direct explanations of the measurements needed. No figures, tables, headings, values, equations, source listings or command arguments were intentionally changed.

Changed files:
- Chapters/11_Discussion/01_Key_Findings.tex
- Chapters/11_Discussion/02_Topology_Adaptation.tex
- Chapters/11_Discussion/03_Control_Contribution.tex
- Chapters/11_Discussion/04_Open_Circuit_Safety.tex
- Chapters/11_Discussion/05_Magnetics_Integration.tex
- Chapters/11_Discussion/06_Reference_Comparison.tex
- Chapters/11_Discussion/07_Limitations.tex
- Chapters/11_Discussion/08_Lessons_Learned.tex
- Chapters/11_Discussion/09_Future_Improvements.tex
- Chapters/11_Discussion/10_Plan_Gap_Diagnosis.tex
- Chapters/12_Conclusion/chapter.tex
- Chapters/12_Conclusion/02_Research_Questions.tex
- Chapters/12_Conclusion/03_Contributions.tex
- Chapters/12_Conclusion/04_Future_Work.tex
- Backmatter/Appendices/A_Analytical_Equations.tex
- Backmatter/Appendices/C_Firmware_Documentation.tex
- Backmatter/Appendices/D_Modeling_Files.tex
- Backmatter/Appendices/E_Experimental_Data.tex
- Backmatter/Appendices/G_Software_Tools.tex
- Backmatter/Appendices/H_Full_Embedded_Source.tex
- Backmatter/Appendices/I_Full_Supporting_Source.tex
- Backmatter/Appendices/J_Revised_Plan_Integration.tex

Examples:

- Chapters/11_Discussion/01_Key_Findings.tex
  - Before: Average regulation is only part of the design: ripple remains, input-current behavior changes with load, and the thermal images show substantial surface heating.
  - After: The regulated average voltage does not describe the whole result. Ripple remains, input current changes with load, and substantial surface heating is visible in the thermal images.

- Chapters/11_Discussion/01_Key_Findings.tex
  - Before: The most complete high-power set covers
  - After: The most complete high-power measurements cover

- Chapters/11_Discussion/01_Key_Findings.tex
  - Before: The large input--output power difference and hot surfaces show why stage power and temperature need to be measured together before further tuning based on VBUS.
  - After: The large input--output power difference and surface heating need to be investigated through simultaneous stage-power and temperature measurements. Further tuning cannot be based on VBUS alone.

- Chapters/11_Discussion/02_Topology_Adaptation.tex
  - Before: The operating strategy also had to accommodate the detachable connector.
  - After: The control also had to account for load disconnection.

- Chapters/11_Discussion/02_Topology_Adaptation.tex
  - Before: The selected output was maintained under the tested loads, as shown by the measured mean voltages. Ripple and input quality still changed with load. Burst spacing and fixed consumption matter more at low demand; current and heating become concerns at high demand.
  - After: The selected output voltage was maintained under the tested loads, as shown by the measured mean values. Ripple and input-current quality still changed with load. At low demand, burst spacing and fixed power consumption have a greater effect. At high demand, current and heating become limiting concerns.

- Chapters/11_Discussion/03_Control_Contribution.tex
  - Before: Fast switching was kept separate from the slower control of energy transfer. The
  - After: Carrier generation was kept separate from the slower control of energy transfer. The

- Chapters/11_Discussion/03_Control_Contribution.tex
  - Before: Soft switching still needs to be checked using current and node-voltage measurements at the actual commutations.
  - After: Soft switching still needs to be checked from current and node-voltage measurements during the switching transitions.

- Chapters/11_Discussion/03_Control_Contribution.tex
  - Before: Under load, the starting demand is set from the retained average duty and trimmed by voltage error. Loaded boost responds to sag; transfer is suppressed by an upper-voltage decision.
  - After: Under load, demand is initialized from the retained average duty and adjusted according to voltage error. Extra duty is applied when voltage sags, and transfer is suppressed above the upper voltage threshold.

- Chapters/11_Discussion/03_Control_Contribution.tex
  - Before: Separate branches avoid forcing a single duty setting onto different energy conditions.
  - After: Separate control branches allow different duty limits to be used under load and at no load.
