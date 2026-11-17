# Chapters 10–12 prose review

Reviewed every paragraph, caption, and table in these files (generated tables and figure inputs were not edited):

- `Chapters/10_Results/01_Prototype_Verification.tex`
- `Chapters/10_Results/02_Startup_Shutdown.tex`
- `Chapters/10_Results/03_Steady_State.tex`
- `Chapters/10_Results/04_Load_Transients.tex`
- `Chapters/10_Results/05_Open_Circuit.tex`
- `Chapters/10_Results/06_ZVS.tex`
- `Chapters/10_Results/07_Input_Power_Quality.tex`
- `Chapters/10_Results/08_Efficiency.tex`
- `Chapters/10_Results/09_Thermal.tex`
- `Chapters/10_Results/10_Firmware_Comparison.tex`
- `Chapters/10_Results/11_Simulation_Hardware.tex`
- `Chapters/10_Results/12_Compliance_Table.tex`
- `Chapters/10_Results/13_Failures_Lessons.tex`
- `Chapters/10_Results/14_Revised_Plan_Status.tex`
- `Chapters/10_Results/15_V2_Testing_Update.tex`
- `Chapters/10_Results/16_V3_Design_Outcome.tex`
- `Chapters/10_Results/17_V2_Secondary_Load_Tests.tex`
- `Chapters/10_Results/chapter.tex`
- `Chapters/11_Discussion/01_Key_Findings.tex`
- `Chapters/11_Discussion/02_Topology_Adaptation.tex`
- `Chapters/11_Discussion/03_Control_Contribution.tex`
- `Chapters/11_Discussion/04_Open_Circuit_Safety.tex`
- `Chapters/11_Discussion/05_Magnetics_Integration.tex`
- `Chapters/11_Discussion/06_Reference_Comparison.tex`
- `Chapters/11_Discussion/07_Limitations.tex`
- `Chapters/11_Discussion/08_Lessons_Learned.tex`
- `Chapters/11_Discussion/09_Future_Improvements.tex`
- `Chapters/11_Discussion/10_Plan_Gap_Diagnosis.tex`
- `Chapters/11_Discussion/chapter.tex`
- `Chapters/12_Conclusion/01_Project_Summary.tex`
- `Chapters/12_Conclusion/02_Research_Questions.tex`
- `Chapters/12_Conclusion/03_Contributions.tex`
- `Chapters/12_Conclusion/04_Future_Work.tex`
- `Chapters/12_Conclusion/chapter.tex`

Deliberate keeps: test identifiers that identify individual results; local limits on ripple, calibration and instrument disagreement; the 95 W thermal image and separate 100 W load setting; the non-equilibrium 137.08 W secondary result; V3 reduced-function status and uninstalled magnetics; citations, equations and physical test conditions. Source paths in LaTeX commands remain intact.

Lead review: proposal 10-05 changes a requirements-table row from archival traceability to configuration identification; check that this still addresses PR-09 adequately. Proposal 10-04 removes the checksum remark and retains uncertainty about attribution. The isolated 240 W EPR question in discussion is intentionally kept. Generated data tables and archival code were not changed.

Second contextual pass: the V1 steady-state and AC-coupled results retain their numeric distinctions, and the transient and no-load sections retain the specific missing measurements that affect interpretation. The V2 thermal sequence retains the non-monotonic R3 temperatures, increasing R1 temperatures, voltage droop and lack of equilibrium. Discussion and conclusion repeat principal findings for their distinct synthesis and research-question roles; their concrete future measurements remain useful. Proposed 10-06 now connects the modified tank, reported dead time and heating observation while leaving ZVS unverified. The line-waveform caption retains identical C3 data; the probe-scaling limitation appears once in the following paragraph. Additional proposals remove overview file inventory and focus the firmware comparison on its measurable timing gap.

## Section-by-section judgment, complete prose pass

### Chapter 10

- 01 Tested prototype: retained the highest matched connector power, tested settings and thermal-duration limit. Remove spreadsheet/file inventory and make capture interpretation direct (10-01, 10-09).
- 02 Startup: retained the specific absent synchronized signals and resulting unmeasured quantities; these explain the limitation.
- 03 Steady state: retained voltage-error equation, numerical results, abnormal ripple entries and coupling distinctions. Remove test-name bookkeeping (10-02); figure IDs identify actual captures.
- 04 Load transients: retained physical load removal, equation and missing event/state measurements, which explain why overshoot and control state cannot be resolved.
- 05 Open circuit: retained unloaded voltage values and the reason no-load power is undetermined; the no-load result differs from the load-removal section.
- 06 Switching: retained burst observations, frequency, gate-referenced ZVS method and unverified status; remove file/checksum narration (10-03, 10-04).
- 07 Power quality: retained numerical PF/THD, instrument differences, harmonic discrepancy, and calibration limitation; streamline line-waveform caption and text (10-07, 10-08).
- 08 Efficiency: retained formulae, quantitative estimates, excluded conflicting measurements and unresolved instrument discrepancy; connect preliminary nature to acquisition and power boundary (10-11).
- 09 Thermal: retain maxima, missing duration and lack of DC voltage at 4.7 A; express the camera/reference distinction directly (10-12).
- 10 Firmware: retain development table and PA1/PA2 distinction; focus combined-test limitation on unmeasured timing (10-10).
- 11 Model comparison: retain mismatch table and specific missing model features; they explain why no numerical validation is claimed.
- 12 Requirements: keep statuses and sustained-rating test requirements; replace checksum inventory in PR-09 with test identifiers and readings (10-05).
- 13 Bring-up: table retains detailed problems and corrective actions; tighten repeated prose while keeping actual corrections and power limit (10-13).
- 14 Revised plan: retain result and diagnostic table, which explicitly separates connector and secondary test points and supplies plan-specific acceptance status.
- 15 V2 tank and heating: retain removed inductor, leakage-only tank, 95 W image versus 100 W load setting and suspected via restriction. Connect timing and heating without claiming ZVS (10-06).
- 16 V3: retain reduced functionality, 8% estimate and uninstalled magnetics; comparison conditions prevent a misleading complete-supply comparison.
- 17 V2 secondary load: retain numerical droop, non-monotonic R3 temperatures, rising R1 and no equilibrium; these are necessary to interpret 137.08 W.
- Chapter introduction: retained as a short overview that separates V1 USB-C tests from V2 secondary tests.

### Chapter 11

- 01 Key findings: combine duplicated V1 regulation and high-power summaries and retain losses and next measurements (11-03).
- 02 Topology adaptation: relate load-dependent behavior to assessing the coupled power stages and heating (11-04).
- 03 Control: retained concrete DMA, carrier, PA1/PA2 and duty-control functions and the isolated-feature comparison.
- 04 Load disconnection: retained energy equation and implemented mitigation, plus the missing protection measurements and common failure path.
- 05 Magnetics: retained source attribution, measured values, winding heating, later droop and single EPR feedback question. These establish magnetic context and remain technically distinct.
- 06 Published comparison: retained comparator conditions, numerical efficiency and power-boundary limitations; the conditions matter to the comparison.
- 07 Limitations: retained high-load missing DC value, instrument synchronization, ZVS and formal tests; these summarize distinct outstanding validation.
- 08 Lessons: retain engineering explanations and proposed via investigation; replace appendix narration with the test-recording lesson (11-01).
- 09 Development priorities: retained specific measurements, V3 build requirements, and equivalent-function comparison; these are actionable next steps.
- 10 Power shortfall: retained different baseline calculations, diagnostic matrix and controlled retest requirements; no component loss is inferred from the input-output difference.
- Chapter introduction: retained concise V1/V2/V3 progression and remaining priorities.

### Chapter 12

- 01 Project outcome: retain original topology, implementation, V1 and V2 numerical results and V3 status. Focus the repeated milestone paragraph on sustained target and required measurements (12-03).
- 02 Research questions: retained question-by-question answers, reported operating-point limits and distinct magnetic and V3 status; this structure serves the conclusion.
- 03 Contributions: preserve software-check status and pending powered testing while removing file inventory (12-01); retain substantive measurement contributions (12-02).
- 04 Future work: retained specific measurements and tests for losses, thermal endurance, transients, protection and V3. These lead from the conclusions to the next experiments.
- Chapter introduction: retained concise project progression and observed priorities.
