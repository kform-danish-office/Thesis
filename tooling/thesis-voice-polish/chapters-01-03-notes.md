# Voice polish: Chapters 01–03

All 27 assigned `.tex` files were read in full and polished against the new immutable baseline at `/workspace/tooling/thesis-voice-polish/before`. The earlier passive-review backup was not used as the comparison baseline.

| Chapter | Files edited | Changed source lines |
| --- | ---: | ---: |
| 01 Introduction | 8 | 24 |
| 02 Background | 9 | 18 |
| 03 Requirements and Architecture | 10 | 28 |
| Total | 27 | 70 |

The pass made 86 specific prose edits. Word tokens across the assigned files decreased from 8,369 to 8,194; unchanged protected material is included in both counts. Edits were selected sentence by sentence, not applied as global word substitutions.

## Representative changes

- Before: “The implementation choices are connected to the tests and remaining development work through five questions:”
  After: “Five questions connect the implementation choices to the tests and remaining work:”
- Before: “The term inherent PFC is used to describe this charge-transfer mechanism. The expected current envelope is explained by this mechanism …”
  After: “Inherent PFC refers to this charge-transfer mechanism and its expected current envelope.” The following PF/THD measurement requirement remains.
- Before: “The applicable configuration is used when a waveform is interpreted.”
  After: “Each waveform is interpreted with the applicable configuration.”
- Before: “The PCB was designed and assembled, the supplied inductor and transformer were integrated, the power, auxiliary, sensing, and output-interface circuits were implemented, and the STM32G071 firmware was developed in this project.”
  After: The same contribution is stated in three shorter sentences, beginning “The PCB was designed and assembled for this project.” The supplied magnetic parts remain explicitly inherited.
- Before: “With the complete supply, the response of the inherited conversion principle to a detachable, variable load could be tested.”
  After: “The inherited conversion principle could then be tested with a detachable, variable load in the complete supply.” The modal “could” remains.
- Before: “Required controller behavior is separated from the quantities to be measured in the tests.”
  After: “The functional requirements define controller behavior.” The next sentence defines the measurements needed for assessment.

Methods and results remain passive or impersonal. Circuit functions, causal relationships, definitions, and chapter descriptions use ordinary grammar. Long passive chains, indirect “is used to” constructions, vague references such as “former/latter,” and redundant restatement were reduced.

Inherited topology and magnetic design remain separate from the project's board, circuit, controller, integration, and test work. Reported and matched results remain distinct. Continuous power still requires defined-duration thermal and stability evidence. Proposed comparisons and tests retain their original modality. No figures, data, claims, citations, ratings, or later firmware features were added.

## Preservation checks

All checks against the new baseline passed:

- Every per-file numeric literal sequence, including order, is identical.
- All 599 LaTeX command invocations and adjacent braced/optional arguments are identical, including headings, labels, references, citations, and filenames.
- All 21 protected environment blocks are byte-identical, including tables, longtable, figure/TikZ, and equations.
- All 9 inline/display math blocks outside the environment comparison are identical.
- Newline types, counts, and final-newline presence are identical. The revised-plan criteria file retains LF; the other 26 files retain CRLF.
- No I/we/you or first-person prose was introduced.
- The complete thesis retains the same 467 file paths as the new baseline.

Repeated numeric power criteria and protected table/figure wording were left intact where deleting repetition would violate the fixed numeric or command sequence. No prose change required relaxing the protected macro order.

Only the assigned source files and this external note were written. No build, Git action, Code/Data/Pictures/bibliography edit, baseline edit, or global manifest edit was performed. The assigned source files are frozen for cross-review.

## Frozen source hashes

Captured UTC: 2026-10-25T17:38:41+00:00

| Path relative to `/workspace/thesis` | SHA-256 |
| --- | --- |
| `Chapters/01_Introduction/01_Motivation.tex` | `bc69e1cbe6de610c6d3bd3c3e48837d5eed61cea30cc5b79bdbfb3075e6f3f90` |
| `Chapters/01_Introduction/02_Problem_Statement.tex` | `407af044d89714fe217fa12f9207b5e41ed2b2d405619ff3abdc50d6f4a5a232` |
| `Chapters/01_Introduction/03_Aim_Objectives.tex` | `9826a2d72b1e1456602df0ed1e0d2049a02222530622effd7425d47116d0dbee` |
| `Chapters/01_Introduction/04_Research_Questions.tex` | `6ead4cdade1d3987884f90dcdc682343b05af52a96de2ba4b7e97651a7122801` |
| `Chapters/01_Introduction/05_Contributions_Attribution.tex` | `92a329964cd4025858b0fee6326d52531685460ab8c21e9ad19fe3392e6d9155` |
| `Chapters/01_Introduction/06_Scope_Limitations.tex` | `0351835b0be6f5ee7ff5f9470553322d1de0dc4cb05df5bb689dcb3f6b247d38` |
| `Chapters/01_Introduction/07_Thesis_Structure.tex` | `cb1a77b1d285a0c3d4023010c742ffb8af3c17c1e951acaa98a70bca69081cc3` |
| `Chapters/01_Introduction/chapter.tex` | `f6fc49f6927c259c572e12c57c3edc264cf9ca59044d802a5bd2e7b1c412f06a` |
| `Chapters/02_Background/01_Offline_ACDC_PFC.tex` | `25fe9b740d21a268bf3f17d4763f6072c51f6cc5d953ef257eddac34fe2b08a5` |
| `Chapters/02_Background/02_Charge_Pump_Principle.tex` | `9e2a25af5119bbee946e849838aec867fca04b2084bd28fbce96cbd9bf2cb834` |
| `Chapters/02_Background/03_ClassDE_Resonant.tex` | `ebbb8e83d7f37dff877f2bad3964afd6cbb24242d57a9701883e3bfa7ac4430c` |
| `Chapters/02_Background/04_Soft_Switching_GaN.tex` | `83b432f88e3e150186d263f425aa14caa3e4e5506250c0ba689be517c30545d6` |
| `Chapters/02_Background/05_Reference_2020.tex` | `e236a2c0244015a39cf0990611677960e3aa8a151d5beb5c6b2d013941abc0d9` |
| `Chapters/02_Background/06_Reference_2021.tex` | `05e08c92b07b8f067ac435d2cefcd33d6841c341314181cfac9609ab07d8469c` |
| `Chapters/02_Background/07_USBC_Context.tex` | `42215fa7e814d1f55beea1e59310a37ccc43ff0b93227240c210611c2f29673a` |
| `Chapters/02_Background/08_Research_Gap.tex` | `620c427ccd0e83811f8f4382c4d725df07b60480ecb49e696a9992489f1582e5` |
| `Chapters/02_Background/chapter.tex` | `c60f6827b50b7f38c96e0ff2498a686b06f19ea9f7b07c7d9d3bc6681104c05e` |
| `Chapters/03_Requirements_Architecture/01_Use_Case.tex` | `4c14d1071b5731ad5da2328d14d2887855abf9ad70e634be2ec6e1bbc5092190` |
| `Chapters/03_Requirements_Architecture/02_Electrical_Specifications.tex` | `3131c1ee7302c34b7dc9452e1e72a991ed3bcca51a45a4b73e5f0d7fb01c4b8f` |
| `Chapters/03_Requirements_Architecture/03_Functional_Requirements.tex` | `15f817a3d0edb09fa27dbcdf6bf198ab75da83ef1815ee15835250fb7aef5a1e` |
| `Chapters/03_Requirements_Architecture/04_USBC_Interface.tex` | `835a9bdd4aa45ba421e2fddceb857761ad2a9b451c949ed04892ebbedea9db08` |
| `Chapters/03_Requirements_Architecture/05_Safety_Protection.tex` | `8174cc4a8fd5e8f0621ca9dc37183bbd9eb67c5267fa43f9fa3c76da54a28687` |
| `Chapters/03_Requirements_Architecture/06_System_Architecture.tex` | `aeac5432d9b6f3f85c980a7f66409ac13538c07a82058437bba4e4d93c827b2d` |
| `Chapters/03_Requirements_Architecture/07_Operating_Modes.tex` | `9471bebc2fcaa8d5d9d4e92c81f054d8ca3c12d8c454241b41d6f827ce0326a6` |
| `Chapters/03_Requirements_Architecture/08_Verification_Matrix.tex` | `f265929040318e8aed59e20b4bbd67ded8312660181f6eedff52174ee9d5742c` |
| `Chapters/03_Requirements_Architecture/09_Revised_Plan_Criteria.tex` | `421eeb9a4082f609c2202c2c40410e48c3526c13f31185d95cf91a599c7f243b` |
| `Chapters/03_Requirements_Architecture/chapter.tex` | `aaeaa3e77f3a5752037b92ee923d9015109f6d0b5b4f718707098cfe5fb8a374` |
