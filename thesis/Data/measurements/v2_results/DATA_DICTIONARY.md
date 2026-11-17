# V2 entry dictionary

## Common rules

- CSV encoding is UTF-8; separator is comma; quote text containing commas or
  newlines. Use decimal points and no thousands separators in numeric cells.
- Leave missing numeric data empty. Do not use zero, `NaN` or an estimate as a
  missing-value marker. A measured zero may be entered with its source.
- Dates use `YYYY-MM-DD`. Timestamps use ISO 8601 UTC, including `Z`. If a
  capture lacks UTC, leave the UTC field empty and document its native timebase
  and synchronization in `test_setup`. Do not invent timestamps.
- IDs are text. Keep each ID unique within its test and record type. Join on
  `test_id` plus the relevant ID. Use `|` to separate multiple referenced IDs.
- Every result needs evidence and an identified instrument configuration, or an
  explicit qualification explaining the missing basis. Derived readings list
  their source reading IDs and formula/method in `notes`.
- Numeric values in the long-form tables use the unit in the quantity tables
  below. `1` means dimensionless. `%` means percent, not a fractional ratio.
- `context_type` is `test`, `interval`, `event`, `run` or `sample`.
  `context_id`/`context_ids` refers to that ID; for `test` use `test_id`.

## Test setup

`test_setup` is long form: one named fact per row. It avoids storing several
instruments, rework items or cooling conditions in one cell.

| Column | Meaning |
| --- | --- |
| `setup_record_id` | Unique ID for this setup fact within `test_id` |
| `context_type`, `context_id` | Test or specific interval/event/run/sample to which the fact applies |
| `category` | One of the categories below |
| `item_id` | Identifies the individual part, cable, supply, criterion, signal or change |
| `field_name` | Name of the fact; use the names below and document any additions |
| `text_value` | Text, date, status, reference, or unresolved-identity statement |
| `numeric_value`, `unit` | Numeric setting/fact with explicit unit; leave empty for text facts |
| `evidence_ids`, `notes` | Source IDs and any method, uncertainty or qualification |

Use one value column per fact. Enter units such as `V`, `A`, `W`, `Hz`, `s`,
`ohm`, `degC`, `mm`, `%`, `1`, or the stated calibration-coefficient unit.
The following is a recording checklist, not evidence that any check has run.

| Category | Facts to record using `field_name` |
| --- | --- |
| `identity` | `test_date_utc`, `operator`, `assembly_id`, `hardware_generation`, `pcb_revision`, `mcu_part_verified`, `identity_basis`, `test_objective`, `requirement_ids` |
| `hardware` | `schematic_source`, `bom_source`, `fitted_parts`, `magnetics_identification`, `resonant_values`, `rework_description`, `change_reason`, `comparison_test_id`, `before_after_evidence_ids` |
| `firmware` | `target_selected`, `version`, `source_ref`, `build_id`, `settings_export`, `settings_validation_status`, `status_export`, `live_mode`, `protection_enable_state` |
| `calibration` | `signal_name`, `conversion_formula`, `gain`, `offset`, `calibration_basis`, `calibration_evidence_ids`; link retained raw and external reference readings |
| `source` | `mains_source`, `set_voltage_V`, `set_frequency_Hz`, `isolation_and_limiting`, `aux_supply_description` |
| `protocol` | `source_capabilities_export`, `sink_id`, `protocol_mode` (`fixed_pdo` or `pps`), `pdo_apdo_id`, `requested_voltage_V`, `requested_current_A`, `accepted_voltage_V`, `accepted_current_limit_A`, `advertised_apdo_limits`, `negotiation_log`; scope to each interval/event when changed |
| `load` | `load_id`, `load_mode`, `load_setting`, `load_resistance_ohm`, `resistance_basis` (`measured` or `declared`), `load_rating_reference`; include a unit with every numeric setting |
| `wiring` | `cable_id`, `cable_length_m`, `cable_current_rating_A`, `connector_id`, `wiring_diagram`, `probe_positions`, `output_sense_point`, `current_sense_point` |
| `cooling` | `orientation`, `heatsinks`, `airflow_method`, `fan_setting`, `ambient_method`, `enclosure_condition`, `cooling_changes` |
| `boundary` | `ac_input_boundary`, `output_boundary`, `aux_accounting` (`included`, `excluded`, `not_present` or `unknown`), `aux_supply_ids`, `cable_loss_treatment`, `included_offboard_functions`, `dimension_convention` |
| `acquisition` | `timebase_id`, `clock_alignment_method`, `clock_offset_s`, `window_overlap_basis`, `harmonic_min_order`, `harmonic_max_order`, `thd_definition`, `repeat_count`, `uncertainty_budget_reference` |
| `acceptance` | `criterion_id`, `quantity`, `comparison_rule`, `limit`, `duration_s`, `stability_criterion`, `stop_condition`, `limit_basis`; specify numeric limits and units before the run |
| `thermal_run` | `run_id`, `initial_condition`, `start_utc`, `end_utc`, `planned_duration_s`, `actual_duration_s`, `sampling_interval_s`, `location_map`, `temperature_method`, `junction_estimation_method`, `stability_assessment`, `termination_reason`, `cooldown_restart_observation` |
| `change` | `changed_item`, `before_condition`, `after_condition`, `reason`, `expected_effect`, `comparison_test_id`, `change_evidence_ids`; identify each controlled change |

`load_resistance_ohm` describes the physical load. It does not set firmware
limits, infer current capability, or configure the board. Planned duration and
criteria are metadata, not measured outcomes. Keep measured dimensions and
their boundary evidence distinct from a photograph or drawing estimate.

## Instruments

One row defines an instrument/channel/probe configuration. Use a new
`instrument_setup_id` when its connection, range, scaling or acquisition
settings change. `instrument_id` identifies the physical asset.

| Columns | Meaning |
| --- | --- |
| `instrument_role`, `manufacturer_model`, `serial_or_asset_id` | Actual role and device identity; do not inherit older test equipment silently |
| `channel`, `probe_model_serial` | Channel and probe identity |
| `measurement_point`, `reference_return` | Exact physical connection and voltage/current reference |
| `range_setting` | Range with unit; include autorange state |
| `probe_scale_factor`, `scale_factor_definition` | Numeric attenuation/conversion factor and its direction/unit definition |
| `current_polarity`, `coupling` | Physical positive direction and `AC`/`DC`/other declared coupling |
| `bandwidth_Hz`, `sample_rate_Hz`, `record_length_samples` | Effective path bandwidth, sample rate and sample count; distinguish a bandwidth limit from probe capability in notes |
| `averaging_method` | Acquisition/integration/averaging settings and count |
| `calibration_status`, `calibration_date`, `calibration_due_date` | Stated calibration status and actual dates |
| `zero_deskew_check` | What was zeroed/deskewed, when, residual error and supporting evidence |
| `accuracy_uncertainty_ref` | Accuracy/range specification, uncertainty method or retained budget |
| `evidence_ids`, `notes` | Setup/certificate evidence and limitations |

## Steady state

One row is one reading; several rows form an operating interval. Record fixed
PDO/PPS details in interval-scoped setup rows. Do not average unrelated points.

| Columns | Meaning |
| --- | --- |
| `interval_id`, `reading_id` | Operating interval and unique reading ID |
| `quantity`, `value`, `unit` | Quantity from the table below, numeric reading, exact unit |
| `statistic` | `mean`, `rms`, `real_power`, `peak_to_peak`, `spread_of_means`, `ratio`, `count` or a documented instrument statistic |
| `measurement_point`, `measurement_point_class` | Exact connection and physical class; see below |
| `instrument_setup_id` | Instrument configuration used; derived rows reference their inputs instead |
| `window_start_utc`, `window_end_utc`, `window_duration_s` | Actual acquisition/averaging window and duration, not nominal dwell time |
| `timebase_id`, `window_match_status` | Alignment basis and `matched`, `not_matched`, `unknown` or `not_applicable` |
| `value_origin` | `instrument_logged`, `calculated_from_logged` or `calculated_from_raw` |
| `input_reading_ids` | Source IDs for a calculation; empty for a direct reading |
| `evidence_ids`, `qualification`, `notes` | Raw evidence, limitations and method/formula |

For a matched power/efficiency set, AC, DC and any external auxiliary readings
must have demonstrably aligned windows and durations covering the same steady
condition. Store native relative timing/alignment in setup if UTC is unavailable.
If matching or auxiliary accounting is unresolved, retain the readings and
qualification but leave calculated efficiency empty. For PF recomputation use
matched real power and RMS values from the same input boundary. THD recomputation
needs the retained harmonics, fundamental definition and harmonic range.

| `quantity` | `unit` | Meaning |
| --- | --- | --- |
| `ac_mains_voltage_rms` | `V` | RMS at the stated DUT input boundary |
| `ac_mains_current_rms` | `A` | RMS current at that boundary |
| `ac_mains_real_power` | `W` | Real power, not apparent power |
| `ac_mains_frequency` | `Hz` | Measured line frequency |
| `external_aux_voltage_mean` | `V` | One identified external auxiliary input |
| `external_aux_current_mean` | `A` | Same auxiliary input and interval |
| `external_aux_real_power` | `W` | Measured or explicitly derived auxiliary contribution |
| `total_input_power` | `W` | AC plus included external auxiliary input; list source IDs and boundary |
| `connector_vbus_voltage_mean` | `V` | External DC-coupled voltage at connector VBUS |
| `external_output_current_mean` | `A` | External load-path current; state sense point |
| `load_terminal_voltage_mean` | `V` | Load-end voltage; distinct from connector voltage |
| `secondary_bulk_voltage_mean` | `V` | Intermediate bulk node |
| `mcu_pin_voltage_mean` | `V` | Named MCU pin relative to its local reference |
| `current_sense_node_voltage_mean` | `V` | Named sense node, not connector current |
| `adc_raw_code_mean` | `count` | Named raw ADC channel before conversion |
| `firmware_reported_voltage` | `V` | Telemetry with named physical meaning and calibration |
| `firmware_reported_current` | `A` | Telemetry with named physical meaning and calibration |
| `firmware_reported_power` | `W` | Firmware quantity; not external delivered power |
| `output_power_steady_product` | `W` | Matched external mean voltage times mean current for verified steady DC |
| `output_power_instantaneous_mean` | `W` | Mean of synchronized instantaneous external voltage/current product |
| `screening_efficiency` | `%` | Qualified output/total-input ratio; not an assigned continuous rating |
| `pf_instrument_logged` | `1` | Analyzer's logged true PF |
| `pf_recomputed` | `1` | Recomputed true PF with source readings and formula |
| `current_thd_instrument_logged` | `%` | Instrument's logged current THD with harmonic definition |
| `current_thd_recomputed` | `%` | Recomputed current THD with retained spectrum/range |
| `vbus_ripple_peak_to_peak` | `V` | Instantaneous max-minus-min waveform voltage over specified capture |
| `vbus_average_spread` | `V` | Max-minus-min of average-voltage statistics across acquisitions |
| `secondary_bulk_ripple_peak_to_peak` | `V` | Instantaneous bulk waveform max-minus-min |

Allowed `measurement_point_class`: `ac_input`, `external_aux_input`,
`usb_connector`, `load_terminals`, `secondary_bulk`, `mcu_pin`,
`current_sense_node`, `switch_node`, `gate_source`, `driver_input`, `telemetry`,
`system_boundary`, `other`. Specify physical point and return even for `other`.
Add a new quantity only with its unit, meaning and method recorded in notes and
the dictionary; extend the workbook's validation list when doing so.

## Events

One event may have several reading rows and repeated trials. Use distinct
`event_id` values for trials; `repeat_index` is the trial number. `reading_id`
is unique across steady-state and event readings within the test.

| Columns | Meaning |
| --- | --- |
| `event_type` | `startup`, `shutdown`, `load_step`, `load_removal`, `no_load_recovery`, `mode_change`, `attach`, `detach`, `pps_transition`, `protection` or `timing` |
| `stimulus_description`, `trigger_definition` | Applied before/after condition, injection/disconnect method, trigger level/direction and channel |
| `timebase_id`, `time_zero_definition` | Shared clock and physical zero-time reference for all event channels |
| `quantity`, `value`, `unit`, `statistic` | Event quantity below, numeric result, exact unit, and statistic (including count/window for jitter) |
| `measurement_point`, `measurement_point_class`, `instrument_setup_id` | Physical location and acquisition configuration; same classes as steady state |
| `capture_pretrigger_s`, `capture_posttrigger_s` | Recorded span before/after time zero, in seconds |
| `input_reading_ids`, `acceptance_criterion_id` | Inputs to any derivation and previously declared setup criterion |
| `observed_response`, `recovery_description` | Factual response, state changes, recovery/restart and interruptions |
| `result` | `pass`, `fail`, `inconclusive`, `aborted` or `not_assessed`; criterion and evidence required for pass/fail |
| `evidence_ids`, `notes` | Raw traces/logs, applied-condition evidence and method/limitations |

| `quantity` | `unit` | Meaning |
| --- | --- | --- |
| `connector_vbus_minimum` | `V` | Absolute event minimum at connector |
| `connector_vbus_maximum` | `V` | Absolute event maximum at connector |
| `vbus_overshoot` | `V` | Excursion above stated final/reference level |
| `vbus_undershoot` | `V` | Excursion below stated final/reference level |
| `load_current_before` | `A` | Measured pre-event external load current |
| `load_current_after` | `A` | Measured post-event external load current |
| `rise_time` | `s` | State percentage/level definition |
| `fall_time` | `s` | State percentage/level definition |
| `settling_time` | `s` | Time to enter and remain within declared band |
| `response_delay` | `s` | Defined stimulus-to-response interval |
| `recovery_time` | `s` | Defined fault/removal-to-recovery interval |
| `protection_trip_voltage` | `V` | Externally verified applied trip condition |
| `protection_trip_current` | `A` | Named externally measured path; not an inferred PA2 current |
| `switch_node_peak_voltage` | `V` | Measured switching stress at stated node/reference |
| `gate_source_peak_voltage` | `V` | Measured gate-to-own-source voltage |
| `switching_frequency` | `Hz` | Measured carrier frequency |
| `effective_dead_time` | `s` | Measured transistor/driver interval with edge definition |
| `enable_alignment_delay` | `s` | Measured enable/carrier relation with edge definition |
| `timing_jitter` | `s` | State statistic, number of edges and observation interval |
| `turn_on_residual_voltage` | `V` | Switch-node departure from target rail at independently identified turn-on |

For a qualitative event, leave `quantity`, `value` and `unit` empty and enter
the observation/evidence. Protection requires an identified applied condition
and response; ordinary operation does not establish a fault test. Programmed
timer settings do not establish effective dead time or measured jitter.

## Thermal

| Columns | Meaning |
| --- | --- |
| `run_id`, `sample_id` | Sustained run and unique sample/location reading |
| `timestamp_utc`, `elapsed_s` | Actual sample time and seconds since the run's defined start |
| `location_id` | Location/component/sensor tied to a retained annotated map |
| `temperature_kind` | `surface_measured`, `junction_estimated` or `junction_measured`; junction entries require their separate validated method/evidence |
| `temperature_C`, `ambient_C` | Location and ambient temperature in degrees Celsius |
| `instrument_setup_id` | Thermal camera/contact/internal sensor configuration |
| `emissivity`, `reflected_apparent_temperature_C` | Actual camera settings; blank for non-radiometric methods |
| `run_state` | `start`, `running`, `paused`, `stopped`, `cooldown` or `restart` |
| `interruption_event_id` | Linked interruption/protection/restart event, if any |
| `matched_interval_id` | Corresponding electrical interval; do not infer power from a photo label |
| `evidence_ids`, `notes` | Original thermal data, location, sensor method and limitations |

Repeat rows over time and locations. Record orientation/cooling, initial
condition, declared duration, stability and stop criteria in setup. Record
actual duration, interruptions, drift, termination and cooldown/restart there
afterward. A surface maximum is not a junction temperature. Stability or a
continuous-power conclusion requires review of the complete run and criteria.

## Evidence

| Columns | Meaning |
| --- | --- |
| `evidence_id`, `context_type`, `context_ids` | File ID and linked context ID(s) |
| `evidence_role` | `raw_waveform`, `screenshot`, `power_log`, `protocol_log`, `firmware_status`, `settings_export`, `thermal_raw`, `thermal_image`, `assembly_photo`, `wiring_photo`, `calibration`, `analysis`, or documented other role |
| `original_filename`, `retained_path` | Original filename and actual retained path, preferably relative to thesis root |
| `captured_at_utc`, `acquisition_timebase_id` | Actual acquisition time/clock; leave unknown UTC blank |
| `sha256` | SHA-256 of retained file bytes, not a guessed checksum |
| `original_or_derived`, `parent_evidence_ids` | `original`/`derived`; source IDs for derived material |
| `transformation_description` | Exact crop, cleanup, processing or extraction, with tools/settings as relevant |
| `notes` | Provenance, date uncertainty, missing source or other limitations |

Preserve original files. A cleaned/cropped board image belongs in a derived
record linked to its original; it is assembly evidence, not measured electrical
performance. Do not replace raw waveforms with rescaled versions to force an
expected result.
