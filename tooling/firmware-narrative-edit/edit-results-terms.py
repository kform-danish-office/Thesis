from pathlib import Path
r=Path('/workspace/thesis');changes=[]
def replace(name,a,b):
 p=r/name;raw=p.read_bytes();x=a.encode();y=b.encode()
 if x not in raw:x=x.replace(b'\n',b'\r\n');y=y.replace(b'\n',b'\r\n')
 elif b'\n' not in x and b'\r\n' in raw:y=y.replace(b'\n',b'\r\n')
 assert raw.count(x)==1,(name,a[:100],raw.count(x));p.write_bytes(raw.replace(x,y));changes.append(name)
replace('Chapters/10_Results/01_Prototype_Verification.tex',r'\begin{table}[htbp]',r'''The identified final records used the baseline voltage-control firmware.
The high-load record used an earlier revision, while several intermediate-
voltage records do not identify a revision. The configurations are listed
in Table~\ref{tab:prototype-identity}; the software stages are explained in
\cref{sec:ctrl-firmware-identities}.

\begin{table}[htbp]''')
replace('Chapters/10_Results/07_Input_Power_Quality.tex','with PWR-1.9.10 listed as the firmware.',r'with an earlier firmware revision identified in Table~\ref{tab:prototype-identity}.')
replace('Chapters/10_Results/10_Firmware_Comparison.tex','PWR-1.9.20 & Loaded averaged duty','Final voltage control & Loaded averaged duty')
replace('Chapters/10_Results/12_Compliance_Table.tex','Circular ADC DMA in PWR-1.9.20; live timing logs incomplete','Circular ADC DMA in the baseline firmware; live timing logs incomplete')
replace('Chapters/10_Results/14_Revised_Plan_Status.tex','on the V1.0 assembly with PWR-1.9.20.','on the V1.0 assembly with the baseline voltage-control firmware.')
replace('Chapters/10_Results/14_Revised_Plan_Status.tex','assembly or the later integrated V2 implementation with PWR-2.0.1.','assembly or the later integrated V2 design and its controller port.')
replace('Chapters/11_Discussion/03_Control_Contribution.tex','In PWR-1.9.20, the voltage loop','In the baseline firmware, the voltage loop')
replace('Chapters/12_Conclusion/03_Contributions.tex','PWR-1.9.20 was developed around continuous DMA acquisition,','The baseline voltage-control firmware was developed around continuous DMA acquisition,')
replace('Chapters/12_Conclusion/03_Contributions.tex','settings journal and PWR-2.0.1 browser commands and logging were','settings journal, browser commands, and logging were')
replace('Backmatter/Appendices/A_Analytical_Equations.tex','In PWR-1.9.20, loaded-duty averaging,','In the baseline firmware, loaded-duty averaging,')
replace('Backmatter/Appendices/B_Hardware_Documentation.tex','STM32G071RBT6 and the final PWR-1.9.20 firmware family','STM32G071RBT6 and the final voltage-control firmware')
replace('Backmatter/Appendices/F_Contribution_Provenance.tex','V2 MCU hardware and PWR-2.0.1 software','V2 MCU hardware and controller port')
replace('Backmatter/Appendices/J_Revised_Plan_Integration.tex','V2 includes the MCU/PWR-2 development;','V2 includes the integrated MCU and the ported control firmware;')
Path('/workspace/tooling/firmware-narrative-edit/results-terms-notes.md').write_text('''# Results and conclusion terminology\n\nSimplified casual firmware identifiers in Chapters 10–12 and Appendices A/B/F/J. Descriptive baseline voltage-control firmware and V2 controller-port wording now carry the narrative. The exact identifiers remain in the test-configuration table, where the baseline final records, earlier high-load revision and unidentified intermediate-voltage records are distinguished. The input-power-quality discussion points to that table rather than repeating a version string.\n\nNo software revision has been merged with another. The V2 trial remains separately identified with its unrecorded firmware version. Numerical quantities, mathematics, raw files, firmware/code, labels, citations, and source paths are unchanged. The new introduction to the measurement-configuration table references the parent’s sec:ctrl-firmware-identities explanation.\n\nEdited files:\n'''+''.join('- '+name+'\n' for name in sorted(set(changes))))
print(len(set(changes)),'files edited; exact record identifiers retained in the configuration table')
