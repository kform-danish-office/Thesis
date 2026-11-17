# Chapters 2–4 direct-language pass

The complete prose, captions, headings and qualitative table wording in Chapters 2–4 were reviewed. The user explicitly requested a wider pass than the earlier prose-only edits. This pass includes the table captions, headers and notes that previously remained unchanged.

20 files received 79 local replacements. No builds, manifests, repository operations, firmware changes or publication were performed by this agent.

## Main changes

- Replaced assessment/acceptance-record table captions and headers with the tests, measurements or design tasks being described.
- Named MCU pins directly, including the burst-enable pin, without changing any assignment.
- Rewrote the architecture caption to describe the transformer, feedback isolator and measured quantities instead of saying the drawing was interpreted against another revision.
- Replaced the design-summary organizing paragraph with “Table summarizes the prototype parameters used in the calculations.” Nominal, supplied and calculated status stays in the table notes where it matters.
- Simplified vague analysis instructions to name actual waveform checks, PF/THD measurements and burst-start behavior.
- Kept ZVS polarity/timing limits, incomplete model assumptions, unconfirmed continuous ratings, pending protocol tests, source attribution and precharge attempt-limit behavior.

## Examples

### 03_Requirements_Architecture/02_Electrical_Specifications.tex

Before: Quantity & Required interpretation

After: Quantity & Measurements and test conditions

### 03_Requirements_Architecture/03_Functional_Requirements.tex

Before: Requirement identifiers connect the implemented control functions and measured performance to the results assessment.

After: The FR labels identify control functions, and the PR labels identify performance tests in the results chapter.

### 03_Requirements_Architecture/06_System_Architecture.tex

Before: Functional architecture of the tested V1.0 assembly, interpreted with the V1.1 schematic corrections. Charge-pump transfer and resonant transfer use the shared GaN stage. PA1 senses the secondary bulk bus before the USB-C output stage; PA0 and PA2 indicate primary voltage and half-bridge current. The transformer and AMC0330 blocks span their functional isolation boundary.

After: Power and control architecture of the V1.0 prototype with the V1.1 circuit corrections. The transformer carries power across the isolation barrier, and the AMC0330 returns secondary-bulk feedback to the MCU. PA1 measures this feedback; PA0 and PA2 measure primary voltage and half-bridge current.

### 04_Topology_Analysis/02_Switching_Cycle.tex

Before: Ideal pump-branch intervals in the modified charge-pump topology. Device names refer to functional paths in the reference analysis.

After: Ideal charge-pump intervals during one switching cycle.

### 04_Topology_Analysis/11_Design_Summary.tex

Before: Table~\ref{tab:analysis-design-summary} lists the values used to connect the reference equations to the prototype. It separates nominal circuit values, supplied magnetic measurements, and calculated estimates.

After: Table~\ref{tab:analysis-design-summary} summarizes the prototype parameters used in the calculations.

## Preservation checks

`python3 /workspace/tooling/thesis-direct-language/validate-early.py` passes. All numerical tokens, SI expressions, mathematical expressions, labels, citations, references, source/graphics paths and code/TikZ environments match the baseline. Existing table column counts and line-ending styles are unchanged. Numeric/data cells were not edited. Caption, heading and qualitative table text changes are intentional and are recorded in `early-edits.json` and `early-prose.diff`.

## Changed files

- `Chapters/02_Background/01_Offline_ACDC_PFC.tex`
- `Chapters/02_Background/03_ClassDE_Resonant.tex`
- `Chapters/02_Background/04_Soft_Switching_GaN.tex`
- `Chapters/02_Background/05_Reference_2020.tex`
- `Chapters/02_Background/06_Reference_2021.tex`
- `Chapters/03_Requirements_Architecture/chapter.tex`
- `Chapters/03_Requirements_Architecture/01_Use_Case.tex`
- `Chapters/03_Requirements_Architecture/02_Electrical_Specifications.tex`
- `Chapters/03_Requirements_Architecture/03_Functional_Requirements.tex`
- `Chapters/03_Requirements_Architecture/04_USBC_Interface.tex`
- `Chapters/03_Requirements_Architecture/05_Safety_Protection.tex`
- `Chapters/03_Requirements_Architecture/06_System_Architecture.tex`
- `Chapters/03_Requirements_Architecture/07_Operating_Modes.tex`
- `Chapters/03_Requirements_Architecture/08_Verification_Matrix.tex`
- `Chapters/03_Requirements_Architecture/09_Revised_Plan_Criteria.tex`
- `Chapters/04_Topology_Analysis/01_Topology_Overview.tex`
- `Chapters/04_Topology_Analysis/02_Switching_Cycle.tex`
- `Chapters/04_Topology_Analysis/03_Line_Cycle_PFC.tex`
- `Chapters/04_Topology_Analysis/05_Pump_Inductor.tex`
- `Chapters/04_Topology_Analysis/11_Design_Summary.tex`

## Independent review

A read-only reviewer checked all 79 replacements across the 20 files, including the higher-risk captions, requirements tables, architecture, safety and power-density passages. No actionable findings remain. Supplied-measurement and series-connection assumptions are preserved in the design-summary table. See `early-independent-review.md`. Sources are frozen.
