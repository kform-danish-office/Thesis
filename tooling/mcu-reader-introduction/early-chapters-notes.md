# Chapters 2–3 reader introduction edits

Edited seven files, adding function-first wording and short local explanations. All figure blocks, table blocks, numerical quantities, equations, labels, citations and original newline styles were preserved.

Changes:
- `02_Background/07_USBC_Context.tex`: define the USB-C sink as the connected device, describe the secondary bulk bus, and name the bulk-voltage sensing function before introducing PA1.
- `03_Requirements_Architecture/02_Electrical_Specifications.tex`: explain carrier commands and bursts in plain language; introduce PA11 as an enable pin, PA1 as secondary feedback and PA2 as primary current sensing.
- `03_Requirements_Architecture/03_Functional_Requirements.tex`: refer to the new introductory controller primer before the requirement table; explain the G071 input/enable roles, DMA and UART.
- `03_Requirements_Architecture/04_USBC_Interface.tex`: explain the USB-C socket, configuration-channel connections, and the two I2C clock/data lines; use the sensing function before PA1.
- `03_Requirements_Architecture/05_Safety_Protection.tex`: explain a latched protection state and logic-low enable inhibition; distinguish the command from discharge of stored energy; introduce PA2 by its sensing role.
- `03_Requirements_Architecture/06_System_Architecture.tex`: lead with signal functions, then pin identifiers; explain that the command pins deliver low-voltage control signals rather than load power and that ADC/DMA create and transfer readings.
- `03_Requirements_Architecture/07_Operating_Modes.tex`: explain logic high/low as switching permission before the state table and expand the controller-resource terms used in the table.

No pin assignment, carrier timing, control threshold, measured value or firmware behavior was changed. The new explanations refer to `sec:intro-controller-basics`, which the parent is adding. No build, manifest or GitHub action was performed.
