# Digest Control-System Diagram

This figure summarizes the G071 `PWR-1.9.20` baseline as a conventional
closed-loop voltage-control system. The detailed implementation diagram remains
in [firmware-flow.md](firmware-flow.md).

The F410 port retains this control structure with different peripheral pins;
see [STM32F410 port notes](stm32f410-port.md).

Exports: [PNG](firmware-flow-distilled.png) | [SVG](firmware-flow-distilled.svg)

```mermaid
flowchart LR
    REF["Voltage command<br/>Vref"] -->|+| SUM((" "))
    SUM --> CTRL["Voltage controller<br/>Light: bang-bang<br/>Loaded: averaged duty"]
    CTRL --> EN["PA10 EN control<br/>OFF / burst / ON"]
    EN --> PLANT["Power stage<br/>1 MHz half bridge<br/>Transformer + rectifier"]
    PLANT --> OUT(["Vout"])

    OUT --> SENSE["PA1 isolated voltage feedback<br/>ADC1 DMA"]
    SENSE -->|-| SUM

    LOAD["PA2 bridge-current detector<br/>Light / loaded mode select"] --> CTRL
    PROTECT["OVP / current protection"] -->|Inhibit| EN
    START["Startup precharge"] -.-> EN
    CARRIER["TIM1 PA8/PA9 carrier<br/>Center-aligned dead gap"] --> PLANT

    classDef block fill:#ffffff,stroke:#000000,stroke-width:2px,color:#000000
    classDef junction fill:#ffffff,stroke:#000000,stroke-width:2px,color:#000000
    class REF,CTRL,EN,PLANT,OUT,SENSE,LOAD,PROTECT,START,CARRIER block
    class SUM junction
    linkStyle default stroke:#000000,stroke-width:2px,fill:none
```

PA1 closes the voltage-control loop. PA2 measures half-bridge current only and
selects light-load or loaded behavior; it is not secondary-output-current
feedback. Protection can override the controller and force PA10 EN off.
