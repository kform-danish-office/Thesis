# Hardware and firmware reader introduction

Edited 21 files with 50 targeted prose additions/replacements. No firmware, settings, pin assignment, equation, source graphic, or table row was changed. One figure caption was clarified at the parent’s request. Original line endings retained through byte-based replacements.

Main changes:
- Defined the control path, MCU pins, and driver-versus-load-current distinction before hardware pin references.
- Introduced gate commands and enable by physical role before identifiers.
- Explained ADC readings, buffering and scaling, hardware timers/channels/registers, DMA routes, GPIO and UART.
- Made the G071 PA10 enable versus F410 PA10 UART receive assignment explicit.
- Replaced ambiguous expressions such as “PA1 regulates” in running prose with the reading or signal derived from the pin. The architecture caption now says the controller uses the input signals, rather than saying PA1 itself regulates. Existing TikZ geometry and table entries remain unchanged.

Changed files:
- Chapters/07_Hardware/chapter.tex
- Chapters/07_Hardware/04_GaN_Half_Bridge.tex
- Chapters/07_Hardware/05_Gate_Drive.tex
- Chapters/07_Hardware/07_USBC_Interface.tex
- Chapters/07_Hardware/08_Sensing.tex
- Chapters/07_Hardware/09_Protection.tex
- Chapters/07_Hardware/10_Auxiliary_Power.tex
- Chapters/07_Hardware/12_EMI.tex
- Chapters/07_Hardware/16_V2_F410.tex
- Chapters/07_Hardware/17_V3_Edge_Card_Plan.tex
- Chapters/08_Control_Firmware/chapter.tex
- Chapters/08_Control_Firmware/01_Control_Objectives.tex
- Chapters/08_Control_Firmware/02_Architecture_Timing.tex
- Chapters/08_Control_Firmware/03_Feedback_Calibration.tex
- Chapters/08_Control_Firmware/04_V0_Open_Loop.tex
- Chapters/08_Control_Firmware/08_Control_Law.tex
- Chapters/08_Control_Firmware/09_Limits_Antiwindup.tex
- Chapters/08_Control_Firmware/10_Open_Circuit_Safety.tex
- Chapters/08_Control_Firmware/11_State_Machine.tex
- Chapters/08_Control_Firmware/12_Fault_Handling.tex
- Chapters/08_Control_Firmware/15_PWR_2_Port.tex

Preservation check passed for all 21 edited files: SI/number quantities, inline/display math, labels and source graphic references match the baseline. DTG is described as a timer field, not a standalone register. Source edits are complete and frozen. No build, manifest update or GitHub action was performed.
