# OpenSCAD Reference

Language reference and patterns for generating OpenSCAD (.scad) files.

## Table of Contents

1. [File Structure](#file-structure)
2. [Primitives](#primitives)
3. [Transformations](#transformations)
4. [Boolean Operations](#boolean-operations)
5. [Modules (Functions)](#modules)
6. [Control Flow](#control-flow)
7. [Useful Patterns](#useful-patterns)
8. [Enclosure Template](#enclosure-template)
9. [Export](#export)

---

## File Structure

OpenSCAD files are declarative: you describe geometry, not steps. Parameters
go at the top for easy customisation.

```scad
// ============================================================
// PARAMETERS
// ============================================================
pcb_width  = 65;
pcb_depth  = 35;
wall       = 2.0;
corner_r   = 3.0;

// ============================================================
// DERIVED VALUES
// ============================================================
int_width  = pcb_width + 2 * 0.8;  // 0.8mm side clearance

// ============================================================
// GEOMETRY
// ============================================================
difference() {
    outer_shell();
    inner_cavity();
}

// ============================================================
// MODULES
// ============================================================
module outer_shell() { ... }
module inner_cavity() { ... }
```

### Special variables

```scad
$fn = 60;      // Circle resolution (number of segments). 60 is good for
               // final render; use 30 for preview speed.
$fa = 2;       // Minimum angle per segment
$fs = 0.4;     // Minimum segment size (mm). Good default for 3D printing.
```

Set `$fn` globally for consistent resolution, or per-object: `cylinder(r=5, h=10, $fn=60);`

## Primitives

### Cube (box)

```scad
cube([width, depth, height]);               // Corner at origin
cube([width, depth, height], center=true);  // Centred on origin
```

### Cylinder

```scad
cylinder(h=height, r=radius);                    // Flat-bottom at origin
cylinder(h=height, r1=bottom_r, r2=top_r);       // Cone/frustum
cylinder(h=height, d=diameter, center=true);      // By diameter
```

### Sphere

```scad
sphere(r=radius);
sphere(d=diameter);
```

### Polyhedron (arbitrary mesh)

```scad
polyhedron(
    points = [[0,0,0], [10,0,0], [10,10,0], [0,10,0],
              [0,0,10], [10,0,10], [10,10,10], [0,10,10]],
    faces  = [[0,1,2,3], [4,5,1,0], [5,6,2,1],
              [6,7,3,2], [7,4,0,3], [7,6,5,4]]
);
```

### Text (for embossing/debossing)

```scad
linear_extrude(height=0.6)
    text("HELLO", size=8, font="Liberation Sans:style=Bold",
         halign="center", valign="center");
```

### 2D shapes for extrusion

```scad
// Rectangle
square([width, height], center=true);

// Circle
circle(r=radius);
circle(d=diameter);

// Polygon
polygon(points=[[0,0], [10,0], [10,10], [0,10]]);
```

## Transformations

```scad
translate([x, y, z]) object();
rotate([x_deg, y_deg, z_deg]) object();
scale([sx, sy, sz]) object();
mirror([1, 0, 0]) object();   // Mirror across YZ plane

// Extrude 2D to 3D
linear_extrude(height=h) 2d_shape();
linear_extrude(height=h, twist=90, slices=50) 2d_shape();
rotate_extrude(angle=360) 2d_profile();

// Offset (grow/shrink 2D shapes — useful for walls)
offset(r=2) square([10, 10]);           // Rounded expansion by 2mm
offset(delta=2) square([10, 10]);       // Sharp-corner expansion
offset(r=-wall) square([ext_w, ext_d]); // Shrink for inner cavity
```

## Boolean Operations

```scad
// Subtraction (cut B from A)
difference() {
    A();   // Keep this
    B();   // Cut this away
    C();   // Also cut this
}

// Union (merge)
union() {
    A();
    B();
}

// Intersection (keep only overlap)
intersection() {
    A();
    B();
}
```

## Modules

Modules are reusable geometry functions:

```scad
module standoff(height, outer_d, hole_d) {
    difference() {
        cylinder(h=height, d=outer_d);
        translate([0, 0, -0.1])
            cylinder(h=height + 0.2, d=hole_d);
    }
}

// Use it
translate([5, 5, 0]) standoff(4, 7, 4);
translate([60, 5, 0]) standoff(4, 7, 4);
```

### Parametric modules with defaults

```scad
module rounded_box(size, radius=3, center=false) {
    // size = [x, y, z]
    offset_pos = center ? -size/2 : [0, 0, 0];
    translate(offset_pos)
    hull() {
        for (x = [radius, size[0]-radius])
        for (y = [radius, size[1]-radius])
            translate([x, y, 0])
                cylinder(h=size[2], r=radius);
    }
}
```

## Control Flow

### For loops

```scad
// Place 4 standoffs at specified positions
mount_positions = [[5,5], [60,5], [5,30], [60,30]];

for (pos = mount_positions) {
    translate([pos[0], pos[1], 0])
        standoff(4, 7, 4);
}
```

### Conditional geometry

```scad
if (include_ventilation) {
    vent_slots();
}
```

### List comprehension

```scad
// Generate a list of positions
positions = [for (i = [0:5:50]) [i, 0, 0]];
```

## Useful Patterns

### Rounded rectangle (2D, for extrusion)

```scad
module rounded_rect(size, r) {
    offset(r=r) offset(r=-r) square(size, center=true);
}

// Usage: extrude into a box with rounded vertical edges
linear_extrude(height=20) rounded_rect([50, 30], 3);
```

### Shell (hollow box)

```scad
module shell(outer_size, wall, floor=0) {
    floor_t = floor > 0 ? floor : wall;
    difference() {
        cube(outer_size);
        translate([wall, wall, floor_t])
            cube([outer_size[0]-2*wall,
                  outer_size[1]-2*wall,
                  outer_size[2]]);  // Open top
    }
}
```

### Ventilation slot grid

```scad
module vent_slots(area_w, area_h, slot_w=1.2, slot_h=8, spacing=2.5) {
    cols = floor(area_w / (slot_w + spacing));
    rows = floor(area_h / (slot_h + spacing));
    start_x = (area_w - cols * (slot_w + spacing) + spacing) / 2;
    start_y = (area_h - rows * (slot_h + spacing) + spacing) / 2;

    for (c = [0:cols-1])
    for (r = [0:rows-1])
        translate([start_x + c*(slot_w+spacing), start_y + r*(slot_h+spacing), 0])
            cube([slot_w, slot_h, 50]);  // Through-cut
}
```

### Honeycomb pattern (2D)

```scad
module honeycomb(area_w, area_h, cell_size=5, wall=1.2) {
    pitch_x = cell_size + wall;
    pitch_y = (cell_size + wall) * sin(60);
    cols = ceil(area_w / pitch_x) + 1;
    rows = ceil(area_h / pitch_y) + 1;

    intersection() {
        square([area_w, area_h]);
        for (c = [0:cols])
        for (r = [0:rows]) {
            x = c * pitch_x + (r % 2) * pitch_x / 2;
            y = r * pitch_y;
            translate([x, y])
                circle(d=cell_size, $fn=6);
        }
    }
}
```

### Connector cutout helper

```scad
module connector_cutout(width, height, depth=10, chamfer=0.5) {
    // Centred cutout with entry chamfer
    union() {
        cube([width, depth, height], center=true);
        // Chamfer on the outside edge
        translate([0, depth/2, 0])
            cube([width+2*chamfer, chamfer*2, height+2*chamfer], center=true);
    }
}
```

### Screw boss with optional heat-set insert hole

```scad
module screw_boss(height, outer_d=7, hole_d=4, base_fillet=1.5) {
    union() {
        // Main boss
        difference() {
            cylinder(h=height, d=outer_d);
            translate([0, 0, -0.1])
                cylinder(h=height+0.2, d=hole_d);
        }
        // Base fillet (approximated as a cone)
        cylinder(h=base_fillet, d1=outer_d+2*base_fillet, d2=outer_d);
    }
}
```

## Enclosure Template

Complete parametric enclosure with standoffs and connector cutout:

```scad
// ============================================================
// PARAMETERS
// ============================================================

// PCB dimensions
pcb_x       = 65;
pcb_y       = 35;
pcb_z       = 1.6;
top_clear   = 12;
bot_clear   = 2;

// Enclosure
wall        = 2.0;
floor_t     = 1.6;
corner_r    = 3.0;
side_clear  = 0.8;

// Mounting
mount_holes = [[3, 3], [62, 3], [3, 32], [62, 32]];
standoff_od = 7;
insert_hole = 4.0;  // M3 heat-set insert

// Connectors (position from PCB origin, which is bottom-left)
usb_c_pos   = [0, 17.5];  // Centre of USB-C on left edge
usb_c_w     = 9.5;
usb_c_h     = 3.5;

// Resolution
$fn = 60;

// ============================================================
// DERIVED
// ============================================================

int_x = pcb_x + 2*side_clear;
int_y = pcb_y + 2*side_clear;
int_z = bot_clear + pcb_z + top_clear + 1;
ext_x = int_x + 2*wall;
ext_y = int_y + 2*wall;
ext_z = int_z + floor_t;

// PCB origin inside enclosure
pcb_ox = wall + side_clear;
pcb_oy = wall + side_clear;
pcb_oz = floor_t + bot_clear;

// ============================================================
// MAIN
// ============================================================

difference() {
    union() {
        tray_shell();
        standoffs();
    }
    insert_holes();
    usb_cutout();
}

// ============================================================
// MODULES
// ============================================================

module tray_shell() {
    difference() {
        // Outer
        rounded_box([ext_x, ext_y, ext_z], corner_r);
        // Inner cavity (open top)
        translate([wall, wall, floor_t])
            rounded_box([int_x, int_y, int_z + 1], max(corner_r-wall, 0.5));
    }
}

module rounded_box(size, r) {
    hull() {
        for (x = [r, size[0]-r])
        for (y = [r, size[1]-r])
            translate([x, y, 0])
                cylinder(h=size[2], r=r);
    }
}

module standoffs() {
    for (pos = mount_holes) {
        translate([pcb_ox + pos[0], pcb_oy + pos[1], 0])
            cylinder(h=floor_t + bot_clear, d=standoff_od);
    }
}

module insert_holes() {
    for (pos = mount_holes) {
        translate([pcb_ox + pos[0], pcb_oy + pos[1], -0.1])
            cylinder(h=floor_t + bot_clear + 0.2, d=insert_hole);
    }
}

module usb_cutout() {
    // USB-C cutout on left wall
    cx = -0.1;
    cy = pcb_oy + usb_c_pos[1];
    cz = pcb_oz + pcb_z/2 + usb_c_h/2;  // Centre of connector above PCB
    translate([cx, cy - usb_c_w/2 - 0.3, cz - usb_c_h/2 - 0.3])
        cube([wall + 0.2, usb_c_w + 0.6, usb_c_h + 0.6]);
}
```

Save as `enclosure.scad`. Open in OpenSCAD and press F5 to preview, F6 to
render, then File → Export → STL.

## Export

### From OpenSCAD GUI

- F5: Preview (fast, approximate)
- F6: Render (slow, exact, required before export)
- File → Export as STL / 3MF / OFF / AMF / CSG

### From command line

```bash
# Render and export to STL
openscad -o output.stl input.scad

# With custom parameters
openscad -o output.stl -D 'pcb_x=80' -D 'wall=2.5' input.scad

# Export as 3MF
openscad -o output.3mf input.scad
```

The `-D` flag overrides parameters, making it easy to generate variants
without editing the file.

### From a script (batch generation)

```bash
#!/bin/bash
for wall in 1.6 2.0 2.4; do
    openscad -o "enclosure_wall${wall}.stl" \
             -D "wall=${wall}" \
             enclosure.scad
done
```
