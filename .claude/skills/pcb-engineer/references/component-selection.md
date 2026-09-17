# Component Selection Guide

Decision framework for selecting electronic components. Covers methodology,
package types, derating, and finding alternatives.

## Table of Contents

1. [Selection Methodology](#selection-methodology)
2. [Package Types & Sizes](#package-types-and-sizes)
3. [Derating Guidelines](#derating-guidelines)
4. [Passive Component Selection](#passive-component-selection)
5. [Microcontroller Selection](#microcontroller-selection)
6. [Voltage Regulator Selection](#voltage-regulator-selection)
7. [Finding Alternative Parts](#finding-alternative-parts)
8. [Preferred Manufacturer List](#preferred-manufacturer-list)

---

## Selection Methodology

For every component, evaluate in this order:

1. **Does it meet the electrical spec?** Voltage rating, current rating,
   tolerance, bandwidth, impedance — whatever the circuit requires.
2. **Does the package fit the design?** Physical size, pad pitch compatible
   with fab capabilities, thermal performance adequate.
3. **Is it available?** Check stock at major distributors. If a part has <1000
   units in stock at all major distributors combined, look for alternatives
   immediately.
4. **Is it affordable at volume?** Check pricing at 1pc (prototype), 100pc,
   and 1000pc. Flag parts that are disproportionately expensive.
5. **Is it second-sourced?** At least one alternative should exist. Single-
   source components are a supply chain risk.
6. **Is it mature and well-documented?** New parts with sparse documentation
   and no application notes are riskier. Prefer parts with good datasheets,
   reference designs, and community experience.

### Red flags

- Part only available from one obscure distributor
- Datasheet is poorly written or incomplete
- No reference design or evaluation board available
- Part is marked "NRND" (Not Recommended for New Designs) or "EOL" (End of Life)
- Only available in packages too small for the user's soldering capability
- Lead time >12 weeks without alternatives

## Package Types and Sizes

### SMD passive packages (resistors, capacitors)

| Package code | Size (mm) | Size (mil) | Good for |
| --- | --- | --- | --- |
| 0201 | 0.6×0.3 | 24×12 | Very dense pro boards; impossible to hand-solder |
| 0402 | 1.0×0.5 | 40×20 | Dense designs; challenging but possible to hand-solder |
| 0603 | 1.6×0.8 | 63×31 | Good general-purpose; manageable with steady hands |
| 0805 | 2.0×1.25 | 79×49 | Recommended for beginners; easy to hand-solder |
| 1206 | 3.2×1.6 | 126×63 | Large, easy to solder; higher power handling |
| 2512 | 6.3×3.2 | 250×125 | High-power resistors, current sense |

**Recommendation for learners**: Use 0805 for most passives. Switch to 0603
for space-constrained areas. Avoid 0402 and smaller unless using assembly
service.

### IC packages

| Package | Pitch | Pins | Hand-solderable? | Notes |
| --- | --- | --- | --- | --- |
| SOT-23 / SOT-23-5/6 | 0.95mm | 3-6 | Yes | Small transistors, regulators |
| SOT-223 | 2.3mm | 3+tab | Yes, easy | Regulators with thermal tab |
| SOIC-8/14/16 | 1.27mm | 8-16 | Yes | Standard logic, op-amps |
| SSOP | 0.65mm | 8-48 | Possible | Tighter pitch than SOIC |
| TQFP | 0.5mm/0.8mm | 32-100+ | Tricky | MCUs, mid-complexity ICs |
| QFN/DFN | 0.5mm/0.65mm | 8-64+ | Difficult | Pads underneath, needs reflow |
| BGA | 0.4-1.0mm ball pitch | 16-1000+ | No | Requires professional assembly |

**Recommendation for learners**: Prefer SOIC and SOT-23 family. TQFP is
manageable with flux and patience. QFN is fine if using an assembly service
(JLCPCB SMT assembly handles QFN well). Avoid BGA unless necessary.

### Through-hole vs SMD

Through-hole (THT) is easier to hand-solder but takes more board space and
cannot be auto-assembled as cheaply. Use THT for:

- Pin headers and programming connectors
- Large electrolytic capacitors
- Connectors with mechanical stress (barrel jacks, USB-A)
- Prototyping and learning

Use SMD for everything else in production designs.

## Derating Guidelines

Never operate a component at its absolute maximum rating. Derating provides
safety margin against temperature variation, ageing, and transient stress.

| Parameter | Derating rule |
| --- | --- |
| Voltage (capacitor) | Rate for ≤50% of rated voltage (ceramics), ≤80% (electrolytics) |
| Voltage (semiconductor) | Rate for ≤80% of absolute max Vds/Vce/Vr |
| Current (continuous) | Rate for ≤80% of rated current |
| Power (resistor) | Rate for ≤50% of rated power |
| Temperature | Ensure operating temp stays ≤80% of max junction temp |
| Capacitance (ceramic) | Account for DC bias derating and temperature derating |

Example: a 10V-rated 10µF X5R 0805 capacitor at 5V DC bias may only provide
5-6µF actual capacitance. If you need 10µF at 5V, either use a 16V-rated cap
or use two 10µF caps in parallel.

## Passive Component Selection

### Resistors

| Application | Tolerance | Type | Notes |
| --- | --- | --- | --- |
| Pull-up/pull-down | 5% | Thick film | Value not critical |
| Voltage divider (non-precision) | 1% | Thick film | Standard for most uses |
| Feedback divider (regulator) | 1% | Thick film | Affects output voltage accuracy |
| Current sense | 1% or 0.1% | Metal film or metal element | Low TCR important |
| High precision (ADC reference) | 0.1% | Thin film | Low TCR, low noise |

Preferred series: E96 (1%) or E24 (5%). Standard values within E96:
10, 10.2, 10.5, 10.7, 11.0, 11.3, ... (geometric progression).

### Capacitors

Selection priority:

1. What capacitance is needed? (from circuit design)
2. What voltage rating? (≥2× operating for ceramic, ≥1.25× for electrolytic)
3. What dielectric? (C0G for precision, X5R/X7R for decoupling)
4. What package fits? (0805 for general, smaller for dense areas)
5. DC bias derating acceptable? (check manufacturer curves)

### Inductors

For power inductors (buck/boost converters):

1. Required inductance from converter design
2. Saturation current ≥ peak current with 20% margin
3. RMS current ≥ average current
4. DCR as low as practical for efficiency
5. Shielded construction preferred for EMI

For signal inductors (filters, matching):

1. Inductance value with tight tolerance
2. Self-resonant frequency (SRF) well above operating frequency
3. Q factor if used in resonant circuits

## Microcontroller Selection

### Decision framework

Questions to answer first:

1. **Processing power needed?** Simple GPIO + UART → 8-bit AVR. Moderate
   (sensor fusion, display) → ARM Cortex-M0/M3. Heavy (DSP, connectivity
   stacks) → Cortex-M4/M7.
2. **Peripherals needed?** Count: UARTs, SPI, I2C, ADC channels, timers, PWM
   channels, USB, CAN, Ethernet.
3. **GPIO count?** Count all needed I/O pins, add 10-20% margin for future
   expansion.
4. **Memory?** Flash for code (64KB is generous for simple projects, 256KB+
   for complex firmware with libraries), RAM for runtime data.
5. **Development ecosystem?** Arduino-compatible matters for beginners.
   Manufacturer IDE/SDK quality matters for production.
6. **Power consumption?** Battery-powered → look at sleep mode current.
7. **Availability and cost?** The global chip shortage taught hard lessons.
   Pick parts that are multi-sourced or from large product families.

### Common MCU families

| Family | Core | Good for | Ecosystem | Beginner-friendly? |
| --- | --- | --- | --- | --- |
| ATmega328P | AVR 8-bit | Simple projects, Arduino | Arduino IDE | Very |
| RP2040 | Dual Cortex-M0+ | General purpose, USB, PIO | MicroPython, C SDK | Yes |
| STM32F103 | Cortex-M3 | Moderate complexity | STM32CubeIDE, Arduino | Moderate |
| STM32F4xx | Cortex-M4F | DSP, audio, motor control | STM32CubeIDE | Moderate |
| ESP32-S3 | Dual Xtensa LX7 | WiFi + BLE projects | Arduino, ESP-IDF | Yes |
| nRF52840 | Cortex-M4F | BLE, low power | Zephyr, nRF Connect | Moderate |
| SAMD21 | Cortex-M0+ | USB, Arduino-compatible | Arduino, ASF4 | Yes |

### Recommendation for new users

The **RP2040** is an excellent starting point: dual-core, flexible I/O (PIO
state machines), USB native, very well documented, cheap (~$0.70), and
available in QFN-56 (assembly service) or pre-mounted on Pico/Pico W modules
for prototyping. Massive community and library support.

For wireless: **ESP32-S3** (WiFi+BLE) or **nRF52840** (BLE, ultra-low power).

## Voltage Regulator Selection

### Decision tree

```text
Start
  │
  ├─ Is (Vin - Vout) > 2V AND Iload > 200mA?
  │    ├─ Yes → Buck converter (efficiency matters)
  │    └─ No → LDO is fine
  │
  ├─ Is the load noise-sensitive (ADC, audio, RF)?
  │    ├─ Yes → LDO, or buck + LDO post-regulator
  │    └─ No → Buck converter for efficiency
  │
  ├─ Need Vout > Vin?
  │    ├─ Yes → Boost converter
  │    └─ No → Buck or LDO
  │
  └─ Battery powered, need maximum runtime?
       ├─ Yes → Buck converter with low quiescent current
       └─ No → LDO for simplicity
```

See `common-circuits.md` for specific part recommendations and circuits.

## Finding Alternative Parts

### Compatibility levels

1. **Drop-in replacement**: same pinout, same package, same or better specs.
   Can substitute with no board or schematic changes.
   Example: AP2112K-3.3 → XC6220B331MR (both SOT-23-5, same pinout, 3.3V LDO)

2. **Equivalent, re-pin**: same function, same package size, but different
   pinout. Requires schematic change and potentially new footprint or trace
   rerouting.
   Example: AMS1117-3.3 (SOT-223) → LD1117S33CTR (SOT-223, same footprint
   but verify pinout — some SOT-223 LDOs swap GND and VOUT positions)

3. **Equivalent, re-size**: same function, different package. Requires new
   footprint and PCB layout changes.
   Example: AP2112K-3.3 (SOT-23-5) → MIC5504-3.3YM5 (SOT-23-5, drop-in) vs
   MIC5365-3.3YC5 (SC-70-5, smaller package, new footprint)

### How to find alternatives

1. Check the manufacturer's product page — they often list pin-compatible parts
   from their own portfolio
2. Use parametric search on DigiKey/Mouser: filter by function, package,
   voltage, current, sort by stock
3. Cross-reference databases: Octopart consolidates stock/pricing across
   distributors
4. For passive components: alternatives are usually straightforward — same
   value, same package, different manufacturer
5. For ICs: read the alternative's datasheet completely. "Pin-compatible" claims
   sometimes differ in subtle ways (enable pin polarity, thermal pad connection,
   output voltage tolerance)

### Warning about counterfeit parts

When sourcing from non-authorised channels (AliExpress, eBay, etc.), counterfeit
components are a real risk, especially for popular MCUs and voltage regulators.
For production designs, always source from authorised distributors (DigiKey,
Mouser, Farnell/Newark, LCSC for JLCPCB assembly). For prototyping, the risk
is lower but still present — if something behaves strangely, consider that the
part itself may be fake.

## Preferred Manufacturer List

These manufacturers are well-established, widely stocked, and produce reliable
components. This is not exhaustive but gives a starting point:

| Category | Recommended manufacturers |
| --- | --- |
| Resistors | Yageo, Samsung, Panasonic, Vishay, KOA |
| Capacitors (ceramic) | Samsung, Murata, Yageo, TDK, Kemet |
| Capacitors (electrolytic) | Nichicon, Panasonic, Rubycon, Wurth |
| Inductors (power) | Wurth, Bourns, Coilcraft, TDK, Murata |
| Voltage regulators | Texas Instruments, Diodes Inc, Microchip, ON Semi, Richtek |
| MCUs | STMicroelectronics, Raspberry Pi (RP2040), Espressif, Nordic Semi, Microchip/Atmel |
| MOSFETs | Nexperia, Infineon, ON Semi, Diodes Inc |
| ESD protection | Nexperia, ON Semi, STMicroelectronics, Littelfuse |
| Connectors | Molex, TE Connectivity, Amphenol, JST, Wurth |
| Crystals | Abracon, ECS, TXC, Murata |
