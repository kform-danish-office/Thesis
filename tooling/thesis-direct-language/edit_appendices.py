from pathlib import Path
import json
root=Path('/workspace/thesis')
changes={
'Backmatter/Appendices/A_Analytical_Equations.tex':[
 ('Screening efficiency is calculated only for tests with a DC-coupled average VBUS, a load-current value, and compatible logged input power.', 'Initial efficiency estimates use tests with a DC-coupled average VBUS, load current, and a corresponding input-power reading.'),
 ('These quantities are kept separate. Absolute output voltage is taken from DC-coupled measurements.', 'Absolute output voltage is taken from DC-coupled measurements.')],
'Backmatter/Appendices/C_Firmware_Documentation.tex':[
 ('The two archived controller programs are identified in \\cref{sec:ctrl-firmware-identities}. Their PWR identifiers refer to software revisions, not hardware generations or power ratings. PWR-1.9.20 is the baseline voltage-control firmware associated with the identified final measurements.', 'Section~\\cref{sec:ctrl-firmware-identities} describes the two archived controller programs. The PWR numbers name firmware revisions. PWR-1.9.20 is the baseline voltage-control firmware; the test tables state which runs used it.'),
 ('The frozen manifest,', 'The source manifest,'),
 ('Principal firmware milestones and their meaning.', 'Firmware development milestones.'),
 ('The plan\'s V2 prototype and the later MCU firmware port are part of the same development. The hardware generation and software revision must be identified separately; moving acquisition to DMA was a software-development step, not a new board.', 'The V2 prototype and its MCU firmware port were developed together. DMA acquisition was introduced in firmware on the earlier board before the V2 hardware port.'),
 ('The port convention is introduced in \\cref{sec:intro-controller-basics}.\nThe table distinguishes logical port signals from package terminals and\nlists the assigned timer channels, ADC inputs, DMA paths, and alternate\nfunctions. Assignments are specific to each board.', 'The MCU pin names are introduced in \\cref{sec:intro-controller-basics}.\nThe table lists the MCU pins, timer channels, ADC inputs, DMA paths, and\nalternate functions for each board.'),
 ('Peripheral assignments. F410 package numbers refer to the UFQFPN48 device.', 'MCU pins and peripherals for both boards. F410 package pins use the UFQFPN48 numbering.'),
 ('Primary indication & PA0,', 'Primary voltage input & PA0,'),
 ('Primary current & PA2,', 'Half-bridge current input & PA2,'),
 ('The stated dead time is calculated from registers; gate-driver propagation and transistor switching still need measurement.', 'The programmed dead time is calculated from the timer registers. Actual gate timing still needs to be measured.'),
 ('the filters are initialized, and identity and status are printed.', 'the filters are initialized, and the firmware version and status are printed.'),
 ('The following records are required before repeat tests:', 'Before repeating a test, save the output of these commands:'),
 ('Terminal commands for saving firmware identity and configuration.', 'Commands to print the firmware version, status, and settings.'),
 ('Not every historical measurement has this complete export. Missing settings are left unspecified; source defaults are not assumed to be the test settings.', 'Some earlier tests have no complete settings export. Their missing settings remain unknown.'),
 ('Full status, version identity, or short parameter summary.', 'Full status, firmware version, or short parameter summary.'),
 ('The validated export must be saved.', 'Save the exported settings after validation.'),
 ('Function navigation for the archived V2 sketch.', 'V2 firmware functions and source lines.'),
 ('Format identity, diagnostics, units, and paste-ready configuration.', 'Print the firmware version, diagnostics, units, and paste-ready configuration.')],
'Backmatter/Appendices/E_Experimental_Data.tex':[
 ('The tables below link each completed test\nto its worksheet row and instrument readings, so each plotted point can be\ntraced to its source measurement. Blank fields mark missing measurements.', 'The tables list the worksheet row and instrument readings for each\ncompleted test. Blank fields mark missing measurements.'),
 ('Workbooks accompanying the thesis source.', 'Measurement workbooks.'),
 ('average-voltage error, screening efficiency, and the input-output power', 'average-voltage error, initial efficiency estimates, and the input-output power'),
 ('still have differing instrument readings, so their efficiencies remain\nscreening values.', 'still have differing instrument readings, which limit the accuracy of the\nefficiency estimates.'),
 ('The tables below link each completed test to its voltages, load,\npower-quality readings, firmware version, and calculation status.', 'The tables list voltages, load, power-quality readings, firmware version,\nand calculations for each completed test.')],
'Backmatter/Appendices/F_Contribution_Provenance.tex':[
 ('below credits the original designs and identifies the thesis contributions.', 'below lists the earlier designs and the work completed in this thesis.'),
 ('Attribution of the principal technical material.', 'Earlier designs and work completed in this thesis.'),
 ('Later project schematic and frozen source snapshot', 'V2 schematic and archived source'),
 ('browser protocol, and documented software checks; no transferred V1.0 performance claim', 'browser protocol, and software tests; V1.0 measurements remain from the earlier board')],
'Backmatter/Appendices/G_Software_Tools.tex':[
 ('The software supports controller builds, the V2 browser interface, and result\nreproduction.', 'The software builds the controller, runs the V2 browser interface, and\nprocesses measurements into the thesis figures.'),
 ('the archived V2 tools still require powered validation.', 'the archived V2 interface still needs testing with the powered converter.'),
 ('The frozen PWR-2.0.1', 'The archived PWR-2.0.1'),
 ('Responsibilities of the browser and serving modules in the frozen snapshot.', 'Browser application files.'),
 ('File & Responsibility and reason for the separation', 'File & Function'),
 ('Page structure, controls, status labels, and responsive layout. Presentation changes can be made without changing the UART transport.', 'Page structure, controls, status labels, and responsive layout.'),
 ('Connects UI actions to the device link, updates the chart, and manages recording. The UI displays acknowledged commands and reported device values separately.', 'Connects controls to the device link, updates the chart, records sessions, and displays command acknowledgments and device readings.'),
 (' The UI does not write UART bytes directly.', ''),
 (' Framing and validation can be tested independently of the browser page.', ''),
 ('Implements local session storage and CSV/download helpers. Recording and export do not depend on a cloud database.', 'Stores sessions locally and provides CSV and download helpers.'),
 ('Transport decisions and their implemented behavior. These are software rules, not measured electrical response times.', 'Serial commands and link handling.'),
 ('Mechanism & Implementation and purpose', 'Action & Behavior'),
 ('Correlated replies &', 'Command acknowledgments &'),
 ('Ordered changes &', 'Command queue &'),
 ('Enable interlock &', 'Enable checks &'),
 ('names, session provenance, settings, and diagnostic-current/power', 'names, session source, settings, and diagnostic-current/power'),
 ('Commands for the frozen browser tests, static build, and local server.', 'Commands to test, build, and serve the browser app.'),
 ('The frozen\ninterface can be checked', 'The archived\ninterface can be checked'),
 ('These files were present\nat source capture, but integration was incomplete.', 'Integration of these archived files was unfinished.'),
 ('The included interface is therefore incomplete and cannot be used to\ndemonstrate a working browser calculator.', 'The archived calculator page cannot run without the missing module and build entries.'),
 ('Build and MCU image-check commands for the frozen firmware source.', 'Firmware build and HEX-check commands.'),
 ('Test source included with the supporting software.', 'Software test files.'),
 ('File & Behavior exercised', 'File & Tests'),
 ('and synthetic isolation, using an in-memory serial device.', 'and separation of Demo and serial state, using an in-memory serial device.'),
 ('CSV quoting, missing fields, units, provenance, formula-like text, and empty sessions.', 'CSV quoting, missing fields, units, session source, formula-like text, and empty sessions.'),
 ('All 38 Node tests passed on the frozen source snapshot,', 'All 38 Node tests passed on the archived source,'),
 ('Powered validation must cover UART wiring and acknowledgment timing,', 'Powered tests still need to check UART wiring and acknowledgment timing,'),
 ('protection, and link-loss response. These remain outside the\nbuild, mock, and browser-Demo test scope.', 'protection, and link-loss response.'),
 ('screening\nefficiency, and input-minus-output power difference.', 'initial\nefficiency estimates, and input-minus-output power difference.'),
 ('Source and\ngenerated-output checksums, CSV data, source registers, figure\ndescriptions, and processing notes are written beside the results.\nRecord-count assertions check the processing scope, not measurement accuracy.', 'The scripts save source and\noutput checksums, CSV data, file lists, figure descriptions, and processing\nnotes beside the results. Assertions check that the expected records were processed.'),
 ('Appendix~\\ref{app:data}. Repeating the rebuild checks that\nthe processing steps can be reproduced. The original\nlimits on instrument synchronization, calibration, AC-detail\ninterpretation, and thermal dwell time still apply.', 'Appendix~\\ref{app:data}. Instrument synchronization, calibration,\nAC-coupled readings, and thermal dwell time still limit the measurements.')],
'Backmatter/Appendices/H_Full_Embedded_Source.tex':[
 ('Both complete controller files are included here. Their software identifiers and development roles are introduced in \\cref{sec:ctrl-firmware-identities}.', 'The two controller programs are listed in full below. Their development is described in \\cref{sec:ctrl-firmware-identities}.'),
 ('the browser protocol. The changes can be traced through the two files, while\nthe earlier measurements remain associated with their original code.', 'the browser protocol.'),
 ('The listings read the frozen source files directly, without omitted functions,\ncomments, or source lines.', 'The listings include every function, comment, and source line.')],
'Backmatter/Appendices/I_Full_Supporting_Source.tex':[
 ('The listings also include the frozen calculator files.', 'The listings also include the archived calculator files.'),
 ('Generated build outputs, duplicate deployment copies, third-party libraries,\nand historical intermediate sketches are not separate implementations in this\nappendix.', 'Generated build outputs, duplicate deployment copies, third-party libraries,\nand intermediate sketches are omitted.'),
 ('Calculator styling snapshot', 'Archived calculator styling'),
 ('Calculator page snapshot', 'Archived calculator page')],
'Backmatter/Appendices/J_Revised_Plan_Integration.tex':[
 ('\\section{Where the Additional Work Appears}', '\\section{Thesis Sections for the Revised Plan}'),
 ('\\caption[Revised-plan integration into the thesis.]{Integration of the revised plan into the technical chapters.}', '\\caption[Revised plan and thesis sections.]{Revised plan and corresponding thesis sections.}'),
 ('Plan work & Thesis treatment', 'Planned work & Thesis section'),
 ('Objectives and acceptance &', 'Objectives and test criteria &'),
 ('including the power levels and required completion records.', 'including power levels, tests, and design documents.'),
 ('defines the baseline repeat, measurement boundaries, staged loading, and controlled-change method.', 'describes how to repeat the baseline, measure input and output power, increase the load in stages, and change one parameter at a time.'),
 ('ranks the questions the missing tests need to resolve.', 'discusses possible causes of the power limit.'),
 ('states which records are available.', 'summarizes the available test results.'),
 ('distinguishes the V3 design-volume estimate from the outstanding complete-system power-density comparison and readiness decision.', 'reports the V3 design-volume estimate; a complete-system power-density comparison and readiness decision remain unfinished.'),
 ('Completion is assessed in Section~\\ref{sec:res-revised-plan} from the available designs and tests.', 'Section~\\ref{sec:res-revised-plan} summarizes the completed designs and available test results.'),
 ('Planned date & Required completion record', 'Planned date & Planned work')]
}
log=[]
for rel,rows in changes.items():
    p=root/rel; data=p.read_bytes(); eol='\r\n' if b'\r\n' in data else '\n'
    for old,new in rows:
        a=old.replace('\n',eol).encode();b=new.replace('\n',eol).encode()
        count=data.count(a)
        if count<1:raise RuntimeError((rel,old))
        data=data.replace(a,b)
        log.append({'path':rel,'before':old,'after':new,'count':count})
    p.write_bytes(data)
Path('/workspace/tooling/thesis-direct-language/appendices-edits.json').write_text(json.dumps(log,indent=2)+'\n')
print('Appendix prose changes:',len(log),'in',len(changes),'files')
