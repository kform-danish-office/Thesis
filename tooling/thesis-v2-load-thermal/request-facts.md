# Current V2 load and thermal tests

User requests integrating seven new V2 secondary-output load captures and seven thermal images into the thesis using supervised Terra proposals and lead judgement. Use AC supply, electronic load and thermal images only. Do not use the scope row or derive any waveform/ripple/timing results from it. Earlier valid V1 scope data is outside this exclusion and remains historical.

User confirms in the request: none of these load tests became thermally stable. More work is expected on diode selection and related design. The tests show operation is possible. The input bridge heated more at lower output power and less at higher output power in the observed tests. Treat causes as hypotheses, not diagnoses. These are secondary-output results, not USB-C connector results or continuous ratings.

Original CSV files are in /workspace/thesis/Data/measurements/v2_load_thermal/raw. Device IDs: AC supply 4c5d43a8-3948-432f-9320-a8eeab4d5849; electronic load d80f4f53-4f7c-44ee-8ce0-d5860477faa7. Ignore all fields from a12d2769-5fe0-4f5d-b5eb-84b102a3e8fc (scope).

Seven images are visible in the user message but not yet found as local files. Image clock timestamps and visually transcribed R3/R1 maxima (deg C):
20:24:39: 65.1 / 50.3
20:25:54: 83.9 / 57.2
20:26:46: 68.2 / 59.7
20:27:11: 73.2 / 69.4
20:27:33: 74.5 / 81.6
20:27:54: 75.6 / 88.7
20:28:17: 73.7 / 98.3
ROI emissivity displayed 0.95; screen footer 0.97. Use ROI emissivity for region readings, do not silently merge it with global setting. Region-to-component mapping is awaiting user confirmation. CSV times are 19:24:41 through19:28:20 UTC, matching camera sequence +1h and 2-4s later. Do not claim clock synchronization or exact same instant.

Follow /workspace/AGENTS.md, /workspace/tooling/thesis-voice-guide.md and /workspace/tooling/thesis-agent-voice-checklist.md. Existing voice guide's single 95 W thermal image refers to an older run; the new dataset expands the V2 results. No upload dates or chat handoff language in thesis narrative. All current source and historical data read-only for proposing agents. Write only assigned review outputs. Root edits after judging.

User confirmed R3=input bridge; R1=secondary area. It is not a single-component junction measurement. Original thermal-image files requested for embedding; none accessible yet.
