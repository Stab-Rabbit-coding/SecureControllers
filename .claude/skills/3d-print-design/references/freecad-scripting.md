# FreeCAD Scripting Reference

Guide for generating FreeCAD models via Python scripts. These scripts are run
inside FreeCAD's Python console or as standalone scripts with FreeCAD's
libraries.

## Table of Contents

1. [Script Structure](#script-structure)
2. [Creating a Part Design Body](#creating-a-part-design-body)
3. [Sketches](#sketches)
4. [Operations (Pad, Pocket, Fillet, Chamfer)](#operations)
5. [Boolean Operations](#boolean-operations)
6. [Positioning and Transforms](#positioning-and-transforms)
7. [Exporting](#exporting)
8. [Parametric Design Pattern](#parametric-design-pattern)
9. [Common Enclosure Script Template](#enclosure-template)
10. [Running Scripts](#running-scripts)

---

## Script Structure

Every FreeCAD script follows this pattern:

```python
import FreeCAD
import Part
import Sketcher
from FreeCAD import Vector, Placement, Rotation

# Create a new document
doc = FreeCAD.newDocument("MyDesign")

# ... build geometry ...

# Recompute all features
doc.recompute()

# Save
doc.saveAs("/path/to/output.FCStd")

# Export to STL/STEP
Part.export([doc.getObject("Body")], "/path/to/output.step")
import Mesh
Mesh.export([doc.getObject("Body")], "/path/to/output.stl")
```

### Running the script

The user should:

1. Open FreeCAD
2. Go to Macro → Macros → navigate to the .py file → Execute
3. Or from the Python console: `exec(open("/path/to/script.py").read())`
4. Or from command line: `freecad -c script.py` (headless)

## Creating a Part Design Body

Part Design is FreeCAD's parametric modelling workbench — the equivalent of
SolidWorks' feature tree.

```python
import FreeCAD
import PartDesign
import Sketcher
from FreeCAD import Vector

doc = FreeCAD.newDocument("Enclosure")
body = doc.addObject("PartDesign::Body", "Body")
```

## Sketches

Sketches are 2D profiles that get extruded, pocketed, or revolved into 3D.

### Creating a sketch on a plane

```python
# Sketch on XY plane
sketch = body.newObject("Sketcher::SketchObject", "Sketch")
sketch.AttachmentSupport = [(doc.getObject("XY_Plane"), "")]
sketch.MapMode = "FlatFace"

# Or on the XZ plane
sketch.AttachmentSupport = [(doc.getObject("XZ_Plane"), "")]
```

### Drawing in a sketch

```python
# Rectangle (4 lines + constraints)
sketch.addGeometry(Part.LineSegment(Vector(0, 0, 0), Vector(50, 0, 0)))
sketch.addGeometry(Part.LineSegment(Vector(50, 0, 0), Vector(50, 30, 0)))
sketch.addGeometry(Part.LineSegment(Vector(50, 30, 0), Vector(0, 30, 0)))
sketch.addGeometry(Part.LineSegment(Vector(0, 30, 0), Vector(0, 0, 0)))

# Add coincident constraints to close the rectangle
sketch.addConstraint(Sketcher.Constraint("Coincident", 0, 2, 1, 1))
sketch.addConstraint(Sketcher.Constraint("Coincident", 1, 2, 2, 1))
sketch.addConstraint(Sketcher.Constraint("Coincident", 2, 2, 3, 1))
sketch.addConstraint(Sketcher.Constraint("Coincident", 3, 2, 0, 1))

# Dimension constraints
sketch.addConstraint(Sketcher.Constraint("DistanceX", 0, 1, 0, 2, 50.0))
sketch.addConstraint(Sketcher.Constraint("DistanceY", 1, 1, 1, 2, 30.0))

# Circle
sketch.addGeometry(Part.Circle(Vector(25, 15, 0), Vector(0, 0, 1), 5.0))

# Arc
sketch.addGeometry(Part.ArcOfCircle(
    Part.Circle(Vector(10, 10, 0), Vector(0, 0, 1), 5.0),
    0,           # Start angle (radians)
    3.14159      # End angle (radians)
))
```

### Rounded rectangle (common for enclosures)

```python
def add_rounded_rect(sketch, x, y, w, h, r):
    """Add a rounded rectangle to a sketch. x,y = bottom-left corner."""
    import math

    # Four arcs at corners
    # Bottom-left
    sketch.addGeometry(Part.ArcOfCircle(
        Part.Circle(Vector(x+r, y+r, 0), Vector(0,0,1), r),
        math.pi, 1.5*math.pi))
    # Bottom-right
    sketch.addGeometry(Part.ArcOfCircle(
        Part.Circle(Vector(x+w-r, y+r, 0), Vector(0,0,1), r),
        1.5*math.pi, 2*math.pi))
    # Top-right
    sketch.addGeometry(Part.ArcOfCircle(
        Part.Circle(Vector(x+w-r, y+h-r, 0), Vector(0,0,1), r),
        0, 0.5*math.pi))
    # Top-left
    sketch.addGeometry(Part.ArcOfCircle(
        Part.Circle(Vector(x+r, y+h-r, 0), Vector(0,0,1), r),
        0.5*math.pi, math.pi))

    # Four straight lines connecting the arcs
    sketch.addGeometry(Part.LineSegment(Vector(x+r, y, 0), Vector(x+w-r, y, 0)))       # bottom
    sketch.addGeometry(Part.LineSegment(Vector(x+w, y+r, 0), Vector(x+w, y+h-r, 0)))   # right
    sketch.addGeometry(Part.LineSegment(Vector(x+w-r, y+h, 0), Vector(x+r, y+h, 0)))   # top
    sketch.addGeometry(Part.LineSegment(Vector(x, y+h-r, 0), Vector(x, y+r, 0)))       # left

    # Add coincident constraints between arc endpoints and line endpoints
    # (omitted for brevity — connect each arc endpoint to its adjacent line)
```

## Operations

### Pad (extrude a sketch into 3D)

```python
pad = body.newObject("PartDesign::Pad", "Pad")
pad.Profile = sketch
pad.Length = 20.0          # Extrude height in mm
pad.Reversed = False       # Direction
pad.Midplane = False       # Extrude equally both sides
doc.recompute()
```

### Pocket (cut into solid using a sketch)

```python
# Create a sketch on the top face of the pad
pocket_sketch = body.newObject("Sketcher::SketchObject", "PocketSketch")
pocket_sketch.AttachmentSupport = [(pad, "Face6")]  # Top face
pocket_sketch.MapMode = "FlatFace"
# ... add geometry to pocket_sketch ...

pocket = body.newObject("PartDesign::Pocket", "Pocket")
pocket.Profile = pocket_sketch
pocket.Length = 18.0       # Depth of cut
doc.recompute()
```

### Fillet (round edges)

```python
fillet = body.newObject("PartDesign::Fillet", "Fillet")
fillet.Base = (pad, ["Edge1", "Edge2", "Edge3", "Edge4"])  # Select edges
fillet.Radius = 2.0
doc.recompute()
```

Finding edge names: use FreeCAD's GUI to select edges and note their names,
or iterate programmatically. Edge numbering depends on the feature's topology.

### Chamfer

```python
chamfer = body.newObject("PartDesign::Chamfer", "Chamfer")
chamfer.Base = (pad, ["Edge5", "Edge6"])
chamfer.Size = 1.0
doc.recompute()
```

## Boolean Operations

For combining or cutting Part objects (outside of Part Design workflow):

```python
import Part

box = Part.makeBox(50, 30, 20)
cylinder = Part.makeCylinder(5, 25, Vector(25, 15, -2))

# Subtraction (cut cylinder from box)
result = box.cut(cylinder)

# Union (merge)
result = box.fuse(cylinder)

# Intersection
result = box.common(cylinder)

# Add to document
feature = doc.addObject("Part::Feature", "Result")
feature.Shape = result
```

## Positioning and Transforms

```python
# Move an object
obj.Placement = Placement(
    Vector(10, 20, 0),                    # Translation
    Rotation(Vector(0, 0, 1), 45)         # Rotation: axis, angle in degrees
)

# Relative move
obj.Placement.Base = obj.Placement.Base + Vector(5, 0, 0)
```

## Exporting

### STL export

```python
import Mesh

# Export single object
mesh = doc.getObject("Body").Shape.tessellate(0.1)  # tolerance in mm
Mesh.export([doc.getObject("Body")], "/path/to/output.stl")
```

### STEP export (preferred for interchange)

```python
import Part
Part.export([doc.getObject("Body")], "/path/to/output.step")
```

### 3MF export

FreeCAD 1.0+ supports 3MF. Alternatively, export STL and convert.

```python
Mesh.export([doc.getObject("Body")], "/path/to/output.3mf")
```

## Parametric Design Pattern

Structure scripts with all user-adjustable parameters at the top:

```python
# ============================================================
# PARAMETERS — Edit these to customise the design
# ============================================================

# PCB dimensions (measure your board)
PCB_WIDTH = 65.0          # mm
PCB_DEPTH = 35.0          # mm
PCB_THICKNESS = 1.6       # mm
PCB_TOP_CLEARANCE = 12.0  # Tallest component on top
PCB_BOT_CLEARANCE = 1.0   # Solder joints / bottom components

# Mounting holes (positions relative to PCB bottom-left corner)
MOUNT_HOLES = [
    (3.0, 3.0),           # Bottom-left
    (62.0, 3.0),          # Bottom-right
    (3.0, 32.0),          # Top-left
    (62.0, 32.0),         # Top-right
]
MOUNT_HOLE_DIA = 3.2      # M3 clearance

# Enclosure parameters
WALL_THICKNESS = 2.0
FLOOR_THICKNESS = 1.6
CORNER_RADIUS = 3.0
SCREW_BOSS_OD = 7.0       # Outer diameter of screw boss
INSERT_HOLE_DIA = 4.0     # For M3 heat-set insert

# Connector cutouts (relative to PCB left edge, measured to centre)
CONNECTORS = [
    {"name": "USB-C", "side": "left", "x_from_edge": 0, "z_centre": 2.5,
     "width": 9.5, "height": 3.5},
]

# ============================================================
# DESIGN — Derived dimensions and geometry below
# ============================================================

SIDE_CLEARANCE = 0.8
INT_WIDTH = PCB_WIDTH + 2 * SIDE_CLEARANCE
INT_DEPTH = PCB_DEPTH + 2 * SIDE_CLEARANCE
INT_HEIGHT = PCB_BOT_CLEARANCE + PCB_THICKNESS + PCB_TOP_CLEARANCE + 1.0
# ... build the model using these parameters ...
```

This pattern lets the user change any parameter and re-run the script to get
an updated model without editing the geometry code.

## Enclosure Template

A complete minimal enclosure (bottom tray only) in Part shape operations:

```python
import FreeCAD
import Part
from FreeCAD import Vector

doc = FreeCAD.newDocument("Enclosure")

# Parameters
wall = 2.0
floor = 1.6
r = 3.0  # corner radius
int_w, int_d, int_h = 67, 37, 16  # internal dimensions

ext_w = int_w + 2*wall
ext_d = int_d + 2*wall
ext_h = int_h + floor

# Outer shell (rounded box)
outer = Part.makeBox(ext_w, ext_d, ext_h)
# Round vertical edges
outer = outer.makeFillet(r, [
    e for e in outer.Edges
    if abs(e.tangentAt(0).z) > 0.9  # vertical edges
])

# Inner cavity
inner = Part.makeBox(int_w, int_d, int_h)
inner.translate(Vector(wall, wall, floor))
inner = inner.makeFillet(max(r - wall, 0.5), [
    e for e in inner.Edges
    if abs(e.tangentAt(0).z) > 0.9
])

# Cut cavity from outer
tray = outer.cut(inner)

# Add screw bosses
standoff_h = 2.0  # PCB sits 2mm above floor
for mx, my in [(5, 5), (62, 5), (5, 32), (62, 32)]:
    boss = Part.makeCylinder(3.5, standoff_h + floor,
                              Vector(wall + 0.8 + mx, wall + 0.8 + my, 0))
    tray = tray.fuse(boss)
    # Drill insert hole
    hole = Part.makeCylinder(2.0, standoff_h + floor + 1,
                              Vector(wall + 0.8 + mx, wall + 0.8 + my, -0.5))
    tray = tray.cut(hole)

feature = doc.addObject("Part::Feature", "Tray")
feature.Shape = tray
doc.recompute()

# Export
Part.export([feature], "/tmp/enclosure_tray.step")
import Mesh
Mesh.export([feature], "/tmp/enclosure_tray.stl")
```

## Running Scripts

### Inside FreeCAD GUI

1. Open FreeCAD
2. Macro → Macros → navigate to the .py file → Execute
3. The model appears in the 3D viewport
4. Adjust parameters in the script, re-run

### Headless (command line)

```bash
freecad -c script.py
```

Or with FreeCADCmd (no GUI):

```bash
freecadcmd script.py
```

### As a Python module (if FreeCAD is on the Python path)

```python
import sys
sys.path.append("/usr/lib/freecad/lib")  # Adjust for your installation
import FreeCAD
# ... rest of script
```

The exact path depends on the FreeCAD installation. Common locations:

- Linux: `/usr/lib/freecad/lib` or `/usr/lib/freecad-python3/lib`
- macOS: `/Applications/FreeCAD.app/Contents/Resources/lib`
- Windows: `C:\Program Files\FreeCAD 1.0\bin`
