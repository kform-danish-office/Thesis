# Backmatter and measurement presentation review

62 exact-match proposals; source files unchanged.

## Files covered

- Backmatter/Appendices/A_Analytical_Equations.tex
- Backmatter/Appendices/B_Hardware_Documentation.tex
- Backmatter/Appendices/C_Firmware_Documentation.tex
- Backmatter/Appendices/D_Modeling_Files.tex
- Backmatter/Appendices/E_Experimental_Data.tex
- Backmatter/Appendices/F_Contribution_Provenance.tex
- Backmatter/Appendices/G_Software_Tools.tex
- Backmatter/Appendices/H_Full_Embedded_Source.tex
- Backmatter/Appendices/I_Full_Supporting_Source.tex
- Backmatter/Appendices/J_Revised_Plan_Integration.tex
- Backmatter/Backpage.tex
- Backmatter/References.tex
- Data/measurements/processed_rewrite/ac_complete_table.tex
- Data/measurements/processed_rewrite/appendix_ac_complete_table.tex
- Data/measurements/processed_rewrite/appendix_efficiency_table.tex
- Data/measurements/processed_rewrite/appendix_electrical_tables.tex
- Data/measurements/processed_rewrite/appendix_harmonic_tables.tex
- Data/measurements/processed_rewrite/appendix_thermal_complete_table.tex
- Data/measurements/processed_rewrite/appendix_thermal_tables.tex
- Data/measurements/processed_rewrite/dc_complete_table.tex
- Data/measurements/processed_rewrite/efficiency_table.tex
- Data/measurements/processed_rewrite/harmonics_complete_table.tex
- Data/measurements/processed_rewrite/measurement_appendix.tex
- Data/measurements/processed_rewrite/pq_complete_table.tex
- Data/measurements/processed_rewrite/raw_waveform_source_table.tex
- Data/measurements/processed_rewrite/record_metadata_table.tex
- Data/measurements/processed_rewrite/thermal_complete_table.tex
- Data/measurements/processed_rewrite/transient_complete_table.tex
- Data/measurements/v2_load_thermal/load_table.tex
- Data/measurements/v2_load_thermal/thermal_figures.tex
- Data/project_records/Original_Project_Definition.tex
- Data/project_records/V2_October_2026_Project_Definition.tex

## Deliberate keeps and lead review

- Complete embedded and supporting listings, their LaTeX input paths, and schematic sheets stay. Settings-journal checksums are functional and stay. Test IDs, measured quantities and sampling intervals stay. Project definitions are historical plans; preserve their technical history.
- Generated tables require the lead to synchronize the generators. The waveform interval values are sampling intervals, not total capture times; no duration was inferred. Thermal image conditions retain their identifiers.
- The browser and firmware build commands retain their working directories so they remain usable. Model table headings are updated together. Some unused generated presentation files retain source filenames and should be checked for inclusion before changing.

## Section-by-section editorial judgment

- **A, voltage nodes and ratio:** Definitions distinguish bulk and connector nodes and the reciprocal convention; keep. **Power and quality:** Equations and instrument-related limits are useful; replace workbook framing with direct calculation wording. **Regulation and ripple:** Keep the distinction between average-reading spread and instantaneous ripple. **Burst timing and protection:** Keep the board-specific enable pin, hysteresis and OVP limits; they describe actual control behavior.
- **B, tested board and PCB views:** Revision tables and photographs identify tested hardware and remain useful. **Complete schematics and V2 design:** Retain historical V1 and earlier V2 sheets, current colour V2 sheets, PCB layers and their captions. The descriptions distinguish drawings from powered tank changes without overstating fitted configuration.
- **C, firmware versions and targets:** Keep the milestone history, board-specific pin table and distinctions between measured hardware and software; remove archive inventory. **Carrier, ADC and calibration:** Keep timing, conversion equations, scan ordering and fitted-resistor uncertainty. **Execution, startup and protection:** Keep operational order, duty logic and OVP conditions; limitations are specific to behavior. **Settings journal:** Retain checksum algorithm and interruption limits because they are part of firmware operation. **UART and tuning:** Retain command reference; proposed tuning rewrite connects scan and objective. **Parameter reference:** Retain limits and compatibility fields; clarify software bounds. **Browser commands, transmit and telemetry:** Keep protocol and lease behavior and diagnostic power limitations. **Calibration and carrier timing:** Keep cancellation, physical loads, quantization and passive resonance distinctions. **Function map and build/test results:** Keep function identities, commands and limits; remove directory inventory where proposed.
- **D, circuit and magnetic models:** Preserve parameters, device differences, attribution and suggested modeling work; use Variant 1 and 2 consistent with the modeling chapter rather than filenames. Magnetic model descriptions remain as functional descriptions.
- **E, sources and calculation:** Replace source inventory with the measurement context; retain instrument disagreement, eligibility, AC coupling, ripple and thermal interpretation. **Electrical, harmonic and thermal data:** Keep measurement values and meaningful test IDs; remove image filename column. **Waveform acquisition:** Keep each record ID, count and sampling interval, removing file and hash inventory. A sampling interval is not a capture duration.
- **F, contributions:** Keep the contribution and attribution table, including the earlier DTU magnetic work, component-measurement attribution and cited topology. Descriptions are functional and do not require a rewrite.
- **G, browser architecture:** Keep UART isolation, event flow, display and signal roles; revise initial summary to include both measurement campaigns. **Framing and link loss:** Keep queue, timeout and lease limitations because they affect control behavior. **Controls and recorded sessions:** Keep operator-connected loads, calibration cancellation, timing readback and unsynchronized timestamps. **Build:** Keep executable commands and working directories, and the explicit local-server allowlist. **Calculator:** Introduce its numerical purpose; retain distinct magnetizing and leakage models. **Firmware builds and tests:** Preserve linker addresses, HEX constraints, actual test coverage and powered checks. **Measurement processing:** Replace file-location and checksum narrative with the actual calculations and uncertainty.
- **H, complete embedded source:** Keep source listings, identifiers and continuation-arrow explanation; remove line counts and manifest directions. **I, supporting source:** Keep all code listings, functional headings and captions; remove redundant path/line-count introductions and archive inventory. Build and module identifiers in operational descriptions remain useful.
- **J, revised plan and requirements:** Retain cited earlier 75 W milestone, 65 W minimum, 100 W target and unresolved 85 W point; remove external file directions. **Plan-to-thesis mapping:** Keep the references and actual planned work. **Milestones and remaining work:** Keep historical dates as project history and preserve V3 scope and unfinished density comparison.
- **Generated electrical tables:** Keep test IDs and row references, values, AC versus DC conditions and exclusions. The metadata table uses direct treatment labels while retaining the uncertain measurement boundary and blank firmware values; no revision has been inferred. Generator changes must accompany accepted presentation changes.
- **Generated harmonic and thermal tables:** Keep all measurements, thermal emissivity and reference-marker uncertainty. Both thermal table variants receive consistent filename-column removal. **V2 load/thermal tables and figure captions:** Keep seven readings, capture IDs, regions and load conditions; no revisions proposed to the numerical presentation.
- **Project-definition TeX records:** These are historical plan documents; keep their original objectives, dates and planned procedures as historical records. **Backpage and references:** No prose intervention proposed; retain citations and publication information. Measurement appendix and unused generated variants retain test IDs and values; check whether included before changing any unreferenced output.

The waveform and thermal presentation changes are exact proposals only; raw assets and source data are untouched. The metadata uncertainty wording requires generator synchronization. The output includes 68 proposals after this pass.
