from pathlib import Path
root=Path('/workspace/thesis')
changes={
'Chapters/02_Background/07_USBC_Context.tex':[
('The USB-C output adds a second regulation stage. The interface and configuration determine the voltage offered to the sink and the negotiation behavior.', 'The USB-C output adds a second regulation stage. The interface and configuration determine the voltage offered to the connected device, called the sink, and how that voltage is negotiated.'),
('The isolated resonant stage in the prototype feeds a secondary bulk bus.', 'The isolated resonant stage in the prototype feeds the secondary bulk bus: the rectified transformer-output supply before the USB-C regulator.'),
('PA1 provides bulk-voltage feedback for STM32 control.', 'The bulk-voltage sensing input, identified as PA1 on the STM32 microcontroller, provides the feedback used to control this upstream supply.'),
],
'Chapters/03_Requirements_Architecture/02_Electrical_Specifications.tex':[
('The carrier sets the switching-cycle duration. The burst frequency sets how often groups of cycles can be enabled, while the control period sets how often feedback is evaluated and the command updated.', 'The carrier is the repeating command that times the power switches. Bursts are groups of these switching cycles, separated by intervals when transfer is inhibited. The burst frequency sets how often a group can be enabled, while the control period sets how often the sensor readings are evaluated and the command updated.'),
('whose enable output is PA11.', 'whose power-stage enable output is assigned to pin PA11.'),
('PA1 measures that upstream bulk voltage, so its setpoint is not the selected connector voltage. PA2 provides primary half-bridge current information for load classification; it does not measure connector current.', 'The upstream bulk voltage is measured through the secondary-feedback input (PA1), so its setpoint is not the selected connector voltage. The primary-current sensing input (PA2) provides information about the half bridge for load classification; it does not measure current at the USB-C connector.'),
],
'Chapters/03_Requirements_Architecture/03_Functional_Requirements.tex':[
('The identifiers link each requirement to its assessment in the results summary.', r'''The identifiers link each requirement to its assessment in the results summary.

The pin notation and controller functions are introduced in \cref{sec:intro-controller-basics}. In the G071 implementation below, the power-stage enable output (PA10) permits or stops bursts, while the secondary-voltage input (PA1) supplies the main feedback reading. The other two sensor inputs measure primary voltage (PA0) and primary half-bridge current (PA2). Direct memory access (DMA) transfers the converted readings into memory without a separate software copy for each sample. The universal asynchronous receiver-transmitter (UART) provides the serial connection used to exchange commands and status with a computer.'''),
],
'Chapters/03_Requirements_Architecture/04_USBC_Interface.tex':[
('Its output feeds \\texttt{USB\\_PD\\_OUT} and connector J1 VBUS. CC1/CC2 connect to the interface controller, alongside the data-line and protection connections.', 'Its output feeds \\texttt{USB\\_PD\\_OUT} and VBUS at the USB-C socket, J1. CC1 and CC2 are the connector\'s configuration-channel lines, used by the interface controller to detect attachment and support power negotiation. They are distinct from the connector\'s power contacts and data lines.'),
('The output section has local input and output capacitance, current sensing, VBUS and signal protection, and an I2C header on \\texttt{PD\\_SCL}/\\texttt{PD\\_SDA}.', 'The output section has local input and output capacitance, current sensing, and VBUS and signal protection. An I2C service header provides a two-wire communication connection: \\texttt{PD\\_SCL} carries the clock and \\texttt{PD\\_SDA} carries data.'),
('The secondary bulk voltage is regulated by the STM32 through PA1.', 'The secondary bulk voltage is regulated using the STM32\'s secondary-voltage sensing input, PA1.'),
],
'Chapters/03_Requirements_Architecture/05_Safety_Protection.tex':[
('Outside the allowed conditions, OVP is latched and PA10 is held low until the defined clear or reset action.', 'Outside the allowed conditions, overvoltage protection (OVP) is latched: the stop condition remains active until the defined clear or reset action. The power-stage enable output (PA10) is held at logic low, the digital state that inhibits switching bursts. This command does not discharge energy already stored in the capacitors.'),
('PA2 provides load classification and diagnostics.', 'The primary half-bridge-current sensing input (PA2) is used for load classification and diagnostics.'),
],
'Chapters/03_Requirements_Architecture/06_System_Architecture.tex':[
('The STM32G071 provides complementary PA8/PA9 carrier commands and controls average transfer through PA10 burst enable. PA0 supplies primary-voltage information, PA1 secondary-voltage feedback, and PA2 half-bridge current information. The latest samples are made available through free-running DMA without blocking the control loop. Sampling is not synchronized to each carrier cycle.', 'The STM32G071 produces the complementary switching commands at the carrier outputs, PA8 and PA9. Average transfer is controlled through a separate burst-enable output, PA10. These pins carry low-voltage commands to the gate driver; they do not carry the load power. The sensor inputs provide primary-voltage information (PA0), secondary-voltage feedback (PA1), and primary half-bridge-current information (PA2). Their voltages are converted into numerical readings by the analog-to-digital converter. DMA transfers those readings into memory while the scan continues, without blocking the control loop. Sampling is not synchronized to each carrier cycle.'),
],
'Chapters/03_Requirements_Architecture/07_Operating_Modes.tex':[
('Table~\\ref{tab:req-states} shows how the final firmware separates those tasks.', r'''The digital enable output is the controller's permission for the power stage to switch: logic high permits a burst and logic low inhibits it. In the G071 implementation, this output is PA10. The table also names general-purpose input/output (GPIO), which is the configurable pin interface; UART, which exchanges serial commands; and the analog-to-digital converter (ADC), whose readings are transferred by DMA.

Table~\ref{tab:req-states} shows how the final firmware separates those tasks.'''),
],
}
for relative, pairs in changes.items():
    path=root/relative
    raw=path.read_bytes()
    for old,new in pairs:
        a=old.encode();b=new.encode()
        if a not in raw:
            a=a.replace(b'\n',b'\r\n');b=b.replace(b'\n',b'\r\n')
        elif b'\n' not in a and b'\r\n' in raw:
            b=b.replace(b'\n',b'\r\n')
        assert raw.count(a)==1,(relative,old[:100],raw.count(a))
        raw=raw.replace(a,b)
    path.write_bytes(raw)
print('Edited',len(changes),'files; figures/tables left unchanged')
