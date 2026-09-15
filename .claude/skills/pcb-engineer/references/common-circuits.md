# Common Circuits Reference

Standard subcircuits for PCB designs. Each section includes the circuit
topology, typical component values, selection rationale, and layout notes.

## Table of Contents

1. [Power Supply — Linear Regulators (LDO)](#linear-regulators)
2. [Power Supply — Buck Converters](#buck-converters)
3. [Power Supply — Boost Converters](#boost-converters)
4. [USB Power & Data](#usb-power-and-data)
5. [Protection Circuits](#protection-circuits)
6. [Decoupling Strategy](#decoupling-strategy)
7. [Crystal Oscillator](#crystal-oscillator)
8. [Level Shifting](#level-shifting)
9. [LED Drivers](#led-drivers)
10. [Reset & Supervisory](#reset-and-supervisory)
11. [Debug & Programming Headers](#debug-and-programming-headers)

---

## Linear Regulators

### When to use

- Voltage drop (Vin - Vout) is small (ideally < 1V for LDO)
- Current draw is low to moderate (< 1A typical)
- Noise-sensitive circuits (ADCs, audio, RF) — LDOs produce far cleaner output
  than switching regulators
- Simplicity is valued over efficiency

### Efficiency calculation

Efficiency = Vout / Vin × 100%. An LDO converting 5V to 3.3V is only 66%
efficient — the remaining 34% is dissipated as heat. Calculate power
dissipation: P = (Vin - Vout) × Iload. If P > 0.5W, consider a heatsink pad
or switching regulator instead.

### Standard LDO circuit

```
VIN ──┬──[C_IN]──┐
      │          │
      └──[ LDO ]─┤── VOUT ──┬──[C_OUT]──┐
          │      │           │           │
         EN    GND          LOAD        GND
          │      │                       │
         VIN    GND                     GND
```

**C_IN (input capacitor)**:

- Value: 1µF-10µF ceramic (X5R or X7R dielectric)
- Purpose: supplies transient current to the regulator, stabilises input
- Place within 5mm of the VIN pin
- Voltage rating: ≥ 2× Vin (ceramics lose capacitance at DC bias)

**C_OUT (output capacitor)**:

- Value: 1µF-22µF ceramic (X5R or X7R) — check datasheet for stability
  requirements; some LDOs need minimum ESR for loop stability
- Purpose: output filtering, transient response
- Place within 5mm of the VOUT pin
- Some LDOs (older designs) require a tantalum or electrolytic with specific
  ESR for stability — always check the datasheet

### Recommended LDO parts

| Vout | Part | Package | Max current | Dropout | Features |
|---|---|---|---|---|---|
| 3.3V | AP2112K-3.3 | SOT-23-5 | 600mA | 250mV | Low cost, widely available |
| 3.3V | MIC5504-3.3YM5 | SOT-23-5 | 300mA | 115mV | Very low quiescent current |
| 3.3V | AMS1117-3.3 | SOT-223 | 1A | 1.1V | Not a true LDO, but dirt cheap and everywhere |
| 5.0V | AP2112K-5.0 | SOT-23-5 | 600mA | 250mV | Same family as above |
| 1.8V | AP2112K-1.8 | SOT-23-5 | 600mA | 250mV | Same family |
| Adj | LM1117 | SOT-223 | 800mA | 1.2V | Adjustable via resistor divider |

### Layout notes for LDOs

- Input and output caps must be as close to the IC as possible
- Route the GND trace wide and short — it carries the full load current
- For SOT-223 packages, the large tab is usually the output — solder it to a
  generous copper pad for heatsinking
- Keep high-current input traces short and direct from the power source

## Buck Converters

### When to use

- Voltage step-down with high efficiency needed (>85% typical)
- Moderate to high current (>500mA, or when LDO thermal dissipation is a problem)
- Battery-powered designs where efficiency extends battery life

### Trade-offs vs LDO

Buck converters are more efficient but add complexity (inductor, schottky
diode or synchronous FET, feedback network) and generate switching noise that
couples into nearby analogue signals. Always follow a buck regulator feeding
sensitive loads with an LC filter or LDO post-regulator.

### Standard buck converter circuit

```
VIN ──┬──[C_IN]──┬───────────────────────────┐
      │          │                             │
      │      [BUCK IC]─── SW ──[L]──┬── VOUT ─┤
      │          │                   │         │
      │         BST                [C_OUT]     │
      │          │                   │        LOAD
      │         FB ← [R_TOP]─┬─[R_BOT]─┐      │
      │          │            │         │      │
      │         EN           VOUT      GND    GND
      │          │
      │         VIN
      │          │
      └─────────GND
```

**Inductor selection**:

- Inductance: typically 2.2µH-22µH depending on switching frequency and
  current. Higher frequency allows smaller inductors.
- Saturation current rating: must be ≥ peak current (Iload + 0.5×ΔI_ripple)
- DCR (DC resistance): lower is better for efficiency
- Shielded inductors reduce EMI — prefer shielded for production designs

**Input capacitor**: 10µF-22µF ceramic (X5R/X7R), low ESR. Place directly at
the VIN and GND pins. This cap sees high-frequency pulsed current — use a
quality ceramic, not electrolytic alone.

**Output capacitor**: 22µF-47µF ceramic for low ripple. Additional bulk
electrolytic for energy storage if load has large transients.

**Feedback resistor divider** (adjustable output):

- Vout = Vref × (1 + R_TOP/R_BOT)
- Use 1% resistors. Typical R_BOT = 10k-100kΩ.
- Place divider close to the IC's FB pin, route from the output side of C_OUT

### Recommended buck converter parts

| Vout | Part | Package | Max current | Freq | Notes |
|---|---|---|---|---|---|
| 3.3V | AP3429 | SOT-23-5 | 600mA | 1.4MHz | Tiny, low component count |
| 3.3V | TPS562201 | SOT-23-6 | 2A | 580kHz | Good all-rounder |
| 5V/3.3V | MP2359 | SOT-23-6 | 1.2A | 1.4MHz | Widely available |
| Adj | TPS54331 | SOIC-8 | 3A | 570kHz | Robust, well-documented |
| Adj | LM2596 | TO-263 | 3A | 150kHz | Large but easy, good for beginners |

### Layout notes for buck converters

This is where layout matters most. A badly laid out buck converter will not
meet spec and may oscillate or produce excessive EMI.

- **Hot loop**: the path VIN→IC→inductor→output cap→GND→input cap→VIN carries
  high-frequency pulsed current. Make this loop as small as possible. This is
  the single most important layout rule for switching regulators.
- **Input cap**: directly at VIN and GND pins, on the same layer, short traces
- **Inductor**: connect SW pin to inductor with a short, wide trace
- **Output cap**: at the inductor output, close to the load
- **Feedback**: route from the far side of the output capacitor (Kelvin
  connection) back to the FB pin. Keep this trace away from the SW node.
- **Ground**: use a solid ground plane. Connect all ground pins with short vias
  to the plane. Do not route ground as traces for power circuits.
- **SW node**: keep copper area small to reduce radiated EMI (but wide enough
  for current). Do not route other signals under or near this node.

## Boost Converters

### When to use

- Voltage step-up needed (e.g., 3.3V battery to 5V, or 5V to 12V)
- Single-cell LiPo (3.0-4.2V) to 5V for USB output
- LED backlighting (boosting to LED forward voltage)

### Standard boost circuit

```
VIN ──┬──[C_IN]──┬──[L]──┬── SW (IC) ──┐
      │          │        │              │
      │         GND       └──[D]── VOUT ─┤
      │                          │       │
      │                        [C_OUT]  LOAD
      │                          │       │
      └─────────────────────────GND─────GND
```

Key differences from buck: the inductor is on the input side, and a diode
(Schottky or synchronous FET) blocks reverse current from output to input.

### Recommended boost converter parts

| Application | Part | Package | Max current | Notes |
|---|---|---|---|---|
| 3.3V→5V, low power | TPS61023 | WSON-6 | 1A output | High efficiency at light load |
| LiPo→5V, USB out | TPS61030 | QFN-10 | 4A switch | Powers USB peripherals from battery |
| General purpose | MT3608 | SOT-23-6 | 2A switch | Very cheap, adequate for prototypes |

## USB Power and Data

### USB Type-C connector (power sink, device mode)

For a device that receives power over USB-C:

- CC1 and CC2 pins each need a 5.1kΩ resistor to GND — this tells the source
  "I'm a device, please provide 5V"
- VBUS to your power input through a protection circuit (see Protection section)
- SHIELD to GND through a 1MΩ resistor (provides ESD path without ground loop)

### USB 2.0 data lines

- D+ and D- are a 90Ω differential pair
- Series resistors: 22Ω on each line, placed close to the USB transceiver
  (not at the connector end)
- ESD protection: TVS diode array across D+, D-, and VBUS (e.g., USBLC6-2SC6)
- Keep pair length matched within 0.1mm
- Route as differential pair with controlled impedance

### USB Type-C for USB 2.0 only (no SuperSpeed)

If only using USB 2.0 through a Type-C connector, connect:

- A6 (D+) and B6 (D+) together
- A7 (D-) and B7 (D-) together
- A5 (CC1) through 5.1kΩ to GND
- B5 (CC2) through 5.1kΩ to GND
- A4/B4/A9/B9 (VBUS) all connected together
- A1/B1/A12/B12 (GND) all connected together
- SuperSpeed pins (TX/RX) left unconnected

## Protection Circuits

### ESD protection

Every external-facing signal needs ESD protection. Use TVS diode arrays rated
for IEC 61000-4-2 (±8kV contact, ±15kV air discharge).

| Interface | Recommended part | Package | Notes |
|---|---|---|---|
| USB 2.0 | USBLC6-2SC6 | SOT-23-6 | 2-channel, very common |
| General I/O | PRTR5V0U2X | SOT-363 | 2-channel, ultra-low capacitance |
| Single line | PESD5V0S1BA | SOD-323 | Single unidirectional |

Place TVS diodes as close to the connector as possible, before any series
resistors or other components.

### Reverse polarity protection

For barrel jack or terminal block power inputs where the user might connect
power backwards:

**P-MOSFET method** (recommended): A P-channel MOSFET in the high side.
Gate to input, source to load. When polarity is correct, Vgs is negative and
the FET conducts with very low Rdson loss. When reversed, Vgs is positive and
the FET blocks. Much more efficient than a series diode.

**Series Schottky diode**: simplest method, but drops 0.3-0.5V and wastes
power. Acceptable for prototypes or very low current.

### Overcurrent protection

- **Resettable fuse (PTC)**: self-recovering, good for USB and user-facing
  ports. Select trip current at ~2× normal operating current.
- **TVS + fuse for power input**: combine a fuse for overcurrent with a TVS
  for overvoltage clamping.

### Overvoltage protection

For inputs that might see voltage spikes (automotive 12V, industrial):

- TVS diode (unidirectional) rated just above max normal voltage
- Followed by an LDO or buck converter with adequate input voltage rating

## Decoupling Strategy

This is one of the most important aspects of PCB design for digital circuits.

### The rules

1. **Bulk capacitor at power entry**: 10µF-100µF electrolytic or ceramic at
   each voltage rail's entry point to the board. This is the energy reservoir
   for the entire rail.

2. **Local ceramic at every IC**: one 100nF (0.1µF) ceramic cap per VCC/VDD
   pin, placed within 2-3mm of the pin. For multi-supply ICs (e.g., MCU with
   AVDD, DVDD, VDDIO), each supply pin gets its own cap.

3. **Additional bulk per IC group**: 10µF ceramic shared among a cluster of
   ICs on the same rail, within ~10mm.

4. **High-frequency bypass for fast digital**: 10nF or 1nF ceramic in parallel
   with the 100nF, for ICs with fast edges (>100MHz clock, high-speed ADCs).

5. **Ferrite bead filtering**: between noisy digital supplies and sensitive
   analogue supplies. A ferrite bead + cap forms a low-pass filter that blocks
   high-frequency switching noise.

### Capacitor dielectric selection

| Dielectric | Use for | Avoid for |
|---|---|---|
| C0G/NP0 | Timing circuits, filters, precision — no DC bias derating | Bulk decoupling (too expensive per µF) |
| X5R | General decoupling up to 85°C | High-temp or high-reliability |
| X7R | General decoupling up to 125°C | Precision timing circuits |
| X5R/X7R ceramic | 100nF-22µF decoupling | Values >47µF (use electrolytic) |
| Electrolytic (aluminium) | Bulk capacitance >47µF | High-frequency bypass |
| Tantalum | Bulk with low ESR | Anywhere a short could apply reverse voltage (tantalum caps fail short and can catch fire) |

### DC bias derating warning

Ceramic capacitors (especially X5R/X7R in small packages) lose significant
capacitance when DC voltage is applied. A "10µF" 0402 X5R cap rated for 6.3V
may have only 2-3µF of actual capacitance at 5V DC bias. Always check the
manufacturer's DC bias curves. Solutions:

- Use a higher voltage rating (10V or 16V for a 5V rail)
- Use a larger package size
- Use two caps in parallel

## Crystal Oscillator

### Standard crystal circuit for MCU

```
MCU_OSC_IN ──┬──[C_LOAD1]──GND
             │
          [XTAL]
             │
MCU_OSC_OUT ─┤
             │
          [C_LOAD2]──GND
```

**Load capacitor calculation**:
C_LOAD = 2 × (CL - C_stray)

Where CL is the crystal's specified load capacitance (from datasheet, commonly
12pF-20pF) and C_stray is PCB parasitic capacitance (estimate 2-5pF).

Example: crystal with CL=12pF, C_stray≈3pF → C_LOAD = 2×(12-3) = 18pF.
Use 18pF or nearest standard value (15pF or 18pF).

### Layout notes for crystals

- Place crystal within 5mm of the MCU's oscillator pins
- Route traces short and direct; avoid vias
- Ground pour under the crystal, no other signals routed under it
- Add a ground guard ring around the crystal for noise-sensitive applications
- The crystal is one of the most EMI-sensitive components on the board

## Level Shifting

### 3.3V ↔ 5V bidirectional (I2C)

Use a dual N-MOSFET level shifter (e.g., BSS138-based circuit):

```
3.3V ──[R_PULL_3V3]──┬── LOW_SIDE
                      │
                    D ┤
                   [NMOS]
                    S ┤
                      │
5.0V ──[R_PULL_5V]───┴── HIGH_SIDE
                      │
                     GND (gate)
                      ↑
                     3.3V
```

R_PULL values: 4.7kΩ typical for I2C at 100-400kHz. For faster buses, lower
values (2.2kΩ) but higher power consumption.

For convenience, use a pre-built level shifter IC like TXB0104 (4-bit
bidirectional) or TXS0102 (2-bit, I2C compatible).

### Unidirectional (e.g., SPI MOSI 3.3V→5V)

Simple voltage divider for high-to-low: two resistors.
Buffer IC (74LVC1T45) for low-to-high with proper drive strength.

## LED Drivers

### Simple indicator LED

```
GPIO ──[R_SERIES]──[LED]──GND
```

R_SERIES = (Vgpio - Vf_led) / I_led

Typical values:

- Red LED: Vf≈1.8V, I=5-10mA for indicator → R = (3.3-1.8)/0.005 = 300Ω (use 330Ω)
- Green LED: Vf≈2.2V → R = (3.3-2.2)/0.005 = 220Ω
- Blue/white LED: Vf≈3.0V → R = (3.3-3.0)/0.005 = 60Ω (marginal on 3.3V, consider 5V supply)

For PWM dimming, ensure the GPIO can source the LED current. Most MCU pins
can source 5-20mA; check the datasheet.

## Reset and Supervisory

### Standard MCU reset circuit

```
VCC ──[R_PULL]──┬── RESET_N (MCU)
                │
              [C]──GND
                │
             [BUTTON]──GND  (optional manual reset)
```

R_PULL: 10kΩ typical
C: 100nF — provides power-on delay and noise filtering
Button: momentary tactile switch for manual reset

For production designs, consider a voltage supervisor IC (e.g., MCP130,
TPS3839) that holds reset until VCC is stable and above the MCU's minimum
operating voltage. This prevents brownout-related corruption.

## Debug and Programming Headers

### ARM SWD (Serial Wire Debug) — most common for STM32, nRF, RP2040

Minimum 4-pin header:

1. VCC (target voltage reference, not power supply)
2. GND
3. SWDIO (data, bidirectional)
4. SWCLK (clock)

Optional additions:
5. RESET (nRST)
6. SWO (Serial Wire Output, for trace/printf debugging)

Standard 10-pin Cortex Debug Connector (1.27mm pitch, 2×5):
Pin 1=VCC, 2=SWDIO, 3=GND, 4=SWCLK, 5=GND, 6=SWO, 7=key(NC),
8=NC, 9=GND, 10=nRST

### UART debug header

3-pin minimum: TX, RX, GND. Add VCC for reference. Use 2.54mm pitch pin
header for easy connection to USB-UART adapters (e.g., FTDI, CP2102).

### ISP/ICSP (AVR, PIC)

6-pin 2×3 header at 2.54mm pitch:
1=MISO, 2=VCC, 3=SCK, 4=MOSI, 5=RST, 6=GND

### JTAG (larger ARM, FPGA)

Standard 20-pin ARM JTAG (2×10, 2.54mm pitch):
Includes TDI, TDO, TMS, TCK, nTRST, nSRST, and multiple GND pins.
Consider TagConnect pogo-pin footprints for production boards to save space.
