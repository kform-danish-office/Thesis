# V2 results entry

This is a blank entry pack. The CSVs contain headers only. The workbook has the
same six entry sheets, plus instructions and a dictionary. No V2 electrical or
thermal result, power rating, MCU identity, firmware identity, or circuit
revision has been entered. The user's identification of the photograph as V2
does not establish those details.

The [V2 board image provenance](../../../Pictures/Thesis/07_Hardware/V2_2026-10-25/README.md)
retains the original photograph, documentary crop and separately labeled
generated illustration. That image metadata stays with the assets; no
measurement row has been added from the photograph.

Use either `V2_Results_Entry.xlsx` or the UTF-8 CSVs. If both are edited, choose
one as the master and export the other before comparison. The workbook adds no
measurement formulas. Blank cells mean not entered, not zero.

| File / entry sheet | One row records |
| --- | --- |
| `test_setup.csv` / `Test setup` | One setup fact, declared setting, or acceptance criterion |
| `instruments.csv` / `Instruments` | One instrument/channel/probe configuration for a test |
| `steady_state.csv` / `Steady state` | One reading or explicitly derived quantity in an interval |
| `events.csv` / `Events` | One measured quantity or observation from a timed event |
| `thermal.csv` / `Thermal` | One location/sensor reading at one time in a sustained run |
| `evidence.csv` / `Evidence` | One retained source file and its provenance |

## Enter a run

1. Assign a unique `test_id`. Reuse it in all six tables. Identify the actual
   assembly, fitted parts/rework, controller target, firmware and saved settings
   in `test_setup`. Use `unknown` in a text field when an identity is unresolved.
2. Give every instrument configuration an `instrument_setup_id`. Record the
   channel, physical node and return, scaling, range, bandwidth, zero/deskew and
   calibration/accuracy basis. Retain wiring and probe-position evidence.
3. Define the input/output and auxiliary-power boundaries, load, cable,
   cooling, ambient method, duration, stability criterion and stop limits.
   Record advertised capabilities and actual requested/accepted PDO or APDO
   settings for each operating interval. PPS applies only to an advertised APDO.
4. Enter actual observations. Use one steady-state row per physical quantity;
   `quantity` determines its required `unit`. Put actual acquisition windows
   and the clock/alignment method in the record. Repeating an `interval_id`
   alone does not synchronize measurements.
5. Keep raw exports, screenshots, negotiation logs, status/settings exports and
   thermal histories. Register paths and checksums in `evidence`; refer to their
   IDs from each setup/measurement row. Record transformations separately.
6. Assess results against the previously declared criteria. Keep aborted,
   interrupted, incomplete and failed runs with their cause and evidence.

Use [DATA_DICTIONARY.md](DATA_DICTIONARY.md) for column meanings, quantity/unit
pairs and the setup fields to record. No planned load points have been inserted
as measurement rows. A test with no observation should have no measurement row.

## Calculation and interpretation rules

- Pair real AC input and external output readings over the same verified
  steady interval. Include measured external auxiliary input, or state its
  exclusion before reporting a qualified screening efficiency. Internal
  auxiliary power is already included at the DUT AC input.
- Connector VBUS, load-terminal voltage, secondary bulk and MCU-pin voltage
  are separate measurement points. PA2/current-sense telemetry does not supply
  independent connector output current. Record pin scaling and physical load
  resistance as observations or declared setup; these entries do not configure
  the hardware.
- For verified steady DC, `output_power_steady_product` may use the product of
  the matched external average voltage/current. Otherwise use the average of
  the synchronized instantaneous product. List source reading IDs and method.
- Keep instrument-logged PF/THD and recomputed PF/THD in their separate
  quantities. Record the harmonic range, definition and raw basis for THD.
- `vbus_ripple_peak_to_peak` is an instantaneous waveform maximum minus minimum
  over a stated capture. `vbus_average_spread` is the spread of average-voltage
  statistics across acquisitions. They are not interchangeable. AC coupling
  alone cannot establish absolute DC voltage.
- A thermal camera supplies surface temperature. Junction estimates require a
  separate method and uncertainty basis. One image or short electrical point
  does not establish sustained operation, continuous power or lifetime.

## Planned checks — not entered

- [ ] Verify assembly, firmware, fitted sensing and calibration records.
- [ ] Record supported fixed-PDO and advertised-APDO negotiation and load tests.
- [ ] Capture matched AC/DC/auxiliary power, PF/THD, ripple and stress readings.
- [ ] Record startup/shutdown, load changes, attach/detach, timing and protection.
- [ ] Complete the defined-duration temperature history and cooldown/restart.
- [ ] Review repeatability, uncertainty, exclusions and evidence completeness.

This pack follows the existing V2 hardware section, revised validation method
and revised-plan results status. It does not add the earlier assembly's results
or the plan's reported V2 point to the measured dataset. No compile, powered
test, firmware change or hardware change is implied by creating these files.
