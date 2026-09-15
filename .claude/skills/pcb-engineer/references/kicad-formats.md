# KiCad File Formats Reference

Reference for generating KiCad 8.x project files programmatically.

## Table of Contents

1. [Project Structure](#project-structure)
2. [S-Expression Syntax](#s-expression-syntax)
3. [Schematic Format (.kicad_sch)](#schematic-format)
4. [Symbol Library Format (.kicad_sym)](#symbol-library-format)
5. [PCB Format (.kicad_pcb)](#pcb-format)
6. [Footprint Format (.kicad_mod)](#footprint-format)
7. [Project File (.kicad_pro)](#project-file)
8. [Common Patterns](#common-patterns)

---

## Project Structure

A KiCad 8 project directory typically contains:

```
project-name/
├── project-name.kicad_pro    # Project settings (JSON)
├── project-name.kicad_sch    # Root schematic (S-expression)
├── project-name.kicad_pcb    # PCB layout (S-expression)
├── sym-lib-table              # Symbol library table
├── fp-lib-table               # Footprint library table
└── project-name-backups/      # Auto-backups
```

## S-Expression Syntax

KiCad files (except .kicad_pro) use S-expressions — nested parenthesised
lists. The general form is:

```
(keyword value ...)
(keyword (sub-keyword value ...) ...)
```

Strings containing spaces or special characters must be double-quoted.
Numbers are written without quotes. UUIDs are used as unique identifiers
throughout.

Generate UUIDs as standard v4 UUIDs (lowercase hex, 8-4-4-4-12 format).

Coordinates use millimetres. Origin (0,0) is top-left for schematics and
the board origin for PCBs. Angles are in degrees, counter-clockwise positive.

## Schematic Format

File extension: `.kicad_sch`

### Minimal valid schematic

```
(kicad_sch
  (version 20231120)
  (generator "pcb-engineer-skill")
  (generator_version "1.0")
  (uuid "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")
  (paper "A4")

  (lib_symbols
    ;; Embedded copies of all symbols used in this schematic
  )

  ;; Components, wires, labels, power symbols go here
)
```

### Symbol instance (placing a component)

```
(symbol
  (lib_id "Device:R")
  (at 100 50 0)          ;; x, y, rotation in degrees
  (unit 1)
  (exclude_from_sim no)
  (in_bom yes)
  (on_board yes)
  (dnp no)
  (uuid "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")
  (property "Reference" "R1"
    (at 100 48 0)
    (effects (font (size 1.27 1.27)) (justify left))
  )
  (property "Value" "10k"
    (at 100 52 0)
    (effects (font (size 1.27 1.27)) (justify left))
  )
  (property "Footprint" "Resistor_SMD:R_0402_1005Metric"
    (at 100 50 0)
    (effects (font (size 1.27 1.27)) hide)
  )
  (property "Datasheet" ""
    (at 100 50 0)
    (effects (font (size 1.27 1.27)) hide)
  )
  (property "MPN" "RC0402FR-0710KL"
    (at 100 50 0)
    (effects (font (size 1.27 1.27)) hide)
  )
  (instances
    (project "project-name"
      (path "/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
        (reference "R1")
        (unit 1)
      )
    )
  )
)
```

### Wire

```
(wire
  (pts
    (xy 100 50)
    (xy 120 50)
  )
  (stroke (width 0) (type default))
  (uuid "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")
)
```

### Net label

```
(label "VCC_3V3"
  (at 110 50 0)
  (effects (font (size 1.27 1.27)))
  (uuid "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")
)
```

### Global label (for inter-sheet connections)

```
(global_label "SDA"
  (shape bidirectional)
  (at 120 60 0)
  (effects (font (size 1.27 1.27)))
  (uuid "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")
  (property "Intersheets" ""
    (at 0 0 0)
    (effects (font (size 1.27 1.27)) hide)
  )
)
```

### Power symbol

```
(symbol
  (lib_id "power:GND")
  (at 100 70 0)
  (unit 1)
  (exclude_from_sim no)
  (in_bom yes)
  (on_board yes)
  (dnp no)
  (uuid "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")
  (property "Reference" "#PWR01"
    (at 100 76 0)
    (effects (font (size 1.27 1.27)) hide)
  )
  (property "Value" "GND"
    (at 100 74 0)
    (effects (font (size 1.27 1.27)))
  )
  (instances
    (project "project-name"
      (path "/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
        (reference "#PWR01")
        (unit 1)
      )
    )
  )
)
```

### Hierarchical sheet (sub-schematic)

```
(sheet
  (at 150 80)
  (size 20 15)
  (fields_autoplaced yes)
  (stroke (width 0.1524) (type solid))
  (fill (color 0 0 0 0.0000))
  (uuid "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")
  (property "Sheetname" "Power Supply"
    (at 150 79 0)
    (effects (font (size 1.27 1.27)) (justify left bottom))
  )
  (property "Sheetfile" "power_supply.kicad_sch"
    (at 150 96 0)
    (effects (font (size 1.27 1.27)) (justify left top))
  )
  (pin "VIN" input
    (at 150 85 180)
    (effects (font (size 1.27 1.27)) (justify left))
    (uuid "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")
  )
)
```

## Symbol Library Format

File extension: `.kicad_sym`

Used for custom symbols not in KiCad's standard libraries.

```
(kicad_symbol_lib
  (version 20231120)
  (generator "pcb-engineer-skill")
  (generator_version "1.0")

  (symbol "MyChip"
    (exclude_from_sim no)
    (in_bom yes)
    (on_board yes)
    (property "Reference" "U"
      (at 0 10 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Value" "MyChip"
      (at 0 -10 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Footprint" ""
      (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Datasheet" "https://example.com/datasheet.pdf"
      (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )

    (symbol "MyChip_0_1"
      ;; Graphics (body outline)
      (rectangle
        (start -5.08 7.62)
        (end 5.08 -7.62)
        (stroke (width 0.254) (type default))
        (fill (type background))
      )
    )

    (symbol "MyChip_1_1"
      ;; Pins for unit 1
      (pin input line
        (at -7.62 5.08 0)     ;; position and rotation
        (length 2.54)
        (name "VIN" (effects (font (size 1.27 1.27))))
        (number "1" (effects (font (size 1.27 1.27))))
      )
      (pin output line
        (at 7.62 5.08 180)
        (length 2.54)
        (name "VOUT" (effects (font (size 1.27 1.27))))
        (number "3" (effects (font (size 1.27 1.27))))
      )
      (pin power_in line
        (at 0 -10.16 90)
        (length 2.54)
        (name "GND" (effects (font (size 1.27 1.27))))
        (number "2" (effects (font (size 1.27 1.27))))
      )
    )
  )
)
```

### Pin types

Use the correct pin type for accurate ERC (Electrical Rule Check):

| Type | Use for |
|---|---|
| `input` | Digital/analogue inputs |
| `output` | Digital/analogue outputs |
| `bidirectional` | I2C SDA, data bus lines |
| `tri_state` | Outputs with high-Z state |
| `passive` | Resistors, capacitors, inductors |
| `power_in` | VCC, VDD, GND pins on ICs |
| `power_out` | Regulator output, power source |
| `unconnected` | No-connect pins |
| `free` | Pins that can connect to anything |

## PCB Format

File extension: `.kicad_pcb`

### Minimal valid PCB

```
(kicad_pcb
  (version 20240108)
  (generator "pcb-engineer-skill")
  (generator_version "1.0")

  (general
    (thickness 1.6)        ;; Board thickness in mm
    (legacy_teardrops no)
  )

  (paper "A4")

  (layers
    (0 "F.Cu" signal)
    (31 "B.Cu" signal)
    (32 "B.Adhes" user "B.Adhesive")
    (33 "F.Adhes" user "F.Adhesive")
    (34 "B.Paste" user)
    (35 "F.Paste" user)
    (36 "B.SilkS" user "B.Silkscreen")
    (37 "F.SilkS" user "F.Silkscreen")
    (38 "B.Mask" user "B.Mask")
    (39 "F.Mask" user "F.Mask")
    (40 "Dwgs.User" user "User.Drawings")
    (41 "Cmts.User" user "User.Comments")
    (42 "Eco1.User" user "User.Eco1")
    (43 "Eco2.User" user "User.Eco2")
    (44 "Edge.Cuts" user)
    (45 "Margin" user)
    (46 "B.CrtYd" user "B.Courtyard")
    (47 "F.CrtYd" user "F.Courtyard")
    (48 "B.Fab" user "B.Fabrication")
    (49 "F.Fab" user "F.Fabrication")
  )

  (setup
    (pad_to_mask_clearance 0)
    (allow_soldermask_bridges_in_footprints no)
    (pcbplotparams
      (layerselection 0x00010fc_ffffffff)
      (plot_on_all_layers_selection 0x0000000_00000000)
    )
  )

  (net 0 "")
  (net 1 "GND")
  (net 2 "VCC_3V3")

  ;; Board outline
  (gr_rect
    (start 0 0)
    (end 50 30)
    (stroke (width 0.1) (type default))
    (fill none)
    (layer "Edge.Cuts")
    (uuid "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")
  )

  ;; Footprints, traces, vias, zones go here
)
```

### 4-layer stackup

For 4-layer boards, add inner layers:

```
(layers
  (0 "F.Cu" signal)
  (1 "In1.Cu" signal)       ;; Typically ground plane
  (2 "In2.Cu" signal)       ;; Typically power plane
  (31 "B.Cu" signal)
  ;; ... same user layers as above
)
```

### Footprint instance

```
(footprint "Resistor_SMD:R_0402_1005Metric"
  (layer "F.Cu")
  (uuid "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")
  (at 25 15 0)              ;; x, y, rotation
  (property "Reference" "R1"
    (at 0 -1.5 0)
    (layer "F.SilkS")
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (property "Value" "10k"
    (at 0 1.5 0)
    (layer "F.Fab")
    (effects (font (size 1 1) (thickness 0.15)))
  )
  ;; Pads
  (pad "1" smd roundrect
    (at -0.48 0)
    (size 0.56 0.62)
    (layers "F.Cu" "F.Paste" "F.Mask")
    (roundrect_rratio 0.25)
    (net 3 "NET_R1_1")
    (uuid "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")
  )
  (pad "2" smd roundrect
    (at 0.48 0)
    (size 0.56 0.62)
    (layers "F.Cu" "F.Paste" "F.Mask")
    (roundrect_rratio 0.25)
    (net 4 "NET_R1_2")
    (uuid "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")
  )
)
```

### Trace

```
(segment
  (start 25 15)
  (end 30 15)
  (width 0.25)
  (layer "F.Cu")
  (net 1)
  (uuid "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")
)
```

### Via

```
(via
  (at 30 15)
  (size 0.6)               ;; Annular ring outer diameter
  (drill 0.3)              ;; Drill diameter
  (layers "F.Cu" "B.Cu")
  (net 1)
  (uuid "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")
)
```

### Copper zone (ground pour)

```
(zone
  (net 1)
  (net_name "GND")
  (layer "B.Cu")
  (uuid "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")
  (hatch edge 0.5)
  (connect_pads
    (clearance 0.3)
  )
  (min_thickness 0.2)
  (fill yes
    (thermal_gap 0.5)
    (thermal_bridge_width 0.5)
  )
  (polygon
    (pts
      (xy 0 0)
      (xy 50 0)
      (xy 50 30)
      (xy 0 30)
    )
  )
)
```

### Mounting hole

```
(footprint "MountingHole:MountingHole_3.2mm_M3"
  (layer "F.Cu")
  (uuid "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")
  (at 3 3)
  (property "Reference" "H1"
    (at 0 -3.5 0)
    (layer "F.SilkS")
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (property "Value" "MountingHole"
    (at 0 3.5 0)
    (layer "F.Fab")
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (pad "" np_thru_hole circle
    (at 0 0)
    (size 3.2 3.2)
    (drill 3.2)
    (layers "*.Cu" "*.Mask")
    (uuid "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")
  )
)
```

## Project File

File extension: `.kicad_pro` — this is JSON, not S-expression.

```json
{
  "meta": {
    "filename": "project-name.kicad_pro",
    "version": 1
  },
  "board": {
    "design_settings": {
      "defaults": {
        "board_outline_line_width": 0.1,
        "copper_line_width": 0.2,
        "copper_text_size_h": 1.5,
        "copper_text_size_v": 1.5,
        "copper_text_thickness": 0.3
      },
      "rules": {
        "min_clearance": 0.15,
        "min_track_width": 0.15,
        "min_via_annular_width": 0.13,
        "min_via_diameter": 0.45
      }
    }
  },
  "libraries": {
    "pinned_footprint_libs": [],
    "pinned_symbol_libs": []
  },
  "schematic": {
    "drawing": {
      "default_line_thickness": 0.006,
      "default_text_size": 0.05
    }
  },
  "sheets": [
    ["", ""]
  ],
  "text_variables": {}
}
```

## Common Patterns

### Adding custom properties to components

Custom properties (MPN, supplier part number, etc.) are added as additional
`property` entries in both the symbol instance (schematic) and the footprint
(PCB). These survive round-tripping between schematic and PCB.

```
(property "MPN" "LM1117MPX-3.3/NOPB"
  (at 0 0 0)
  (effects (font (size 1.27 1.27)) hide)
)
(property "Supplier" "DigiKey"
  (at 0 0 0)
  (effects (font (size 1.27 1.27)) hide)
)
(property "Supplier_PN" "LM1117MPX-3.3/NOPBCT-ND"
  (at 0 0 0)
  (effects (font (size 1.27 1.27)) hide)
)
```

### Standard grid and spacing

- Symbol pins snap to 2.54mm (100mil) grid
- PCB components typically placed on 0.5mm or 0.25mm grid
- Traces on 0.05mm grid for fine-pitch, 0.25mm for general routing

### Net class definitions (in .kicad_pcb setup section)

```
(net_class "Default" ""
  (clearance 0.2)
  (trace_width 0.25)
  (via_dia 0.6)
  (via_drill 0.3)
  (uvia_dia 0.3)
  (uvia_drill 0.1)
)
(net_class "Power" "Power traces"
  (clearance 0.3)
  (trace_width 0.5)
  (via_dia 0.8)
  (via_drill 0.4)
  (uvia_dia 0.3)
  (uvia_drill 0.1)
)
```

### KiCad standard library names

When referencing KiCad's built-in libraries, use these naming conventions:

- Symbols: `Device:R`, `Device:C`, `Device:L`, `power:GND`, `power:+3V3`,
  `Connector_Generic:Conn_01x04`, `MCU_ST:STM32F103C8Tx`
- Footprints: `Resistor_SMD:R_0402_1005Metric`, `Capacitor_SMD:C_0402_1005Metric`,
  `Package_SO:SOIC-8_3.9x4.9mm_P1.27mm`, `Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical`

Always verify library names match the user's KiCad version. The names above
are for KiCad 8.x.
