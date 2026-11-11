---
title: "How UART works"
order: 1
excerpt: "Follow the byte 0x55 from a transmitter to a receiver, bit by bit."
header:
  teaser: /assets/images/visuals/how-uart-works.svg
last_modified_at: 2026-11-11
---

<p class="visuals-back"><a href="{{ '/visuals/' | relative_url }}">&larr; All explainers</a></p>

UART (Universal Asynchronous Receiver/Transmitter) sends data one bit at a time over a wire, with no shared clock. This page follows one byte, `0x55`, from a sending device to a receiving device. It starts with the wiring, then the frame on the wire, then what happens inside each chip, and ends with what goes wrong.

## 1. The wiring

A basic UART link uses two signal wires and a ground:

| Device A pin | Connects to | Device B pin | Purpose                  |
| ------------ | ----------- | ------------ | ------------------------ |
| TX           | →           | RX           | Data from A to B         |
| RX           | ←           | TX           | Data from B to A         |
| GND          | —           | GND          | Common voltage reference |

TX on one device always goes to RX on the other. If both devices only send in one direction, one of the two data wires can be left out. There is no clock wire and no address: the link connects exactly two devices.

## 2. The frame on the wire

Because there is no clock, the sender wraps every byte in a **frame** so the receiver can find where the bits start and end:

1. **Idle.** The line rests high.
2. **Start bit.** The line goes low for one bit time. This falling edge tells the receiver that a frame is beginning.
3. **Data bits.** Usually 8, sent **least significant bit first**.
4. **Parity bit** (optional). An extra bit that makes the count of 1s even or odd.
5. **Stop bit.** The line goes high for one bit time (some setups use two). The line then stays high until the next start bit.

Sending `0x55` (`0101 0101`) with 8N1 (8 data bits, no parity, 1 stop bit), the line carries this sequence:

| Slot  | Idle | Start | D0  | D1  | D2  | D3  | D4  | D5  | D6  | D7  | Stop | Idle |
| ----- | ---- | ----- | --- | --- | --- | --- | --- | --- | --- | --- | ---- | ---- |
| Level | 1    | 0     | 1   | 0   | 1   | 0   | 1   | 0   | 1   | 0   | 1    | 1    |

The least significant bit goes first, so D0 is the rightmost bit of `0101 0101`, which is 1. The data bits therefore read 1 0 1 0 1 0 1 0 on the wire, which looks like the reverse of the binary notation.

The frame is 10 bit times long. At 9600 baud, one bit lasts 1 / 9600 ≈ 104 µs, so the whole frame takes about 1.04 ms. Only 8 of those 10 bits are data, so the useful rate is 80% of the baud rate.

## 3. Inside the transmitter

1. The processor writes the byte `0x55` to the transmit data register.
2. The hardware copies it into the **shift register** when the shift register is free. The processor can then write the next byte without waiting.
3. The **baud-rate generator** divides the peripheral clock down to one tick per bit time.
4. On each tick, the transmitter drives the TX pin with the next bit: start bit, D0 through D7, then the stop bit. It then returns the pin to idle (high).
5. When the shift register is empty, the hardware reports "transmit complete" and loads the next byte if one is waiting.

## 4. Inside the receiver

The receiver has its own baud-rate generator, running independently of the sender's.

1. **Wait for the start.** The receiver watches the RX line. A high-to-low transition marks the start of a frame.
2. **Find the middle of the bit.** Many receivers sample at 16 times the baud rate. After the falling edge, they count 8 of those ticks to reach the middle of the start bit and check that the line is still low. If it is not, the edge was a glitch and the receiver goes back to waiting.
3. **Sample each bit.** From there, the receiver samples every 16 ticks, always near the middle of a bit, where the signal is most stable.
4. **Shift in the bits.** Each sampled bit enters the shift register. Since the first bit received is the least significant, it ends up in bit 0 of the byte.
5. **Check the stop bit.** The line should be high. If it is low, the receiver reports a framing error.
6. **Hand over the byte.** The byte moves to the receive data register and a flag or interrupt tells the processor to read it.

## 5. When it goes wrong

| Error          | Cause                                                          | What the receiver sees                              |
| -------------- | -------------------------------------------------------------- | --------------------------------------------------- |
| Framing error  | Baud rate mismatch, noise, or a line break                     | Stop bit is 0 instead of 1                          |
| Parity error   | A bit flipped in transit (when parity is enabled)              | Number of 1s does not match the parity setting      |
| Overrun error  | The processor did not read the previous byte before a new one arrived | The new byte replaces or is lost against the old one |

### Why the baud rates must match

The receiver synchronizes once, at the start bit, and then relies on its own clock. Any mismatch accumulates over the frame. In 8N1 the stop bit is sampled 9.5 bit times after the start edge. If the clocks differ by 6%, the receiver's sampling point has drifted 9.5 × 0.06 ≈ 0.57 bit times by then, past the edge of the bit it is trying to read. It samples the wrong bit and the data is corrupted.

The theoretical limit is about 5% (0.5 / 9.5). In practice, sampling granularity and edge distortion reduce that, so aim for a combined error of 2% or less between the two devices.

## The whole path in one picture

<figure>
  <a href="{{ '/assets/images/visuals/how-uart-works.svg' | relative_url }}">
    <img src="{{ '/assets/images/visuals/how-uart-works.svg' | relative_url }}"
         alt="Diagram of Device A sending the byte 0x55 to Device B over a TX-to-RX wire with a common ground. A waveform shows the frame: idle high, start bit 0, data bits 1 0 1 0 1 0 1 0 sent least significant bit first, and stop bit 1. Five numbered steps explain the process.">
  </a>
  <figcaption>The path of one byte through a UART link. Select the image to open it full size.</figcaption>
</figure>

The five steps in the diagram match the sections above: parallel to serial (section 3), serial transmission (section 2), reception and sampling (section 4), serial to parallel (section 4), and data received (section 4).

## Things to remember

- Both devices must use the same baud rate, number of data bits, parity setting, and number of stop bits.
- TX on one device connects to RX on the other, and the two devices need a common ground.
- UART has no clock line and no addressing. It is a point-to-point link.
- The start bit's falling edge is the only synchronization the receiver gets. After that, it relies on its own clock.
- Parity is the only built-in error check, and it is optional.

{% include visuals-nav.html %}
