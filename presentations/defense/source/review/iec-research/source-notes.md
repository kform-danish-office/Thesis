# IEC 61000-3-2 source notes for the APEC harmonic-current figure

The original APEC digest identifies Fig. 3(e) as a Class A screen of harmonic-current magnitudes at a 240 V AC, 50 Hz supply and 80 W output. Its text gives PF 0.99 and current THD approximately 4%. The figure compares a measured operating point against limits. Treat it as a comparison, not a declaration of full compliance.

## Equipment classification

IEC 61000-3-2:2018, edition 5, clause 5.1, p. 12 says: “Equipment not specified as belonging to Class B, C or D shall be considered as Class A equipment.” Class D comprises specified types of personal computers and their monitors, television receivers, and refrigerators/freezers with variable-speed compressor drives, with specified power up to 600 W. A general-purpose standalone USB-C supply is therefore reasonably screened against Class A; actual conformity classification and test configuration depend on the final equipment and intended use.

Source: [IEC 61000-3-2:2018 public preview](https://cdn.standards.iteh.ai/samples/22247/bdec75030c3c4f82af83aa4fb86bb1d8/IEC-61000-3-2-2018.pdf), local `iec-61000-3-2-2018-preview.pdf`, pp. 11–13.

## Class A limits

The limits are RMS harmonic currents at orders n from 2 to 40. For odd n: n=3, 2.30 A; 5, 1.14 A; 7, 0.77 A; 9, 0.40 A; 11, 0.33 A; 13, 0.21 A; and n=15–39, 0.15×15/n A. For even n: n=2, 1.08 A; 4, 0.43 A; 6, 0.30 A; and n=8–40, 0.23×8/n A.

Source: [EPSMA Guide to EN 61000-3-2:2014](https://www.epsma.org/wp-content/uploads/2021/01/PFC-Guide_03032018-3-final-7-7.pdf), Table 1, p. 13; local `epsma-pfc-guide-2018.pdf`. An independent published [test report](https://ae-pic-a1.aliexpress-media.com/kf/S5ef6f547ef6f4f22ab165bf463def202U.pdf), pp. 16–17, gives the same values and formulae and labels the test standard EN IEC 61000-3-2:2019+A1:2021; local `example-test-report-2019-a1-2021.pdf`. The publicly accessible 2018 IEC preview identifies Table 1 but does not expose its numerical entries; the independent later-edition report is evidence for the numbers rather than the normative text itself.

## Edition and test qualification

[IEC publication record](https://webstore.iec.ch/en/publication/92799) lists IEC 61000-3-2:2018+A1:2020+A2:2024 as the published consolidated edition 5.2. The present source check has not verified the full 2024 normative text, so retain the digest's cited IEC 61000-3-2:2018 reference and do not claim a current-edition certification from the figure.

EPSMA's 2014-edition guide places the general non-lighting exemption at rated power ≤75 W, subject to the standard's categories. Do not treat 75 W as a universal operating-point threshold, nor as requiring a particular power factor or PFC topology. A conformity verdict would require the applicable class, conditions, instrument, observation and averaging rules, and all required operating modes to be established.
