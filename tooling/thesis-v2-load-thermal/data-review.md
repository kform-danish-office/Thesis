# Independent V2 secondary-load data review

Input power is the AC supply recorded real power; output power is the electronic load voltage multiplied by its current, matching the recorded load power. Efficiency is output power / input power, and input minus output is the estimated combined loss between these measurement points. Values are snapshots.

| Capture | AC V | AC A | Input W | Load V | Load A | Load W | Efficiency % | Input − output W | Bridge R3 °C | Secondary R1 °C |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Capture 015.csv | 240.00 | 0.29 | 64.35 | 26.14 | 1.86 | 48.68 | 75.7 | 15.67 | 65.1 | 50.3 |
| Capture 017.csv | 239.99 | 0.39 | 95.14 | 21.36 | 3.31 | 70.75 | 74.4 | 24.39 | 83.9 | 57.2 |
| Capture 018.csv | 240.00 | 0.45 | 106.73 | 20.07 | 4.29 | 86.17 | 80.7 | 20.56 | 68.2 | 59.7 |
| Capture 019.csv | 239.99 | 0.54 | 121.90 | 18.46 | 5.27 | 97.35 | 79.9 | 24.55 | 73.2 | 69.4 |
| Capture 020.csv | 240.01 | 0.66 | 140.565 | 16.87 | 6.51 | 109.87 | 78.2 | 30.70 | 74.5 | 81.6 |
| Capture 021.csv | 240.00 | 0.84 | 168.86 | 14.92 | 8.51 | 127.05 | 75.2 | 41.81 | 75.6 | 88.7 |
| Capture 022 (2).csv | 239.97 | 0.98 | 189.18 | 13.69 | 10.01 | 137.08 | 72.5 | 52.10 | 73.7 | 98.3 |

All seven AC rows report 50 Hz and approximately 240 V. Load voltage falls from 26.14 V to 13.69 V as current increases from 1.86 A to 10.01 A; output power reaches 137.08 W at the final capture. Estimated efficiency peaks at 80.7% in capture 018 and declines to 72.5% at the final capture. These are secondary-output measurements, not USB-C output measurements or continuous ratings. The user confirms none of these tests reached thermal stability.

Bridge R3 reaches 83.9 °C at 70.75 W output and is 73.7 °C at 137.08 W; secondary R1 rises from 50.3 °C to 98.3 °C across the sequence. Region emissivity is 0.95; the thermal display footer separately shows 0.97. The observed bridge trend does not identify its cause; diode selection and related design need further work.

The camera clock times in the transcribed sequence pair in order with the seven CSV captures if a one-hour clock offset is assumed. After adding one hour to each CSV time, captures follow the displayed image times by 2.673175–4.240071 s. This is consistent with the proposed pairing but does not establish clock synchronization or simultaneous acquisition. The sequence does not establish duration at any load point.

Consistency check: capture 017 reports 95.142 W input, while its displayed 239.99 V and 0.39 A give 93.60 VA and a calculated power factor of 1.0165. This exceeds unity and is not explained by rounding the displayed current to the nearest 0.01 A alone; the source readings or acquisition timing require checking. Use the recorded real power for the stated efficiency estimate, and avoid presenting a power factor for this point. The remaining calculated power factors are below unity. All electronic-load power values exactly match the product of their recorded voltage and current to floating-point precision.

Decimal arithmetic independently confirms the listed load powers and efficiency ratios; rounding output power to two decimal places with half-up rounding gives 48.68, 70.75, 86.17, 97.35, 109.87, 127.05 and 137.08 W. The capture 020 input power is 140.565 W as recorded, or 140.57 W rounded half-up to two decimals. Exact capture timestamps and all seven clock differences are retained in the JSON summary.
