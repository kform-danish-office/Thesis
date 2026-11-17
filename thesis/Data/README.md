# Thesis data

`measurements/` retains the four supplied test workbooks and the instrument
evidence associated with the recorded tests. Planned rows are not completed
measurements.

`measurements/processed_rewrite/` contains the extracted tables used in Chapter
10 and Appendix E, processing notes, checksums, and ten unchanged raw waveform
exports. The raw waveform index records the original acquisition paths and
archived copies. Logged values and conflicting readings are preserved with
their qualifications.

`analysis/rebuild_results.py` regenerates the eight result figures and data
tables using Python, NumPy, and Matplotlib. The source project README contains
the build instructions. No raw waveform is scaled to force an expected voltage
or power.
