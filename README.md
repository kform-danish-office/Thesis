# Charge-pump PFC USB-C power supply

Current editable sources and downloads for the thesis, firmware, browser app and defense presentation.

- [Full thesis PDF](thesis/Thesis_V1_V2_V3.pdf) and [editable thesis](thesis/)
- [Defense PowerPoint](presentations/defense/Defense_Supervisor_Flow.pptx) and [PDF preview](presentations/defense/Defense_Supervisor_Flow.pdf)
- [Current firmware and web app](working-source/)
- [Local setup instructions](LOCAL_START.md)
- [Imported skills](skills/) and [build/review tooling](tooling/)
- [Sync contents and checks](SYNC_REPORT.md)

The latest defense includes the original harmonic-current graph against IEC 61000-3-2 Class A limits at the approximately 80 W USB-C operating point. The Apple charger photographs use an approximate common physical scale. Its original DTU template, speaker notes and reproducible source are in [presentation source](presentations/defense/source/).

The project target is 100 W continuous USB-C output, with a 65 W minimum. V2 direct secondary-load tests and their thermal results are kept distinct from USB-C connector output. No thermal load point reached equilibrium.

The root firmware and documentation mirror the current working copy for existing workflows. Use `working-source/` for further development. Historical releases and previous presentation downloads remain available.
