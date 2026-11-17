# Speaker notes

25-minute speaking allocation, with four backup slides. Timing is an estimate for rehearsal.

## 1. Design and Implementation of a High-Frequency Charge-Pump PFC Resonant Converter for a USB-C Power Supply
*00:00–00:45*

This thesis covers the design and implementation of a USB-C power supply using a high-frequency charge-pump power-factor-correction resonant converter. The aim is a compact supply for a device whose demand can change during operation. The design target is 100 watts continuous, with a 65-watt continuous minimum. A device may be absent at startup, connected later, or removed while energy remains in the converter. The supply therefore needs to control transferred power across changing load conditions.

The range of USB-C adapters illustrates the different power and voltage demands behind this design.

## 2. More power from a compact USB-C adapter
*00:45–02:10*

These adapter examples show the range of power and devices served by USB supplies. The 5 W adapter is a USB power adapter, while the 20 W and 140 W examples use USB-C. The adapter bodies are shown at approximately the same scale; the photographs use different viewing angles. Higher-power devices still need an adapter that is practical to carry and use, so compactness matters alongside power delivery. USB Power Delivery selects an output voltage for the connected device. Demand can also change during operation: a device may be connected after startup, removed, or draw little power while attached. The supply must respond to these changes while maintaining the required output. For this project, the target was 100 W continuous output, with a minimum of 65 W continuous. These are design objectives for the USB-C power supply. Delivering that power in a compact converter makes both component size and heat important.

Higher switching frequency can reduce the size of the passive components, but it also makes switching heat a more demanding problem.

## 3. High frequency makes switching loss a design constraint
*02:10–04:05*

The adapter examples show a broad range of output power and voltage. For a compact supply, switching faster can reduce the energy that has to be transferred in each cycle at a given power. That allows the magnetic components and capacitors to be designed smaller, although their losses and parasitics still constrain the design.

There is a cost to increasing frequency. Each switching cycle dissipates some energy in the devices. At comparable energy per cycle, the switching loss rises approximately in proportion to frequency, so heat becomes a constraint in a small enclosure.

The resonant branch addresses the turn-on part of that loss. During dead time, current charges and discharges the switch-node capacitances and moves the node toward the target rail. If enough current flows in the required direction to complete the transition before the incoming switch turns on, its voltage is near zero at turn-on. In the actual circuit, both the pump and resonant branches contribute current at the shared node, and their directions matter.

The demand from a USB-C device can change or disappear, so efficient switching alone is not enough. Average energy transfer must also be adjusted to maintain the secondary bulk voltage.

The selected circuit combines those functions around one shared half bridge and adds the USB-C output stage.

## 4. One half bridge drives both power paths
*04:05–06:30*

The chosen supply combines current shaping and isolated power transfer around one GaN half bridge. Following the power path from the AC input, the input bridge feeds the charge pump, which transfers charge to the high-voltage-link capacitor, C_DC. Its switching action gives an input-current envelope that follows the rectified line voltage, without a separate PFC current-control loop. The link buffers the difference between pulsating input power and secondary demand.

The half bridge is supplied by that link. Its switch-node voltage, V_SW, excites both the charge pump and the resonant path. The resonant tank transfers energy through the transformer, and the secondary rectifier supplies C_DC1, the secondary bulk capacitor. The USB-C Power Delivery stage then regulates the selected connector voltage from that bulk supply.

The secondary bulk voltage is sent across the isolation barrier to the MCU. The MCU regulates it by enabling groups of switching cycles, so both power paths respond to the same switching activity. In this project the power stage was integrated with sensing, local supplies and the USB-C output; the secondary-voltage burst control was developed and the prototypes tested. The charge-pump topology and design method were developed by Ammar and colleagues in earlier DTU work. The planar magnetics were supplied from earlier DTU work by Bima Nugraha Sanusi and the DTU Power Electronics group.

The charge pump shows how that shared switching action shapes the input current.

## 5. Charge transfer shapes the input current
*06:30–08:40*

The input bridge feeds the charge pump at the left. The rectified input connects to one side of C p and through D p to the high-voltage link, shown here as C DC and V DC. The half bridge, Q high side and Q low side, moves the switch node V SW between the link rails. L p connects that switching node to the other side of C p and the two clamp diodes D C1 and D C2. During an enabled cycle, the input bridge supplies charge to C p through the inductor and steering paths. In the ideal sequence, charging continues until the capacitor voltage reaches approximately the instantaneous rectified input voltage. On the following part of the cycle, stored capacitor energy transfers towards the high-voltage link through the steering path. The clamp diodes hold the pump node at the link rails as the inductor current approaches zero. The pump inductor sets the current slope and helps set how long the excursion takes. For a complete excursion, the input charge taken in one enabled cycle is approximately C p times the rectified line voltage. Averaging those charge packets over many switching cycles gives the current envelope shown. Here f s is the switching frequency, C p is the pump capacitance, and v rec is the instantaneous rectified line voltage. The factor b is the local fraction of enabled cycles. If that fraction is constant over the line cycle, the ideal input-current envelope follows the rectified voltage. This is inherent current shaping without a separate PFC current-control loop. The enabled fraction can vary with line phase, and finite current and clamp timing affect the actual transfer, so the final power factor depends on both the circuit and its control.

That same switching action also drives the transformer and affects half-bridge commutation.

## 6. Resonant transfer and shared-node commutation
*08:40–10:45*

The charge pump shapes the input current, but the same switching node also drives the isolated power path. Starting at the half-bridge switching node, whose voltage is marked V_SW, follow the series capacitor C_RES and inductance L_RES to the transformer primary. The series tank inductance combines transformer leakage and the added inductance in the original tank calculation. Those values placed the estimated resonance close to the nominal one megahertz carrier. The transformer transfers energy across the isolation barrier, and the secondary rectifier charges the bulk supply feeding the USB-C stage.

Now return to the half bridge. During dead time both switches are commanded off, and current moves the switch-node voltage by charging and discharging the associated capacitances. The relevant current is the signed sum of the pump and primary resonant currents at the shared node. Depending on their directions, the two currents can help each other or oppose each other. The available commutation current therefore changes with load, line phase, and the state of the tank when a burst restarts. Its direction and magnitude need to move the node in the available interval; the resonant current alone is not enough to describe the transition.

The carrier sets the fast energy-transfer cycle. The amount of switching must still follow the power demanded at the output.

That is the role of the burst controller: it regulates the secondary bulk supply by adjusting how much of the carrier is enabled.

## 7. Burst control regulates the secondary bulk
*10:45–13:10*

The resonant path transfers energy while the half bridge switches, but the required average transfer changes with the connected device. The MCU therefore regulates the secondary bulk voltage using the feedback path shown across the top. The bulk voltage is measured across the isolation barrier and passed to the MCU. The MCU adjusts the burst-enable command to the half bridge, closing the loop through the converter.

The yellow trace is the measured switch-node voltage at a 5 volt, 3 ampere USB-C output point. The flat region on the left is an idle interval; the repeated transitions form a switching packet. Within an enabled packet, the nominal carrier is 1 megahertz. Increasing the fraction of enabled cycles increases average excitation and energy transfer; reducing it gives the converter less time to transfer energy. The controller uses the secondary voltage to adjust that fraction as demand changes. The bulk supply then feeds the USB-C power-delivery stage, which regulates the selected connector voltage.

The control implementation was developed around secondary-voltage feedback. Earlier ADC reads blocked the foreground while each conversion completed, sharing time with control and communication. Circular direct memory access, or DMA, moves the voltage and current samples to memory in the background, so the control loop can use available readings without waiting for each conversion. During startup, limited packets and settling intervals energize the isolated feedback circuit. At low load or after a device is removed, duty limits reduce continued charging of the bulk capacitor. These bounds support the voltage loop as the available load changes.

The burst view shows when the half bridge is enabled. A closer time scale shows the individual carrier cycles within a packet.

## 8. V1 switching near 1 MHz
*13:10–14:45*

The previous capture showed how switching is grouped into bursts to regulate the secondary supply. This view looks at the faster switching cycles during an active interval. The USB-C voltage was set to 20 volts and the electronic load to 4.7 amps. Yellow is the half-bridge switch node, which drives both the charge-pump and isolated resonant branches. Across the ten-microsecond window, about ten cycles are visible, giving a switching frequency close to one megahertz. The switch-node waveform alternates between its high and low levels on each cycle. Green is the secondary bulk voltage and blue is USB-C VBUS. Both output channels are AC-coupled, so their displayed positions should not be read as DC output levels. The capture shows the switching waveform at the carrier timescale. Gate timing is not shown, so the voltage at turn-on cannot be read from this view.

Connector-voltage measurements then show how the supply delivered power across the USB-C settings.

## 9. USB-C output stays close to the selected voltage
*14:45–16:05*

The carrier capture shows that the converter is switching under load. These DC measurements show what the supply delivered at the USB-C connector. The MCU regulated the secondary bulk supply feeding the USB-C Power Delivery stage, and that stage regulated the connector to the selected voltage. The four series show fixed settings of five, nine, fifteen and twenty volts. Each marker is the average connector-voltage error at a measured current. The largest absolute error was 0.583 percent at five volts and one ampere. At the highest recorded DC point, the measured average was 19.9732 volts at four amperes, giving 79.89 watts at the connector.

The input-to-connector power balance shows the heat cost of delivering that output.

## 10. Efficiency and heat at 79.89 W
*16:05–17:20*

At the 20 volt, 4 ampere connector point just shown, the average USB-C voltage was 19.9732 volts. Multiplying voltage by current gives 79.89 watts delivered at the connector. The logged input power was 104.42 watts, so the input-to-connector efficiency estimate is 76.51 percent.

The input–output difference is nearly 24.53 watts at this operating point. This is the overall difference across the supply; it does not identify the loss of any one component. The heat associated with conversion matters when the supply is made compact, because less space is available to spread and remove it. It also matters for continuous power: a point that can be reached electrically must still be sustained at an acceptable temperature.

The input-current harmonics can also be compared with the IEC limits at this operating point.

## 11. Input harmonics at the 80 W operating point
*17:20–18:50*

At the 80-watt USB-C operating point, the input readings gave a power factor of 0.99 and current THD of 3.98 percent. The blue bars show the individual input-current harmonics, and the orange curve shows the IEC 61000-3-2 Class A limits for each harmonic order. The vertical scale is logarithmic. The shown harmonic components are below the Class A limits at this point. Class A is the reference used for this general-purpose supply. The standard limits each harmonic current; power factor and THD summarize input quality. The 3.98 percent is the logged screen value; the harmonic table from a separate capture gives 4.53 percent when reconstructed. This comparison covers one operating point, rather than a full IEC test. The charge pump shapes the average input-current envelope, while variation in burst density over the line cycle can change its shape.

The V1 thermal image shows where heating became severe under load.

## 12. V1 magnetics heating at high load
*18:50–19:35*

The thermal image shows how strongly the V1 hardware heated at the higher load setting. At the labeled 20 volts and 4.7 amperes, the camera recorded a maximum surface temperature of 102.9 degrees Celsius near the magnetics. The image is a surface-temperature snapshot; no stabilized temperature history was recorded. The heating made the thermal design a practical limit.

During later V2 operation, an external tank inductor also became hot and was removed as part of a tank change.

## 13. V2 removes the hot series inductor
*19:35–21:15*

In the original V2 tank, the external series inductor became hot during operation. It was therefore removed, and the series capacitor was changed to approximately 1.66 nanofarads so that transformer leakage provided the tank inductance. In these equivalents the leakage is shown as a primary-referred part of the transformer. The two given leakage measurements were 16.42 and 16.50 microhenries. Their mean, 16.46 microhenries, with the new capacitance gives an ideal resonance of about 0.963 megahertz, close to the nominal carrier frequency. The software dead time was also set to approximately 60 nanoseconds. After these combined tank and timing changes, half-bridge heating decreased. Heating remained at the input bridge, so removing one hot component did not resolve the full thermal problem.

The modified V2 tank was then loaded directly at the secondary to see how much power reached the load and how the secondary voltage changed.

## 14. More PWM transfers more power
*21:15–22:40*

After the tank changes, an electronic load was connected directly to the V2 secondary, before the USB-C PD stage. The burst-enable PWM acts like a throttle: a greater enabled fraction gives the converter more switching time and increases average energy transfer. The two plots show the resulting secondary voltage and calculated power against load current. At 1.86 amperes, the load received 48.68 watts at 26.14 volts. At 4.29 amperes, the voltage was 20.07 volts and the power was 86.17 watts. At the highest current of 10.01 amperes, the voltage was 13.69 volts and the power reached 137.08 watts. The change in secondary voltage across the sweep was expected.

The same load sequence also shows where heating remained and guides the next circuit changes.

## 15. Secondary and bridge heating guide the redesign
*22:40–24:00*

The images show the 70.75-watt and final 137.08-watt points in the same direct secondary-load sequence. R3 covers the input bridge and R1 the secondary area. These are maximum surface readings within each region, not junction temperatures. The input bridge peaked at 83.9 degrees Celsius at the intermediate point and then varied at the higher loads. The secondary region rose to 98.3 degrees at the final point, showing substantial heating in the secondary area.

The bridge diodes were replaced, but the heating remained. Limited copper and a possible restriction through a single interlayer via could contribute. Wider bridge copper and via paths would improve current distribution and heat spreading. On the secondary side, the observed heating motivates reducing winding and rectifier losses and improving their current paths. These are proposed design changes.

Together, these results define the contribution and the present limit of the supply.

## 16. Controlled USB-C output, with thermal limits
*24:00–25:00*

The project brought the high-frequency charge-pump supply together with the USB-C output, sensing and local supplies. The MCU regulates the secondary voltage using bursts, while the USB-C power-delivery stage sets the selected connector voltage. On V1, 79.89 watts was measured at the USB-C connector. V2 transferred higher power to a direct secondary load, with an expected reduction in secondary voltage as the load increased. The secondary region continued to heat, and the load points did not reach thermal equilibrium. Heating still limits continuous operation. The 100-watt continuous target remains unfulfilled.

## 17. The tank was retuned around transformer leakage
*Backup*

The original design calculation used 9.4 microhenries of external series inductance and one nanofarad of series capacitance. Transformer leakage measurements were 16.42 and 16.50 microhenries; their mean, 16.46 microhenries, is used in both columns. Adding it to the external inductance gives 25.86 microhenries and an ideal series resonance of about 0.990 megahertz. The one-nanofarad value belongs to the original calculation; it is not a confirmed fitted value before the V2 change. In V2, the hot external inductor was removed and the series capacitance changed to about 1.66 nanofarads. The larger capacitance compensates for the lower series inductance in the LC relationship, giving an ideal resonance of about 0.963 megahertz. The tank sets this estimated resonance, while the nominal one-megahertz carrier excites it. The installed response also depends on load, the magnetizing branch and parasitics.

## 18. V2 secondary-load measurements
*Backup*

The electronic load was connected directly to the V2 secondary, before the USB-C PD stage. The table shows secondary power calculated from measured voltage and current. As current increased from 1.86 to 10.01 amperes, voltage fell from 26.14 to 13.69 volts and power rose from 48.68 to 137.08 watts. R3 is the input-bridge surface region and R1 is the secondary surface region. The highest R3 reading, 83.9 degrees Celsius, occurred at the intermediate point of 70.75 watts; later readings were lower, so the bridge temperatures are not monotonic with load. The R1 maximum increased from 50.3 to 98.3 degrees. These are successive load points without thermal equilibrium: the temperature changes reflect the load changes and continued heating during the sequence, rather than a settled temperature curve.

## 19. V2 power circuit and earlier work
*Backup*

The V2 circuit combines the input filter and rectifier, charge-pump and resonant branches, GaN half bridge, transformer, and secondary rectifier. The drawing shows the circuit before the tank change, with the external series inductor L4 still present. The charge-pump conversion principle and analytical design method came from earlier work by Ahmed M. Ammar, Frederik M. Spliid, Yasser Nour, and Arnold Knott. Their papers are “Analysis and Design of a Charge-Pump-Based Resonant AC–DC Converter With Inherent PFC Capability,” IEEE Journal of Emerging and Selected Topics in Power Electronics, 2020, DOI 10.1109/JESTPE.2020.2966143, and “A 1-MHz Resonant LED Driver With Charge-Pump-Based Power Factor Correction,” the same journal, 2021, DOI 10.1109/JESTPE.2021.3083404. The planar inductor and transformer came from earlier DTU work by Bima Nugraha Sanusi and the DTU Power Electronics group; component measurements were made by Máni Gautason. This project integrated the supplied magnetics and developed the hardware, control, sensing, local supplies and USB-C interface, then tested the assembled supply.

## 20. V1 USB-C connector operating points
*Backup*

These are selected loaded operating points at the USB-C connector for V1. The input was approximately 240 volts AC at 50 hertz. The selected voltage is compared with the average measured VBUS, and the signed error is relative to the selected voltage. Connector power is calculated as average VBUS multiplied by the load current. At the 20 volt, 4 ampere point this gives 19.9732 times 4, or 79.89 watts. Across all 14 loaded points, the largest absolute average-voltage error was 0.5826 percent at 5 volts and 1 ampere, which is outside this compact table. The 20 volt, 4.7 ampere oscilloscope capture shown earlier illustrates switching; the 79.89 watt connector result comes from the separate 4 ampere operating point.
