# Hardware and control wording pass

Read Chapters 07–08 and made targeted prose edits in 33 files (92 exact substitutions). The aim was to replace vague or overly compressed language with direct descriptions of the circuit and control behavior. Numbers, math, captions, labels and source commands were preserved. Original byte-level newline styles were retained. No firmware or hardware setting was changed.

Examples:
- “The driver timing is on the same scale as the programmed dead interval.” → “The driver delays are comparable to the programmed dead time.”
- “An open-frame assembly cooled by PCB copper spreading and ambient convection was tested.” → “The assembly was tested without an enclosure. Heat was spread through the PCB copper and removed by ambient convection.”
- “Acquisition was moved to DMA to separate conversion from the foreground decision.” → “ADC acquisition was moved to DMA so conversion could run independently of the foreground control loop.”
- “Timed component temperatures are still needed…” → “Component temperatures still need to be recorded over time…”

Changed files:
- `07_Hardware/01_Prototype_Overview.tex`
- `07_Hardware/02_Input_Filter_Bridge.tex`
- `07_Hardware/03_Charge_Pump_Network.tex`
- `07_Hardware/04_GaN_Half_Bridge.tex`
- `07_Hardware/05_Gate_Drive.tex`
- `07_Hardware/06_Resonant_Output.tex`
- `07_Hardware/07_USBC_Interface.tex`
- `07_Hardware/08_Sensing.tex`
- `07_Hardware/09_Protection.tex`
- `07_Hardware/10_Auxiliary_Power.tex`
- `07_Hardware/11_PCB_Layout.tex`
- `07_Hardware/12_EMI.tex`
- `07_Hardware/13_Thermal.tex`
- `07_Hardware/14_BOM_Manufacturing.tex`
- `07_Hardware/15_Unmanufactured_Revisions.tex`
- `07_Hardware/16_V2_F410.tex`
- `07_Hardware/17_V3_Edge_Card_Plan.tex`
- `08_Control_Firmware/01_Control_Objectives.tex`
- `08_Control_Firmware/02_Architecture_Timing.tex`
- `08_Control_Firmware/03_Feedback_Calibration.tex`
- `08_Control_Firmware/04_V0_Open_Loop.tex`
- `08_Control_Firmware/05_V1_Blocking_Closed_Loop.tex`
- `08_Control_Firmware/06_Blocking_Limitations.tex`
- `08_Control_Firmware/07_V2_DMA.tex`
- `08_Control_Firmware/08_Control_Law.tex`
- `08_Control_Firmware/09_Limits_Antiwindup.tex`
- `08_Control_Firmware/10_Open_Circuit_Safety.tex`
- `08_Control_Firmware/11_State_Machine.tex`
- `08_Control_Firmware/12_Fault_Handling.tex`
- `08_Control_Firmware/13_Timing_Resources.tex`
- `08_Control_Firmware/14_Version_Comparison.tex`
- `08_Control_Firmware/15_PWR_2_Port.tex`
- `08_Control_Firmware/chapter.tex`
