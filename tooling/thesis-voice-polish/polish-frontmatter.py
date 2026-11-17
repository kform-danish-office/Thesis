from pathlib import Path

root = Path('/workspace/thesis')
edits = {
    'Frontmatter/Abstract.tex': [
        ('The main control problem was the energy remaining in the resonant path and capacitors when demand disappeared. Regulation under load and limited further charging at no load were required.',
         'The main control problem was the energy left in the resonant path and capacitors after the load was disconnected. The secondary voltage had to be regulated under load, and further charging limited at no load.'),
        ('The isolated secondary bulk bus is regulated by the final PWR-1.9.20 controller, limited precharge is used while feedback starts, and different duty limits are applied under load and at no load.',
         'The isolated secondary bulk bus was regulated using the final PWR-1.9.20 controller. Limited precharge was used while feedback became available, with separate duty limits under load and at no load.'),
        ('measurements were used to obtain output powers', 'measurements were used to calculate output powers'),
        ('A screening efficiency of', 'An initial efficiency estimate of'),
        ('is calculated from the input--output pairs; uncertain timing and calibration limit the accuracy of that estimate.',
         'was calculated from the paired input and output measurements. Uncertainty in their timing and calibration limits the accuracy of this estimate.'),
        ('Controller operation through the tested no-load and load-removal events is documented in the captures.',
         'Controller operation was recorded during the tested no-load and load-removal events.'),
        ('The next priorities are to measure losses, improve heat removal, and test protection timing.',
         'Next, losses need to be measured, heat removal improved, and protection timing tested.'),
        ('A V2 retest, diagnosis of the power shortfall, and a V3 edge-card design are called for in the revised July--October plan. A common method for comparing power density is also called for. Powered V2 characterization and the V3 comparison remain open.',
         'A V2 retest, investigation of the power shortfall, and a V3 edge-card design are required by the revised July--October plan. Power density is to be compared using the same method for both revisions. Powered V2 characterization and the V3 comparison remain to be completed.'),
        ('Thermal and stability tests of defined duration are required for either rating.',
         'Before either can be claimed as a continuous rating, thermal and stability tests must be run for a defined duration.'),
    ],
    'Frontmatter/Approval.tex': [
        ('A charge-pump PFC resonant converter was built into a USB-C laboratory power supply, and the controller needed for operation with a detachable load was developed.',
         'A USB-C laboratory power supply was built around a charge-pump PFC resonant converter. Its controller was developed for operation with a detachable load.'),
        ('The schematic and PCB were implemented, the supplied magnetics were integrated, the STM32 firmware was developed, and the prototype was brought up and tested as part of this project.',
         'In this project, the schematic and PCB were implemented, the supplied magnetics were integrated, and the STM32 firmware was developed. The prototype was then brought up and tested.'),
        ('The isolated secondary bulk bus is regulated by the controller. The USB-C output stage sits downstream, so the feedback voltage and connector voltage have different roles. That distinction runs through the hardware, firmware, and measurement chapters: each signal must be used for the quantity actually measured.',
         'The isolated secondary bulk bus is regulated by the controller. The USB-C output stage sits downstream, so the feedback voltage and connector voltage describe different points in the circuit. This distinction matters in the hardware, firmware, and measurements: each signal must be used for the quantity it actually represents.'),
        ('The later V2 F410 implementation, browser logging, and software tools are also documented, with the full source in the appendices. The controller development is extended through this work. Software checks and remaining powered tests are described alongside the measured baseline.',
         'The later V2 F410 implementation, browser logging, and software tools are also described, with the full source in the appendices. These additions extend the controller work. Completed software checks and powered tests still needed are reported alongside the measured baseline.'),
        ('In the revised July--October 2026 plan, the next stage is defined: the reported V2 baseline is to be repeated, the power limit identified, controlled changes tested, and a V3 edge-card design assessed.',
         'The next stage is set out in the revised July--October 2026 plan: the reported V2 baseline is to be repeated, the power limit identified, controlled changes tested, and a V3 edge-card design assessed.'),
        ('the planned milestones are connected to the technical chapters. The completed hardware, development changes, test findings, and remaining work are documented in this thesis.',
         'each planned milestone is linked to the relevant technical chapters. The completed hardware, design changes, test results, and remaining work are described in this thesis.'),
    ],
    'Frontmatter/Acknowledgements.tex': [
        ('The supervision and technical guidance provided by Ahmed Ammar and Michael A. E. Andersen are gratefully acknowledged. Support from the DTU laboratory staff and technical personnel during construction and high-voltage testing is also acknowledged, along with practical advice from colleagues and fellow students.',
         'Thanks are due to Ahmed Ammar and Michael A. E. Andersen for their supervision and technical guidance. The help provided by DTU laboratory staff and technical personnel during construction and high-voltage testing is also appreciated, as is the practical advice from colleagues and fellow students.'),
    ],
    'README.md': [
        ('Methods, results, and project actions are reported in passive or impersonal\r\nform, with concise wording and factual claims. Proposed tests retain conditional\r\nwording. Quotations and frozen source listings retain their original text.',
         'Methods, results, and project actions are reported in natural passive or\r\nimpersonal form. Use short, concrete sentences and familiar engineering terms.\r\nKeep definitions and circuit behavior direct; avoid forced passive sentences,\r\nvague claims, and repeated statements about what the document contains.\r\nProposed tests retain conditional wording, and estimates remain distinct from\r\nmeasurements. Quotations and frozen source listings retain their original text.'),
    ],
}

for relative, pairs in edits.items():
    path = root / relative
    text = path.read_bytes().decode('utf-8')
    for old, new in pairs:
        assert text.count(old) == 1, (relative, old)
        text = text.replace(old, new)
    path.write_bytes(text.encode('utf-8'))
    print(relative, len(pairs), 'deliberate edits')
