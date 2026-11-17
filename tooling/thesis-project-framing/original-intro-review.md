# Original introduction and project framing

Read-only inspection of the approved original archive `DTU_Thesis_USB_C_Plain_Headings_2026-10-24.zip` (SHA-256 `fed0ef9fadd0c1c4632b3d0f9aa057885d61714cfa8eacb5b60ed2adbbe3e8ed`). No thesis source, repository, build, manifest or publication state was changed.

## Exact original opening

Member: `Chapters/01_Introduction/chapter.tex`.

```tex
I started with a DTU charge-pump converter and supplied planar magnetics, then built the hardware and controller needed to use them as a USB-C laboratory supply. The main change was the load: it could be absent at startup, draw different amounts of power, or disappear while the converter still held energy. That change connects the circuit design, burst-control development, and tests described in this thesis.
```

The original introduction centers on adapting the converter to a detachable USB-C load, including startup without a load, changing demand and disconnection with stored energy. It is not a V1/V2/V3 development-roadmap opening. The current opening replaces that load-focused explanation with a board-development summary.

## Original aim and motivation

Member: `Chapters/01_Introduction/03_Aim_Objectives.tex`.

```tex
My aim was to turn the inherited charge-pump topology and supplied planar magnetics into an isolated AC--DC laboratory supply, then evaluate it with digital burst control and a USB-C output.
```

The original motivation begins:

```tex
Increasing the switching frequency reduces the energy transferred in each switching period, which can reduce the size of the passive components. It also leaves less time for commutation and makes winding loss, switching loss, and parasitic impedance harder to ignore. A smaller magnetic component is useful only if the power stage, layout, gate drive, and controller can operate with it.
```

The original motivations then describe the difference between the earlier reference load and a USB-C load, integration of the supplied planar inductor and transformer, and implementation of the GaN stage, controller and USB-C output. Those are the original technical aims. It does not describe the user-facing functionality of a bench/laboratory instrument such as manually adjustable outputs or laboratory front-panel controls.

## Important source fact

The uploaded original ZIP itself already contains the words “USB-C laboratory supply” in its opening/problem statement and “isolated AC--DC laboratory supply” in its aim. Blindly restoring it verbatim would therefore repeat the framing the user has just rejected. The latest user correction governs. Its original title is already:

> Design and Implementation of a High-Frequency Charge-Pump PFC Resonant Converter for a USB-C Power Supply

The current title and subtitle in `Setup/Statics.tex` are byte-identical to those original values. “USB-C power supply” is therefore the narrow, source-supported project name. No new product category such as charger or adapter needs to be invented.

The selected `/workspace/Thesis` reference checkout contains firmware/web documentation, not an older thesis TeX introduction. The working-source ZIP also contains no thesis introduction. No earlier authoritative thesis introduction than the approved thesis ZIP was found in these sources.

## Minimal restoration

Keep the existing chapter input list so that the requested V2/V3 sections and MCU pin introduction remain. Restore the original opening's detachable-load narrative, changing the rejected project label to “USB-C power supply”. If retaining the user's established impersonal/passive voice, a close rendering is:

> The project started with a DTU charge-pump converter and supplied planar magnetics. The power hardware and controller were developed for a USB-C power supply. Its load could be absent at startup, draw different amounts of power, or disconnect while energy remained in the converter. These operating conditions guided the circuit design, burst control and tests.

This stays close to the original without claiming a different purpose or reintroducing first-person prose. Do not restore the entire old Chapter 1 file from the ZIP: its input list lacks the subsequently requested V2, V3 and MCU-pin sections. Do not undo colour schematic paths, direct captions, firmware-stage rationale or equal margins.

Correct project-as-laboratory-supply phrasing in the abstract, preface, aims/problem statement and conclusion. Keep genuine references to laboratory testing and the external AC source: laboratory test conditions do not classify the converter itself as a laboratory power supply. In particular the input-condition table's “240 V, 50 Hz laboratory supply” refers to the external test source, not the designed USB-C converter; “AC source” is a clearer alternative there if edited.
