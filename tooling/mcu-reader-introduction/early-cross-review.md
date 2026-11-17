# Read-only cross-review: Chapters 2–3

Compared current text with the snapshot in before/. The revised prose names the physical role before PA/PB labels, explains sensor conversion and serial communication, and distinguishes primary-current sensing from connector current. The G071 and F410 enable assignments remain correct. The free-running ADC scan remains explicitly unsynchronized to carrier cycles. The USB-C paragraph does not claim protocol conformance; it still separates fixed electrical settings from negotiation/interoperability tests. No new incorrect clock or synchronization guarantee was found.

One small actionable clarification:

- **Chapters/03_Requirements_Architecture/02_Electrical_Specifications.tex:4** — The new definition says bursts are separated by intervals “when transfer is inhibited.” For the intended beginner reader, that can suggest all energy transfer stops immediately. The stored tank energy can continue reaching the secondary after enable is low, as the safety section correctly explains. Use “when further switching is inhibited” or “when no further switching is enabled.” This preserves the intended command timing and avoids teaching zero residual transfer.

No other actionable technical or protocol regressions were found. No source files were edited during this review.
