# Chapters 09–10 voice polish

Frozen after a deliberate prose pass through all 28 assigned TeX files. 28 files and 74 narrative paragraphs were revised against the new immutable baseline in `/workspace/tooling/thesis-voice-polish/before`. The aim was direct, practical engineering English, with natural passive methods/results and ordinary grammar for physical relationships and definitions. No personal pronouns remain in the prose.

Representative changes:

- “The downstream output is assessed by this measurement” → “This is a measurement of the downstream output.”
- “For startup and shutdown to be measured, … are required” → “A startup and shutdown capture still needs …”
- “Areas for further investigation are shown in the images; the thermal margin would be established by that run” → “The images show where to investigate; the run would establish the thermal margin.”
- “Output power, screening efficiency, and that difference were calculated” → “Output power, an initial efficiency estimate, and the power difference were calculated.” The next sentences retain the incomplete simultaneous-acquisition and power-path evidence.
- The repeated “is documented/is retained/is assessed” constructions were replaced with concrete descriptions of the records, calculations, and missing tests where possible.

Evidence and attribution checks: efficiency and loss remain derived initial estimates, not independent loss measurements. The AC-detail spread remains distinct from instantaneous waveform ripple. Raw-export scale, calibration, and test-identification limits remain explicit. Thermal observations remain surface readings with missing duration, airflow, ambient, and stabilization evidence. No continuous rating, full ZVS verification, USB-PD qualification, protection trip test, or planned V2/V3 test is presented as completed. Author firmware changes retain “in this work”; LTspice studies retain their inherited attribution. Conditional follow-up work stays conditional. The power-density numerator still requires externally verified continuous output.

Verification passed for all 28 files: exact numeric literal sequence, inline/display math, complete protected environments, every LaTeX command and argument in sequence, headings, source references/paths, original newline styles, and final newline bytes. 69 protected environment entries (including nested table/figure environments) match the baseline byte-for-byte. Baseline hashes match the immutable manifest, and all 467 original thesis paths remain present with no added thesis paths. Only the assigned TeX files and this note were edited by this agent. No build, Git operation, data/code/image/bibliography edit, deployment, publication, or hardware action was performed.

No conflicts with protected macro order or unresolved prose/claim questions remain.

Freeze snapshot (UTC): 2026-10-25T17:37:31.617154+00:00

| Source | Changed paragraphs | Frozen SHA-256 |
|---|---:|---|
| `Chapters/09_Experimental_Methods/01_Objectives.tex` | 2 | `4bf4f69c6608846ca19625d78748f6a0139aef8c982568ad39ce1328c955fffd` |
| `Chapters/09_Experimental_Methods/02_Safety_Arrangements.tex` | 3 | `94cee7356d923f9d2ef4472dcce203b1998e5831846414810b55d810515e7087` |
| `Chapters/09_Experimental_Methods/03_Test_Bench.tex` | 3 | `e31c0f4432495608d1fc62d2cc3d80c0e8dc066268b8786f21723fe2f71a4b15` |
| `Chapters/09_Experimental_Methods/04_Instrumentation.tex` | 2 | `3a1a193364bcb43e4d5dd887b5a7e0f8efeb7ef15a99cc002a8d4e1ec6d12eb0` |
| `Chapters/09_Experimental_Methods/05_Probing.tex` | 2 | `efee88760d596d54e02a788a41867fb6ef8314b45da79e0dc58c852d9ec75e2c` |
| `Chapters/09_Experimental_Methods/06_Test_Matrix.tex` | 3 | `0636dbeb865de9df4949828801014e6102c20193ccfff54a41e15776d9f1ea4b` |
| `Chapters/09_Experimental_Methods/07_Control_Tests.tex` | 3 | `34234f95f8523c53effbca29b6226d035a0077ec1629ef7fce912aeecc817006` |
| `Chapters/09_Experimental_Methods/08_Power_Quality.tex` | 3 | `697ffd25b21ba772db95a2276daa1ef9a20496c533c124b1b9a3e3208f212c69` |
| `Chapters/09_Experimental_Methods/09_Efficiency.tex` | 3 | `857155b14665488205634b1c1ae238e9f0e99da1c52d311ecda9fdfdaaf07a28` |
| `Chapters/09_Experimental_Methods/10_Thermal.tex` | 2 | `4dcc3b516f38a38d03a3e2655795d0ab0f15c3c03e5feebecd647a60b549666c` |
| `Chapters/09_Experimental_Methods/11_Uncertainty.tex` | 2 | `2c50674d00b6ac7e70a481bd65be4eec722b3f81e7c94e004186ddad1cd4ccc4` |
| `Chapters/09_Experimental_Methods/12_Revised_Plan_Validation.tex` | 9 | `98c575d3f327f39d8749158b92b25b506c04adfc1e536e74cf36c02e76d7b601` |
| `Chapters/09_Experimental_Methods/chapter.tex` | 1 | `fb7fffbebe8e75c0e9d4c2fcf7bbc6657a00cacc7ada27c0c5669de6d483a293` |
| `Chapters/10_Results/01_Prototype_Verification.tex` | 3 | `43fd74c6f4dc69783dd031bad7d6099275d333db3997def7a7b362b2838da313` |
| `Chapters/10_Results/02_Startup_Shutdown.tex` | 2 | `f2513e149cfb92d28ee49ebe9f06d39bd224f00ed75cb5fc283377b8cb2c99e9` |
| `Chapters/10_Results/03_Steady_State.tex` | 5 | `0bb948ceb494bd1a1acc346f027fa6c06db6daaefb8f00d3034cb02187045a05` |
| `Chapters/10_Results/04_Load_Transients.tex` | 1 | `c08e10ee457317635fbfd0d3650fc29bf5ec0e467d4f607550d1841266d78caa` |
| `Chapters/10_Results/05_Open_Circuit.tex` | 1 | `227e9c6d846e24b20cde3cc68b7eba460dca1a124430d861ea4106b0cdad8241` |
| `Chapters/10_Results/06_ZVS.tex` | 2 | `6cd2e282f0a73b033c75e6c704b5a96d805281d4ba037c97fddb02fc7e3a6145` |
| `Chapters/10_Results/07_Input_Power_Quality.tex` | 4 | `c3116d03a7ac70df44bad26c64ebcea0da65e2cb7594f0bee7cee22eabe10b71` |
| `Chapters/10_Results/08_Efficiency.tex` | 5 | `845c4930d6560d40c795990495d737b49b16defdf2282b07c48407c6398d384f` |
| `Chapters/10_Results/09_Thermal.tex` | 2 | `2916311eb9d636f3ddee8b1827013dde573517ff64b210a60236293f3f6934f5` |
| `Chapters/10_Results/10_Firmware_Comparison.tex` | 2 | `b8937d4e8f61086cc58e4f590b0d6f45121ee107159c6d8ad449eb9a297c44ce` |
| `Chapters/10_Results/11_Simulation_Hardware.tex` | 2 | `0243242ea1b57797fff267ba6e4cd8a467625abcaadd240900bf73910b1f0447` |
| `Chapters/10_Results/12_Compliance_Table.tex` | 1 | `7d05f3019912fe6448603e367975d13c90f6f5e073efbb4ba709568a47732964` |
| `Chapters/10_Results/13_Failures_Lessons.tex` | 3 | `626143ab8f06470f63d385d791194d59f7bec90673a287021e631181da775776` |
| `Chapters/10_Results/14_Revised_Plan_Status.tex` | 2 | `780b0c3faf3e15eddc755de4f9fab73f6c57dc42c2d154dc02b4a8d150799c13` |
| `Chapters/10_Results/chapter.tex` | 1 | `8b126a639fbca714af7adcb70ea7379dd8b945320b1cf5c0745ca4a8ada1c283` |
