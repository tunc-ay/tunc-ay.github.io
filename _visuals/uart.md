---
title: "How UART works"
order: 1
excerpt: "Follow the byte 0x55 from a transmitter to a receiver, bit by bit."
header:
  teaser: /assets/images/visuals/how-uart-works.svg
last_modified_at: 2026-11-09
---

UART (Universal Asynchronous Receiver/Transmitter) sends data one bit at a time over a wire, with no shared clock. This page follows one byte, `0x55`, from a sending device to a receiving device.

<figure>
  <a href="{{ '/assets/images/visuals/how-uart-works.svg' | relative_url }}">
    <img src="{{ '/assets/images/visuals/how-uart-works.svg' | relative_url }}"
         alt="Diagram of Device A sending the byte 0x55 to Device B over a TX-to-RX wire with a common ground. A waveform shows the frame: idle high, start bit 0, data bits 1 0 1 0 1 0 1 0 sent least significant bit first, and stop bit 1. Five numbered steps explain the process.">
  </a>
  <figcaption>The path of one byte through a UART link. Select the image to open it full size.</figcaption>
</figure>

## What the diagram shows

1. **Parallel to serial.** The transmitter takes a byte from the processor and builds a frame: a start bit, the data bits, an optional parity bit, and a stop bit.
2. **Serial transmission.** The bits go out one at a time on the TX line at a fixed baud rate. The line is high when idle, the start bit is low, the data bits follow with the least significant bit first, and the stop bit is high.
3. **Reception and sampling.** The receiver detects the falling edge of the start bit, then samples the line in the middle of each bit period using its own baud-rate clock. Many receivers sample at 16 times the baud rate to find that midpoint.
4. **Serial to parallel.** The receiver rebuilds the byte and checks the stop bit, and the parity bit if it is used. If the stop bit is not 1, the receiver reports a framing error.
5. **Data received.** The byte is available to the receiving processor.

## The waveform in text

Sending `0x55` (`0101 0101`) with 8N1 (8 data bits, no parity, 1 stop bit), the line carries this sequence:

| Slot  | Start | D0 | D1 | D2 | D3 | D4 | D5 | D6 | D7 | Stop |
| ----- | ----- | -- | -- | -- | -- | -- | -- | -- | -- | ---- |
| Level | 0     | 1  | 0  | 1  | 0  | 1  | 0  | 1  | 0  | 1    |

The frame is 10 bit times long. At 9600 baud, one bit lasts 1 / 9600 ≈ 104 µs, so the whole frame takes about 1.04 ms.

## Things to remember

- Both devices must use the same baud rate, number of data bits, parity setting, and number of stop bits.
- TX on one device connects to RX on the other, and the two devices need a common ground.
- UART has no clock line and no addressing. It is a point-to-point link.
- Parity is the only built-in error check, and it is optional.
