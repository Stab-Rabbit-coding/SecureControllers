# Connector Pinouts Reference

Standard pinouts for common connectors used in PCB designs.

## Table of Contents

1. [USB Type-C](#usb-type-c)
2. [USB Type-A & Micro-B](#usb-type-a-and-micro-b)
3. [Pin Headers (2.54mm)](#pin-headers)
4. [JST Connectors](#jst-connectors)
5. [Barrel Jack / DC Power](#barrel-jack)
6. [SD Card](#sd-card)
7. [I2C Header](#i2c-header)
8. [SPI Header](#spi-header)
9. [UART Header](#uart-header)
10. [JTAG and SWD](#jtag-and-swd)
11. [Ethernet (RJ45)](#ethernet)
12. [Audio Jack (3.5mm)](#audio-jack)

---

## USB Type-C

### Full pinout (24-pin receptacle)

| Pin | Name | Function | Notes |
|---|---|---|---|
| A1 | GND | Ground | |
| A2 | SSTXp1 | SuperSpeed TX+ | USB 3.x only |
| A3 | SSTXn1 | SuperSpeed TX- | USB 3.x only |
| A4 | VBUS | Power (+5V to +20V) | |
| A5 | CC1 | Configuration Channel 1 | 5.1kΩ to GND for UFP (device) |
| A6 | Dp1 | USB 2.0 D+ | |
| A7 | Dn1 | USB 2.0 D- | |
| A8 | SBU1 | Sideband Use 1 | Alt mode (DisplayPort, etc.) |
| A9 | VBUS | Power | |
| A10 | SSRXn2 | SuperSpeed RX- | USB 3.x only |
| A11 | SSRXp2 | SuperSpeed RX+ | USB 3.x only |
| A12 | GND | Ground | |
| B1 | GND | Ground | |
| B2 | SSTXp2 | SuperSpeed TX+ | USB 3.x only |
| B3 | SSTXn2 | SuperSpeed TX- | USB 3.x only |
| B4 | VBUS | Power | |
| B5 | CC2 | Configuration Channel 2 | 5.1kΩ to GND for UFP (device) |
| B6 | Dp2 | USB 2.0 D+ | |
| B7 | Dn2 | USB 2.0 D- | |
| B8 | SBU2 | Sideband Use 2 | Alt mode |
| B9 | VBUS | Power | |
| B10 | SSRXn1 | SuperSpeed RX- | USB 3.x only |
| B11 | SSRXp1 | SuperSpeed RX+ | USB 3.x only |
| B12 | GND | Ground | |

### USB 2.0-only Type-C (simplified wiring)

For devices that only need USB 2.0 through a Type-C connector, connect:

- All VBUS pins together (A4, A9, B4, B9)
- All GND pins together (A1, A12, B1, B12)
- D+ pins together (A6, B6)
- D- pins together (A7, B7)
- CC1 (A5): 5.1kΩ to GND
- CC2 (B5): 5.1kΩ to GND
- SHIELD: 1MΩ to GND (optional 4.7nF cap in parallel for HF noise)
- All SuperSpeed and SBU pins: leave unconnected (NC)

### USB-C as power sink only (no data)

If using USB-C only for 5V power (no data lines):

- VBUS pins → power input
- GND pins → ground
- CC1: 5.1kΩ to GND
- CC2: 5.1kΩ to GND
- All other pins: NC
- This configuration draws up to 5V/3A (15W) per USB-C spec

For USB Power Delivery (>5V), a PD controller IC is needed (e.g., FUSB302,
STUSB4500) — this is significantly more complex.

## USB Type-A and Micro-B

### USB Type-A receptacle (host)

| Pin | Name | Notes |
|---|---|---|
| 1 | VBUS (+5V) | Provide 500mA (USB 2.0) or 900mA (USB 3.0) |
| 2 | D- | |
| 3 | D+ | |
| 4 | GND | |
| Shell | Shield | Connect to GND via 1MΩ |

### USB Micro-B receptacle (device)

| Pin | Name | Notes |
|---|---|---|
| 1 | VBUS (+5V) | Power input from host |
| 2 | D- | |
| 3 | D+ | |
| 4 | ID | GND for OTG host, float for device |
| 5 | GND | |
| Shell | Shield | 1MΩ to GND |

## Pin Headers

Standard 2.54mm (0.1") pitch pin headers. KiCad library naming:
`Connector_PinHeader_2.54mm:PinHeader_1xNN_P2.54mm_Vertical`

Use for prototyping, debug, and low-density board-to-board connections.
Not suitable for high-vibration or production environments — use latching
connectors (JST, Molex) instead.

### Common configurations

| Use | Pins | Typical labelling |
|---|---|---|
| Power breakout | 2-pin | VCC, GND |
| UART debug | 3-pin | TX, RX, GND |
| I2C breakout | 4-pin | VCC, GND, SDA, SCL |
| SPI breakout | 5-pin | VCC, GND, SCK, MOSI, MISO + CS on separate pin |
| SWD programming | 4-pin | VCC, GND, SWDIO, SWCLK |
| General GPIO | 1×N | Label by function |

## JST Connectors

Latching connectors for production designs. Common families:

### JST-PH (2.0mm pitch)

Most common for battery connections, small board-to-board.
KiCad: `Connector_JST:JST_PH_B{N}B-PH-K_1x{N}_P2.00mm_Vertical`

| Pins | Common use |
|---|---|
| 2-pin (PH-2) | LiPo battery connection (standard in hobby market) |
| 3-pin (PH-3) | Servo motors, sensor with power |
| 4-pin (PH-4) | I2C with power (Qwiic/STEMMA QT use this) |

### JST-SH (1.0mm pitch)

Smaller, used for Qwiic/STEMMA QT I2C ecosystem.
Pin order for Qwiic: GND, VCC (3.3V), SDA, SCL

### JST-XH (2.5mm pitch)

Larger, common for internal power connections, LED strips, multi-cell battery
balance connectors.

## Barrel Jack

### Standard DC barrel jack (2.1mm/5.5mm)

Centre pin: positive (standard convention, but ALWAYS mark polarity on PCB)
Outer barrel: negative/ground

KiCad footprint: `Connector_BarrelJack:BarrelJack_Horizontal`

Three-pin variant (switched):

| Pin | Name | Notes |
|---|---|---|
| 1 | Tip (centre) | Positive |
| 2 | Sleeve (barrel) | Negative/GND |
| 3 | Switch | Connected to tip when no jack inserted; disconnects when jack inserted. Use for battery/USB fallback. |

## SD Card

### Micro SD (push-push type, most common)

| Pad | Name | SPI mode | SDIO mode |
|---|---|---|---|
| 1 | DAT2 | NC | Data 2 |
| 2 | CD/DAT3 | CS | Data 3 |
| 3 | CMD | MOSI (DI) | Command |
| 4 | VDD | 3.3V | 3.3V |
| 5 | CLK | SCK | Clock |
| 6 | VSS | GND | GND |
| 7 | DAT0 | MISO (DO) | Data 0 |
| 8 | DAT1 | NC | Data 1 |
| CD | Card Detect | Switch to GND when card inserted |

SPI mode is simpler (4 wires) but slower. SDIO mode (4-bit) is faster but
needs more pins and a more complex driver. For MCUs without native SDIO
peripheral, use SPI mode.

Add a 10µF decoupling cap on VDD close to the socket — SD cards have high
transient current demands.

## I2C Header

Standard 4-pin breakout (compatible with Qwiic/STEMMA QT ecosystem):

| Pin | Name | Notes |
|---|---|---|
| 1 | GND | Ground |
| 2 | VCC | 3.3V (Qwiic) or 5V (some boards) |
| 3 | SDA | Data — needs pull-up (4.7kΩ to VCC typical) |
| 4 | SCL | Clock — needs pull-up (4.7kΩ to VCC typical) |

I2C pull-ups: only one set per bus, not per device. If breaking out to
multiple devices, put pull-ups on the main board only.

## SPI Header

Standard 6-pin breakout:

| Pin | Name | Notes |
|---|---|---|
| 1 | VCC | Power |
| 2 | GND | Ground |
| 3 | SCK | Clock (master output) |
| 4 | MOSI | Master Out Slave In |
| 5 | MISO | Master In Slave Out |
| 6 | CS | Chip Select (active low, one per device) |

Note: the naming MOSI/MISO is being replaced by SDO/SDI or COPI/CIPO in
newer documentation. Both conventions are in wide use.

## UART Header

### Minimal 3-pin

| Pin | Name | Notes |
|---|---|---|
| 1 | GND | Ground (connect first) |
| 2 | TX | Transmit (from this board) |
| 3 | RX | Receive (to this board) |

Cross-connect: this board's TX goes to the adapter's RX, and vice versa.

### 6-pin FTDI-compatible

Compatible with FTDI TTL-232R-3V3 cable and many USB-UART adapters:

| Pin | Name | Direction | Notes |
|---|---|---|---|
| 1 | GND | — | Black wire on FTDI cable |
| 2 | CTS | Input | Clear to send (optional, can tie to GND) |
| 3 | VCC | Output | 3.3V or 5V from adapter (do not use as power source for board) |
| 4 | TX | Output | From this board to adapter |
| 5 | RX | Input | From adapter to this board |
| 6 | RTS | Output | Request to send (optional, can be used for auto-reset) |

## JTAG and SWD

### ARM SWD 10-pin Cortex Debug Connector (1.27mm pitch, 2×5)

| Pin | Name | Notes |
|---|---|---|
| 1 | VTref | Target voltage reference (not power supply) |
| 2 | SWDIO | Serial Wire Data I/O |
| 3 | GND | |
| 4 | SWCLK | Serial Wire Clock |
| 5 | GND | |
| 6 | SWO | Serial Wire Output (optional, for trace) |
| 7 | — | Key (no pin, for keying the connector) |
| 8 | NC | Not connected |
| 9 | GNDdetect | GND (active low target detection) |
| 10 | nRESET | Target reset (active low) |

KiCad footprint: `Connector_PinHeader_1.27mm:PinHeader_2x05_P1.27mm_Vertical`
or use Tag-Connect `TC2050-IDC` for production (no header needed on board).

### Minimal 4-pin SWD

For space-constrained designs, a 4-pin 2.54mm header is sufficient:

| Pin | Name |
|---|---|
| 1 | VCC |
| 2 | GND |
| 3 | SWDIO |
| 4 | SWCLK |

Add nRESET on a 5th pin if the MCU's SWD interface requires it for recovery
from deep sleep or lockout.

## Ethernet

### RJ45 with integrated magnetics

Most RJ45 jacks for PCB mounting include built-in isolation transformers
(magnetics). These are strongly recommended — external discrete transformers
are fiddly and take more space.

Standard Ethernet PHY to RJ45 wiring (100BASE-TX):

| RJ45 pin | Signal | PHY connection |
|---|---|---|
| 1 | TX+ | Through magnetics to PHY TXP |
| 2 | TX- | Through magnetics to PHY TXN |
| 3 | RX+ | Through magnetics to PHY RXP |
| 4 | — | Unused (100BASE-TX) or pair for 1000BASE-T |
| 5 | — | Unused or pair for 1000BASE-T |
| 6 | RX- | Through magnetics to PHY RXN |
| 7 | — | Unused or pair for 1000BASE-T |
| 8 | — | Unused or pair for 1000BASE-T |

LED pins on the jack connect to PHY status outputs (link, activity).

## Audio Jack

### 3.5mm TRRS (4-pole, headset with mic)

| Contact | CTIA standard | OMTP standard |
|---|---|---|
| Tip (T) | Left audio | Left audio |
| Ring 1 (R1) | Right audio | Right audio |
| Ring 2 (R2) | Ground | Microphone |
| Sleeve (S) | Microphone | Ground |

**CTIA** is the dominant standard (Apple, most Android). OMTP is older
(some Samsung, Nokia). Default to CTIA unless the user specifies otherwise.

Series resistors (33Ω) on audio outputs protect against short circuits when
the jack is partially inserted. AC coupling capacitors (10µF-47µF) block DC
offset from the audio DAC.
