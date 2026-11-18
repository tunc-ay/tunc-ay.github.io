---
title: "How CAN works"
order: 2
excerpt: "Follow one message, ID 0x123 carrying the byte 0x55, from a transmitter to every receiver on a CAN bus."
header:
  teaser: /assets/images/visuals/how-can-works.svg
last_modified_at: 2026-11-18
---

<p class="visuals-back"><a href="{{ '/visuals/' | relative_url }}">&larr; All explainers</a></p>

CAN (Controller Area Network) is a two-wire differential bus where many nodes share the same pair of wires. Messages carry an identifier instead of a destination address, and every node hears every message. This page follows one classical CAN frame, with ID `0x123` and the data byte `0x55`, at 500 kbit/s. It starts with the wiring and signal levels, then the frame, then what happens inside each node, and ends with what goes wrong.

## 1. The wiring

A CAN node has a **controller** (usually inside the microcontroller) and a **transceiver** (a separate chip). The controller works with logic-level TX and RX signals. Only the transceiver connects to the bus.

| Node pin / signal | Connects to | Purpose                                              |
| ----------------- | ----------- | ---------------------------------------------------- |
| Controller TX     | → TXD       | Logic-level bits to the transceiver                  |
| Controller RX     | ← RXD       | Logic-level bits from the transceiver                |
| Transceiver CAN_H | ↔ bus CAN_H | One half of the differential pair                    |
| Transceiver CAN_L | ↔ bus CAN_L | The other half of the differential pair              |
| 120 Ω resistor    | H to L      | One at **each end** of the bus, and only at the ends |

The bus is a line, not a star. Every node connects to the same CAN_H and CAN_L wires, and the two physical ends each carry a 120 Ω termination resistor. There is no clock wire. With power off, a correctly terminated bus measures about 60 Ω between CAN_H and CAN_L (two 120 Ω resistors in parallel).

### Dominant and recessive

The bus has two states. Typical values for a 5 V transceiver:

| Bus state | Logic level | CAN_H   | CAN_L   | Voltage difference (H − L) |
| --------- | ----------- | ------- | ------- | -------------------------- |
| Recessive | 1           | ≈ 2.5 V | ≈ 2.5 V | ≈ 0 V                      |
| Dominant  | 0           | ≈ 3.5 V | ≈ 1.5 V | ≈ 2 V                      |

If one node drives the bus dominant while another drives it recessive, the bus is dominant. The bus behaves like a wired AND: **a 0 always beats a 1**. This is what makes arbitration possible (section 4). The receiver reads the voltage difference, not the absolute level, so noise that hits both wires equally is rejected.

## 2. The frame on the wire

All nodes share one bit rate, and the frame is built so that receivers can stay synchronized without a clock wire. A standard (11-bit ID) data frame has these fields:

1. **Idle.** The bus rests recessive (1).
2. **SOF** (start of frame). One dominant bit (0). Its falling edge synchronizes every receiver.
3. **Identifier.** 11 bits, **most significant bit first**. It names the message and sets its priority.
4. **RTR, IDE, r0.** Three bits. In a data frame they are all dominant (0): RTR = 0 means data frame, IDE = 0 means an 11-bit ID, and r0 is reserved.
5. **DLC** (data length code). 4 bits giving the number of data bytes (0 to 8).
6. **Data.** 0 to 8 bytes, each sent **most significant bit first**.
7. **CRC.** A 15-bit checksum, followed by a recessive **CRC delimiter**.
8. **ACK slot.** The transmitter sends a recessive bit. Any receiver that got the frame correctly overwrites it with a dominant bit. Then a recessive **ACK delimiter**.
9. **EOF.** 7 recessive bits.
10. **Intermission.** 3 recessive bits before the next frame may start.

Unlike UART, CAN sends the most significant bit first.

### Bit stuffing

From SOF through the end of the CRC, the transmitter inserts a bit of the opposite level after every five consecutive bits of the same level. The receiver removes these **stuff bits**. This guarantees an edge at least every six bits, which the receivers use to stay synchronized.

### Our example frame

The message is ID `0x123` (`001 0010 0011` in 11 bits), DLC = 1, data `0x55` (`0101 0101`). The CRC-15 over SOF through the data is `0x2363` (`010 0011 0110 0011`).

Before stuffing, the bits after SOF and the ID are RTR = 0, IDE = 0, r0 = 0 and DLC = `0001`. That makes five dominant bits in a row (RTR, IDE, r0, and the first two DLC bits), so the transmitter inserts a recessive stuff bit after the second DLC bit.

| Field         | Bits | Value on the wire                                        |
| ------------- | ---- | -------------------------------------------------------- |
| SOF           | 1    | 0                                                        |
| Identifier    | 11   | 0 0 1 0 0 1 0 0 0 1 1                                    |
| RTR, IDE, r0  | 3    | 0 0 0                                                    |
| DLC (part 1)  | 2    | 0 0                                                      |
| **Stuff bit** | 1    | **1**                                                    |
| DLC (part 2)  | 2    | 0 1                                                      |
| Data (`0x55`) | 8    | 0 1 0 1 0 1 0 1                                          |
| CRC           | 15   | 0 1 0 0 0 1 1 0 1 1 0 0 0 1 1                            |
| CRC delimiter | 1    | 1                                                        |
| ACK slot      | 1    | 1 sent, **0** as seen on the bus (receivers acknowledge) |
| ACK delimiter | 1    | 1                                                        |
| EOF           | 7    | 1 1 1 1 1 1 1                                            |
| Intermission  | 3    | 1 1 1                                                    |

The frame is 43 bits up to the end of the CRC (42 plus one stuff bit), then 10 more bits to the end of EOF, so **53 bits**, or 56 with the intermission. At 500 kbit/s one bit lasts 2 µs, so the frame takes about 106 µs. Only 8 of those 53 bits are data bytes. Most of the rest is identification, error checking, and synchronization.

## 3. Inside the transmitter

1. The processor writes the ID, DLC, and data bytes into a **transmit mailbox** (or FIFO entry) and requests transmission.
2. The controller waits until the bus has been idle for the intermission time.
3. The controller builds the frame. Hardware computes the CRC-15 over the unstuffed bits and inserts stuff bits.
4. The **bit-timing logic** divides the controller clock into **time quanta** (tq) and groups them into one bit time. At 500 kbit/s with a 125 ns time quantum, one bit is 16 tq.
5. The controller sends SOF, then the ID, and starts arbitration (section 4). It sends each bit to the transceiver, which drives CAN_H and CAN_L.
6. While sending, the controller **reads the bus back** through RX at every bit's sample point and compares it to what it sent.
7. If the ACK slot comes back dominant, the frame was received. The controller reports "transmit complete". If an error or lost arbitration occurred, most controllers retry automatically.

## 4. Inside the receiver, and how arbitration works

Every node on the bus runs the receive path, including the node that is transmitting.

1. **Hard synchronization.** A recessive-to-dominant edge while the bus is idle marks SOF, and the receiver restarts its bit timing from that edge.
2. **Sample point.** Each bit time is split into a sync segment (1 tq), two segments that absorb propagation delay and phase error, and a final phase segment. In our example the receiver samples at tq 14 of 16, which is 87.5% of the bit.
3. **Resynchronization.** On every later edge, the receiver can lengthen or shorten a segment by a small amount to realign with the sender. Stuff bits guarantee these edges keep coming.
4. **Destuff and shift.** The receiver drops each stuff bit and shifts the remaining bits into its registers.
5. **Check.** It recomputes the CRC and compares. It also checks the fixed-form bits (delimiters, EOF).
6. **Acknowledge.** If everything is correct, the receiver drives the ACK slot dominant. It does this whether or not it wants the message.
7. **Accept or ignore.** **Acceptance filters** compare the ID with the IDs the node cares about. Matching frames go to a receive FIFO or mailbox, and an interrupt tells the processor.

### Arbitration

Any node may start sending when the bus is idle, so two nodes may start in the same bit. They resolve this bit by bit, without corrupting either frame. Suppose node A sends ID `0x123` and node B sends `0x124`:

| ID bit (MSB first) | 1   | 2   | 3   | 4   | 5   | 6   | 7   | 8   | **9** | 10  | 11  |
| ------------------ | --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- |
| Node A (`0x123`)   | 0   | 0   | 1   | 0   | 0   | 1   | 0   | 0   | **0** | 1   | 1   |
| Node B (`0x124`)   | 0   | 0   | 1   | 0   | 0   | 1   | 0   | 0   | **1** | 0   | 0   |
| Bus                | 0   | 0   | 1   | 0   | 0   | 1   | 0   | 0   | **0** | 1   | 1   |

For the first eight bits both nodes send the same value, so nothing happens. In bit 9, node B sends recessive (1) but reads dominant (0) back. Node B concludes that a higher-priority message is on the bus, stops transmitting, and becomes a receiver for that frame. Node A never noticed a conflict and keeps going. Node B retries after the frame ends. **The lowest ID wins**, so IDs double as priorities.

## 5. When it goes wrong

Every node watches every frame, and any node can signal an error.

| Error       | Cause                                                           | What the node sees                                                                               |
| ----------- | --------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| Bit error   | Noise, or a fault on the bus                                    | The transmitter reads back a different level than it sent (outside arbitration and the ACK slot) |
| Stuff error | Noise, or a bit-rate mismatch                                   | Six consecutive bits of the same level                                                           |
| CRC error   | A bit flipped in transit                                        | The computed CRC does not match the received CRC                                                 |
| Form error  | Corrupted frame                                                 | A fixed-form bit (delimiter, EOF) has the wrong level                                            |
| ACK error   | No receiver accepted the frame (no other node, or all in error) | The transmitter sees a recessive bit in the ACK slot                                             |

A node that detects an error sends an **error frame**: an error flag followed by 8 recessive delimiter bits. A node in the normal (_error active_) state sends six dominant bits as its flag, which deliberately violates the stuffing rule so that all other nodes see an error too. An _error passive_ node sends six recessive bits instead, so it cannot disturb other nodes' traffic. The transmitter then resends the frame. Each node keeps a transmit error counter and a receive error counter. A node whose count exceeds 127 becomes error passive, and a transmitter whose count exceeds 255 goes _bus-off_ and stops driving the bus. This keeps one faulty node from blocking everyone else.

### Why bit timing and stuffing matter

UART synchronizes once per byte and then relies on its own clock. CAN frames are much longer, up to about 130 bits with stuffing, so a single synchronization at SOF is not enough. Stuffing forces an edge at least every six bit times, and receivers use each edge to correct their timing. The CAN specification still limits oscillator tolerance (about 1.58% in the worst case), so use a crystal or other accurate clock source. The bit rate also limits the bus length: the signal must travel to the far end and back within one bit time. Typical guidance is about 40 m at 1 Mbit/s and several hundred meters at 125 kbit/s.

## The whole path in one picture

<figure>
  <a href="{{ '/assets/images/visuals/how-can-works.svg' | relative_url }}">
    <img src="{{ '/assets/images/visuals/how-can-works.svg' | relative_url }}"
         alt="Diagram of three CAN nodes on a shared two-wire bus, with a 120 ohm termination resistor at each end. Node A sends a frame with identifier 0x123 and data byte 0x55. A waveform shows the frame bit by bit: start of frame (SOF) 0, the 11 identifier bits, the control bits, the data length code with one inserted recessive stuff bit, data bits 0 1 0 1 0 1 0 1, the 15-bit CRC, and the ACK slot, which Node A sends as 1 and the receivers drive to dominant 0. Five numbered steps explain the process.">
  </a>
  <figcaption>The path of one CAN frame from a transmitting node to the other nodes on the bus. Select the image to open it full size.</figcaption>
</figure>

The five steps in the diagram match the sections above: build the frame (section 3), win arbitration (section 4), transmit on the differential bus (sections 1 and 2), receive, destuff, and check (section 4), and acknowledge and accept (section 4).

## Things to remember

- CAN is a multi-node broadcast bus. Messages carry an ID, not a destination address, and every node sees every frame.
- All nodes must use the same bit rate and compatible bit-timing settings.
- The bus is dominant (0) when any node drives it dominant, so a lower ID wins arbitration.
- CAN sends the most significant bit first, the opposite of UART.
- Bit stuffing keeps edges coming so receivers can resynchronize. The receiver removes the stuff bits.
- The bus needs a 120 Ω termination resistor at each end.
- Hardware does the checking: CRC, ACK, error frames, and automatic retransmission.

{% include visuals-nav.html %}
