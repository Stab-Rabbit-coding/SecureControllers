---
name: svg-illustrator
description: >
  Hand-author stylised SVG illustrations - covers, figures, icons,
  diagrams - that read clearly at a glance and survive print-PDF
  rendering (WeasyPrint). Silhouette library (trees, ridges, water,
  skylines), atmospheric perspective, composition rules, engine
  support matrix, a11y and sanitisation baseline.
---

# SVG Illustrator

Applies when you are authoring SVG by hand: cover art, chapter
ornaments, inline figures, icons, diagrams, simple maps. Not for
data-driven charts (use d3 / matplotlib) or pixel art.

The user values hand-crafted illustration and is allergic to generic
vector clipart. Lead with your best silhouette choice and commit to it;
don't hedge with multiple variants unless they ask. Explain the
drawing principle behind a non-obvious choice - silhouette dominance,
atmospheric perspective, asymmetry bias, fractal stroke scaling - so
the user builds drawing intuition over time.

---

## The one rule

Before you commit a shape, imagine the silhouette on a bus-stop poster
at 30 metres. If you cannot name the thing, the shape is wrong. No
amount of gradient, texture, or accent colour rescues a silhouette that
fails the 30-metre test.

Every failure mode listed in §AI tells below traces back to this rule.

If a first silhouette attempt fails the 30-metre test, note which element failed and why before revising. If the correct path data for a complex organic shape is uncertain, describe the intended curve and offer a simplified fallback rather than committing an approximate shape.

---

## Hierarchy of concerns (higher wins on conflict)

1. **Readability.** Every shape names itself at a glance.
2. **Accessibility.** Decorative art is flagged decorative; informative
   art carries title + desc.
3. **Security.** No script, no foreignObject, no off-host xlink.
4. **Print fidelity.** The drawing renders the same in WeasyPrint as in
   the browser preview.
5. **File hygiene.** Minimal decimals, no orphan defs, no dev comments.
6. **Aesthetics.** Atmospheric, composed, disciplined palette.

Aesthetics last because a readable, accessible, clean SVG that looks
slightly plain is infinitely better than a beautiful drawing that
renders as a black rectangle in the print pipeline.

---

## Coordinate system

- **viewBox first.** `viewBox="0 0 W H"` defines the user-unit
  coordinate space. The width/height attributes can be omitted; CSS
  will scale the drawing.
- **Portrait cover convention:** `viewBox="0 0 800 1131"` matches
  print A-ish aspect (1.414). Landscape figures: `0 0 1131 800`. Icon
  grid: `0 0 24 24` or `0 0 32 32`.
- **preserveAspectRatio="xMidYMid slice"** fills a container by
  cropping; `meet` fits without cropping. `slice` is correct for
  full-bleed covers; `meet` for figures inside text.
- **Origin at top-left.** Y grows downward. "Horizon at one-third from
  top" → `y ≈ viewBox.height / 3`.

---

## Path data shorthand

| Command | Does | When to use |
|---|---|---|
| `M x y` / `m dx dy` | Move to | Start a subpath |
| `L x y` / `l dx dy` | Line to | Straight segment |
| `H x` / `h dx` | Horizontal line | Ridge baseline |
| `V y` / `v dy` | Vertical line | Tree trunks |
| `C x1 y1 x2 y2 x y` | Cubic bezier | Organic curves (fronds, ridges) |
| `S x2 y2 x y` | Smooth cubic | Reflected control point from previous `C` |
| `Q x1 y1 x y` | Quadratic bezier | Lighter organic curves (fewer controls) |
| `T x y` | Smooth quadratic | Chained organic segment |
| `A rx ry rot laf sf x y` | Arc | Circle fragments; rarely what you want |
| `Z` | Close path | Last step of every filled shape |

**Footguns:**

- Uppercase = absolute, lowercase = relative. Mixing them mid-path is
  valid but confusing; pick one style per subpath.
- Implicit line-to after an `M` - a subsequent pair of numbers continues
  as `L` / `l`. Reading `M 10 10 20 20` as three points is wrong; it
  moves to (10,10) then lines to (20,20).
- `Z` creates a straight segment from the current point to the
  subpath start. Self-intersecting paths obey `fill-rule` - `nonzero`
  (default) vs `evenodd` give different results.

---

## Composition

| Rule | Shorthand |
|---|---|
| Rule of thirds | Horizon on `y = H/3` or `y = 2H/3`, never `y = H/2` |
| Single focal point | One sun OR moon OR lone tree, never two |
| Leading lines | Ridge, river, treeline points eye toward focal point |
| Value hierarchy | Foreground = darkest, background = lightest |
| Frame anchor | Foreground element touches at least one frame edge |
| Palette discipline | 5-7 colours total, one warm accent, one cool neutral |

Reference: Turner (atmospheric perspective), Bierstadt (layered
landscape), Hokusai / Hiroshige (flat colour + silhouette), Loomis
(silhouette carries the pose).

---

## Atmospheric perspective

Three-plane model. Each layer receding into distance:

- **Contrast:** -25% to -30% per layer
- **Saturation:** -15% to -20% per layer
- **Hue shift:** toward cool neutral (blue-grey) and toward the sky
  gradient at that horizon height

SVG implementation: one `linearGradient` per layer, the `y=1` stop of
each far layer matches (or nearly matches) the `y=0` stop of the sky.

```xml
<linearGradient id="ridgeFar" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0%" stop-color="#3d5f7a" stop-opacity="0.85"/>
  <stop offset="100%" stop-color="#2c4760" stop-opacity="0.95"/>
</linearGradient>
<linearGradient id="ridgeMid" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0%" stop-color="#2d4a3a"/>
  <stop offset="100%" stop-color="#1e3a2e"/>
</linearGradient>
<linearGradient id="foreground" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0%" stop-color="#1e3a2e"/>
  <stop offset="100%" stop-color="#0e1a15"/>
</linearGradient>
```

---

## Silhouette library

### Conifers (pine, spruce, fir, hemlock, cedar)

Branching signature: **monopodial** (one central axis with lateral
tiers). Crown occupies the top 30-70% of total height depending on
species; trunk is always visible unless crowded.

*Never* a 3-point triangle. *Always* skirted irregular tiers.

```xml
<!-- Pine: crown high, trunk bare, flat-ish top -->
<g fill="#0e1a15">
  <!-- trunk -->
  <rect x="99.5" y="835" width="1" height="25"/>
  <!-- crown: asymmetric tiers drawn as paths -->
  <path d="M 100 835
           C 94 825, 82 822, 76 820
           C 86 816, 92 812, 100 810
           C 108 812, 114 816, 124 820
           C 118 822, 106 825, 100 835 Z"/>
  <path d="M 100 815
           C 95 806, 86 803, 80 800
           C 88 797, 94 794, 100 792
           C 106 794, 112 797, 120 800
           C 114 803, 105 806, 100 815 Z"/>
  <path d="M 100 797
           C 97 790, 92 788, 88 785
           C 94 782, 97 780, 100 778
           C 103 780, 106 782, 112 785
           C 108 788, 103 790, 100 797 Z"/>
  <!-- top tuft -->
  <path d="M 100 780 C 98 774, 98 770, 100 766 C 102 770, 102 774, 100 780 Z"/>
</g>
```

### Deciduous (oak, maple, elm, birch)

Branching signature: **sympodial** (zig-zag crown, each terminal
branch gives rise to two or more children). Canopy is a *cluster of
overlapping ellipses*, not a single lollipop.

```xml
<!-- Oak: wide spread, heavy lower limbs, leafed -->
<g fill="#1e3a2e" stroke="#0e1a15" stroke-width="0.6">
  <!-- trunk + primary branches (skeleton) -->
  <path d="M 400 860 L 400 820
           M 400 835 Q 385 825 372 820
           M 400 830 Q 415 820 428 818
           M 400 840 Q 395 830 388 822
           M 400 820 Q 402 810 406 808"
        fill="none" stroke-width="2.2"/>
  <!-- canopy mass: 5-8 overlapping ellipses, not concentric -->
  <ellipse cx="385" cy="818" rx="22" ry="14"/>
  <ellipse cx="402" cy="812" rx="26" ry="16"/>
  <ellipse cx="420" cy="819" rx="20" ry="13"/>
  <ellipse cx="395" cy="806" rx="18" ry="11"/>
  <ellipse cx="412" cy="801" rx="16" ry="10"/>
</g>
```

### Bare-winter silhouettes

Fractal stroke scaling: each fork level scales stroke-width by ~65%.

```xml
<!-- Bare oak: 4 branch levels, shrinking stroke -->
<g stroke="#0e1a15" fill="none" stroke-linecap="round">
  <!-- trunk: level 0, width 2.4 -->
  <path d="M 200 900 L 200 850" stroke-width="2.4"/>
  <!-- primary branches: width 1.6 -->
  <path d="M 200 866 Q 186 858 178 850
           M 200 860 Q 216 852 222 846
           M 200 855 Q 190 845 184 838"
        stroke-width="1.6"/>
  <!-- secondary: width 1.0 -->
  <path d="M 180 851 q -6 -6 -10 -10
           M 218 847 q 6 -5 10 -8
           M 188 842 q 5 -6 7 -12"
        stroke-width="1.0"/>
  <!-- tertiary twigs: width 0.6 -->
  <path d="M 172 842 q -4 -3 -6 -7
           M 226 842 q 4 -4 6 -8
           M 194 833 q 3 -4 4 -7"
        stroke-width="0.6"/>
</g>
```

### Palms (coconut, Washingtonia, Phoenix)

Each frond is a **unique bezier**. No two fronds share angle, length,
or curve. Trunk leans, often slightly.

```xml
<!-- Washingtonia (fan palm) -->
<g fill="#0e1a15">
  <!-- trunk, slight lean -->
  <path d="M 98 900 C 99 880, 101 860, 102 838 L 104 838 C 103 860, 101 880, 100 900 Z"/>
  <!-- fronds: 9 unique curves radiating from crown -->
  <g stroke="#0e1a15" stroke-width="1.8" fill="none" stroke-linecap="round">
    <path d="M 101 838 C 82 828, 68 820, 58 808"/>   <!-- lower left -->
    <path d="M 101 838 C 84 824, 72 812, 64 796"/>   <!-- mid left -->
    <path d="M 101 838 C 90 824, 84 808, 80 790"/>   <!-- upper left -->
    <path d="M 101 838 C 97 822, 96 806, 94 788"/>   <!-- near upper left -->
    <path d="M 101 838 C 103 820, 105 802, 106 784"/> <!-- top -->
    <path d="M 101 838 C 108 822, 114 806, 118 790"/> <!-- near upper right -->
    <path d="M 101 838 C 112 824, 122 812, 130 798"/> <!-- upper right -->
    <path d="M 101 838 C 116 828, 130 820, 142 812"/> <!-- mid right -->
    <path d="M 101 838 C 120 832, 138 830, 150 828"/> <!-- lower right -->
  </g>
</g>
```

### Ridges / mountains

Real ridges are **fractal**. Each major summit has subordinate
shoulders. No rhythmic zig-zag.

```xml
<!-- Asymmetric ridge with subordinate shoulders -->
<path d="M 0 640
         L 40 612 L 62 622      <!-- subordinate shoulder -->
         L 96 578 L 120 600     <!-- subordinate shoulder -->
         L 158 540              <!-- major summit, one steep flank -->
         L 182 578 L 198 568    <!-- gentler descent with pause -->
         L 232 592 L 258 572
         L 298 608 L 328 598
         L 368 556              <!-- second major summit -->
         L 398 610 L 432 600
         L 476 618 L 510 598
         L 548 624
         L 800 612 L 800 1131 L 0 1131 Z"
      fill="url(#ridgeFar)"/>
```

### Water

Lake: horizontal band, slightly darker than sky, with a thin bright
horizon line and scattered short reflection strokes.

Ocean: same plus low-amplitude swell (gentle `C` arcs, not sine) and
a vertical sun-reflection shimmer.

River: meandering path with **varying width** (narrower upstream,
wider downstream), never constant.

```xml
<!-- Lake with reflected sun shimmer -->
<rect x="0" y="900" width="800" height="120" fill="#2c4760"/>
<line x1="0" y1="900" x2="800" y2="900"
      stroke="#f4c98a" stroke-width="0.8" opacity="0.6"/>
<!-- sun reflection: vertical stack of short strokes, fading -->
<g stroke="#f4c98a" stroke-linecap="round" opacity="0.5">
  <line x1="496" y1="910" x2="504" y2="910" stroke-width="1.8"/>
  <line x1="494" y1="920" x2="506" y2="920" stroke-width="1.5"/>
  <line x1="492" y1="932" x2="508" y2="932" stroke-width="1.2"/>
  <line x1="490" y1="946" x2="510" y2="946" stroke-width="0.9"/>
  <line x1="488" y1="962" x2="512" y2="962" stroke-width="0.7"/>
</g>
```

### Grass, shrubs, chaparral

Irregular tufts of varying size. Single filled path with jagged upper
edge beats individual blades.

```xml
<!-- Grass tuft cluster -->
<path d="M 40 960
         l 4 -14 l 3 4 l 2 -10 l 3 6 l 5 -12 l 2 8 l 4 -6 l 3 5
         l 2 -11 l 3 7 l 4 -9 l 2 4 l 3 -14 l 2 12 l 3 -8 l 2 10 l 0 18 Z"
      fill="#0e1a15"/>
```

### Skylines

Vary width (8-16 units), height, and top shape across buildings.
Window lights as scattered dots, weighted toward tall buildings.

```xml
<g fill="#0e1a15">
  <rect x="390" y="780" width="10" height="50"/>        <!-- short flat -->
  <rect x="405" y="760" width="14" height="70"/>        <!-- medium flat -->
  <rect x="423" y="765" width="8"  height="65"/>        <!-- narrow -->
  <path d="M 435 740 L 435 830 L 455 830 L 455 750 L 445 740 Z"/>  <!-- stepped top -->
  <rect x="460" y="770" width="12" height="60"/>
  <path d="M 476 735 L 476 830 L 490 830 L 490 740 L 483 720 Z"/>  <!-- pyramid / antenna -->
  <rect x="494" y="755" width="10" height="75"/>
  <rect x="507" y="775" width="13" height="55"/>
</g>
<!-- window lights, weighted to tall buildings -->
<g fill="#f4c98a" opacity="0.7">
  <circle cx="442" cy="790" r="0.8"/>
  <circle cx="442" cy="805" r="0.8"/>
  <circle cx="483" cy="770" r="0.8"/>
  <circle cx="483" cy="786" r="0.8"/>
  <circle cx="483" cy="802" r="0.8"/>
</g>
```

### Desert subjects

**Saguaro:** 2-5 arms max, each at 40-80% of trunk height, never
symmetric. Ribs as thin vertical lines on the body. Trunk taper is
slight; arms are straight cylinders with a right-angle bend, not
curves.

**Joshua tree:** forked-dagger silhouette. Branches terminate in spiky
tufts rendered as short radiating strokes. No smooth curves on a
Joshua tree - every branch changes direction sharply.

**Mesa / butte:** flat horizontal cap, vertical cliff face with
subtle strata bands (horizontal lines at irregular intervals), sloped
talus skirt at base. Proportion: cap-to-height ratio 1:2 for mesa,
1:4 for butte.

**Cholla:** a scatter of small fuzzy-edged ovals on a thin branching
skeleton.

```xml
<!-- Saguaro silhouette -->
<g fill="#0e1a15">
  <path d="M 98 840 L 98 800 C 98 792 98 786 100 782 L 102 782
           C 104 786 104 792 104 800 L 104 840 Z"/>
  <!-- left arm, 62% height, right angle bend -->
  <path d="M 98 815 L 86 815 L 86 798 L 90 798 L 90 811 L 98 811 Z"/>
  <!-- right arm, 78% height, shorter -->
  <path d="M 104 808 L 114 808 L 114 795 L 110 795 L 110 804 L 104 804 Z"/>
  <!-- ribs -->
  <g stroke="#000" stroke-width="0.25" opacity="0.4">
    <line x1="99" y1="805" x2="99" y2="838"/>
    <line x1="101" y1="805" x2="101" y2="838"/>
    <line x1="103" y1="805" x2="103" y2="838"/>
  </g>
</g>
```

### Alpine subjects

**Snowfield:** white fill with a soft lower edge (irregular `L` curve)
following slope contour, not a straight horizontal.

**Glacier tongue:** trapezoidal wedge with subtle horizontal ribbing
(crevasse lines), tapered downhill.

**Talus slope:** triangular scatter of small grey polygons at the
base of a cliff - 30-60 shapes, no two identical.

**Krummholz (wind-flagged tree line):** conifer silhouettes leaning
uniformly downwind, skirted on the windward side, full-branched
leeward. Silhouettes shorter than tree line examples.

### Coastal subjects

**Sea stack:** a single vertical cylinder or fin shape offshore.
Waterline at the base, silhouette narrows toward the top by erosion.

**Sand dune:** long asymmetric curve - gentle windward slope, steep
slip face (angle of repose ~34°). Never symmetric.

**Beach grass (Ammophila):** tufted vertical blades bending
downwind, built as short line strokes radiating from a clump.

**Mangrove:** canopy over a tangle of prop roots; prop roots are
arched paths from canopy base to water, not vertical trunks.

**Lighthouse:** narrow tapered cylinder or octagonal shaft with a
crown, a lantern room, and a domed cap. Silhouette reads from
outline alone.

### Rural / agricultural subjects

**Barn:** pitched-roof rectangle, often with a gambrel (two-pitch)
roof. Cupola on the ridge for animation. Silo cylinder adjacent
with a domed cap.

**Grain elevator:** tall vertical cylinder or rectangle, flat or
gabled top, often in clusters of 3-5.

**Wind turbine / windmill:** tall tapered tower with a three-blade
rotor (modern) or four-blade radial fan with a small tail fin
(historic).

**Fence line:** irregular vertical marks along a ground contour,
spacing varies slightly, posts shorter near horizon via perspective.

**Farmhouse:** pitched-roof cube with a chimney and porch outline;
rarely more than that at silhouette scale.

### Architectural subjects

**Bridge:**

- Suspension: two towers, catenary cables (true catenary, not
  parabola - sag at 1/8 span), horizontal deck.
- Arch: single or multi-arch on piers, deck above or through.
- Truss: diagonal chord pattern on a horizontal deck.

**Water tower:** bowl-on-a-tripod silhouette (Southern US) or
cylindrical tank on legs.

**Industrial cooling tower:** hyperboloid curve - distinctive
hourglass profile, wider at base and top, narrow at waist.

**Church / chapel:** gabled rectangle + steeple (spire or tower with
small roof).

### Weather and atmosphere

**Rain:** diagonal parallel strokes at 15-25° from vertical, varying
opacity and length. Not dotted.

**Snow shower:** small ellipses (not circles), varying size, slight
diagonal drift. Background snow is smaller and fainter.

**Fog / mist:** low horizontal band blending into sky value, no hard
edges. Soft gradient mask if the engine supports it; otherwise a
translucent horizontal rectangle.

**Lightning:** jagged polyline with 3-5 direction changes, single
bright white/yellow stroke on a near-black sky. Brief secondary
branches at ~30° from the main bolt.

**Aurora borealis:** horizontal bands in desaturated green / magenta,
never sharp rays. Upper edge soft, lower edge fading to transparent.

**Cloud:** scalloped top edge, flat bottom (cumulus) or horizontal
band (stratus). Never perfectly oval.

### Celestial subjects

**Milky Way arc:** diffuse band crossing the sky, not a sharp line.
Broader and brighter at the galactic centre, fading toward the poles.

**Star field:** scattered small dots of varying size, with 3-5
brighter stars given cross-shaped glints.

**Moon phases:** gibbous / crescent as a circle with a second
displaced circle subtracting the dark portion.

### Geological features

**Canyon wall:** vertical strata bands at irregular heights. Hoodoo
columns: tapered pillar with a cap rock.

**Basalt columns:** hexagonal pattern at column tops, vertical
striations on faces.

**Sea cliff:** vertical face with horizontal strata, talus at base.

---

## Icon and diagram construction

Icons and simple diagrams use a different vocabulary from landscape
covers: fewer colours, thicker strokes, tighter grid.

### Icons

**Grid:** `viewBox="0 0 24 24"` or `0 0 32 32`. Keep everything on
integer or half-integer coordinates.

**Stroke width:** 1.5 or 2 user-units for 24x24 icons; 2 or 2.5 for
32x32. `stroke-linecap="round"` for organic feel,
`stroke-linejoin="round"` to avoid miter spikes at acute corners.

**Colour:** single `currentColor` fill or stroke; CSS controls the
colour on the consuming page.

```xml
<!-- Document icon, 24x24 stroke icon -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"
     fill="none" stroke="currentColor" stroke-width="1.5"
     stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
  <path d="M 6 2 h 8 l 4 4 v 14 a 2 2 0 0 1 -2 2 h -10
           a 2 2 0 0 1 -2 -2 v -16 a 2 2 0 0 1 2 -2 z"/>
  <path d="M 14 2 v 4 h 4"/>
  <line x1="9"  y1="13" x2="15" y2="13"/>
  <line x1="9"  y1="17" x2="15" y2="17"/>
</svg>
```

### Simple diagrams

Box-and-arrow diagrams with labels. Use `<text>` elements, meet
WCAG 1.4.3 contrast (4.5:1 text on background). Arrow heads are
small filled triangles at the arrow end.

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 120"
     role="img" aria-labelledby="d1t d1d" font-family="serif"
     font-size="14">
  <title id="d1t">Pipeline flow</title>
  <desc id="d1d">Three-stage pipeline: Input, Process, Output.</desc>
  <defs>
    <marker id="arr" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 0 L 10 5 L 0 10 Z" fill="#1a1a1a"/>
    </marker>
  </defs>
  <!-- boxes -->
  <g fill="#fafaf8" stroke="#1a1a1a" stroke-width="1.5">
    <rect x="20"  y="40" width="80" height="40" rx="4"/>
    <rect x="160" y="40" width="80" height="40" rx="4"/>
    <rect x="300" y="40" width="80" height="40" rx="4"/>
  </g>
  <!-- arrows -->
  <g stroke="#1a1a1a" stroke-width="1.5" marker-end="url(#arr)">
    <line x1="100" y1="60" x2="160" y2="60"/>
    <line x1="240" y1="60" x2="300" y2="60"/>
  </g>
  <!-- labels -->
  <g fill="#1a1a1a" text-anchor="middle">
    <text x="60"  y="65">Input</text>
    <text x="200" y="65">Process</text>
    <text x="340" y="65">Output</text>
  </g>
</svg>
```

---

## Render-engine support matrix (WeasyPrint 57-61, verified 2026-04)

| Feature | WeasyPrint | Fallback |
|---|---|---|
| `linearGradient`, `radialGradient` | **Yes** | - |
| `pattern` | Partial (viewBox ignored) | Inline tiled group |
| `clipPath` (url fragment) | Yes from 53+ | Stable; minor bugs still fixing |
| `mask` (alpha-only) | Yes | - |
| `mask` (luminance) | No | Use alpha mask or pre-compose |
| `filter` (blur, turbulence, displacement) | **No** (via CairoSVG) | Pre-render or accept unfiltered look |
| `feDropShadow` | No | Stacked duplicate path with offset + opacity |
| `symbol` + `use` | Flaky across docs | Inline the content directly |
| `use` with local fragment | Yes | - |
| `<image href="foo.png">` | Yes | - |
| Data-URI raster | Yes | Prefer file href for reviewability |
| Text on path | Partial | Prefer regular text + positioning |
| `vector-effect="non-scaling-stroke"` | No | Adjust stroke-width per intended display size |

**Rule of thumb:** if the drawing relies on filter primitives (blur,
turbulence, shadow), it will render flat in WeasyPrint. Design the
silhouette to work without the filter, then layer the filter for the
browser preview only.

Re-verify the matrix when you upgrade WeasyPrint; SVG support improves
steadily. CairoSVG drives the rasterisation; watch both changelogs.

---

## Print fidelity beyond WeasyPrint

**Colour space.** WeasyPrint outputs sRGB. For offset or digital
press, the prepress stage needs a CMYK conversion with an ICC profile
(ISO Coated v2 for European press, SWOP v2 for US sheet-fed / web).
Do not embed `icc-color()` paint values in SVG expecting WeasyPrint
to honour them - it will not. Design in sRGB; convert at the PDF stage
through Scribus, Affinity Publisher, or Illustrator.

**Hairline threshold.** At WeasyPrint's default 96 dpi, 1 user-unit
= 1 px ≈ 0.75 pt. Offset-press hairlines below 0.25 pt (≈0.33
user-units on an 800-wide viewBox scaled to A4) drop out. Digital and
inkjet threshold ~0.1 pt. Minimum `stroke-width` floor for any
detail that must survive the press:

| Output | Min stroke-width (on 800-unit viewBox) |
|---|---|
| Offset press | 0.4 |
| Digital / inkjet | 0.2 |
| Screen only | 0.1 |

**Alternative delivery targets.** Most email clients and many
e-readers strip inline SVG. Ship a raster fallback:

| Target | SVG support | Fallback |
|---|---|---|
| Email (Gmail, Outlook, Apple Mail) | Stripped | PNG at 2x display size, 600 px wide min |
| Epub3 | Yes | - |
| Epub2 | No | PNG |
| Kindle (older firmware) | No | PNG |
| Slide decks (PowerPoint, Keynote) | Import-only, no live filter | PNG or Illustrator-flattened PDF |

Inkscape export: `inkscape --export-type=png --export-dpi=144 file.svg`.

**Embedded fonts.** If the SVG contains `<text>`, either (a) restrict
to system-safe families (`serif`, `sans-serif`, `monospace`), or (b)
convert text to paths before shipping (`Object > Object to Path` in
Inkscape; `Type > Create Outlines` in Illustrator). Embedding
`@font-face` inside SVG requires the font licence to permit
embedding and redistribution; many Google Fonts and most commercial
fonts do not. Convert-to-path is the safe default for print-bound
SVG.

---

## Accessibility

Two cases:

**Decorative only (cover art, chapter ornament, background).**

```xml
<svg role="presentation" aria-hidden="true" ...>
```

or the outer `<figure>` can set `aria-hidden="true"`.

**Informational (diagram, data visualisation, map).**

```xml
<svg role="img" aria-labelledby="t1 d1" ...>
  <title id="t1">ZIP 92882 aerial with boundary</title>
  <desc id="d1">
    Satellite view of Corona, California showing the 92882 postal
    boundary outlined in copper. The Santa Ana river corridor runs
    diagonally. Major highways: 91 Freeway along the southern edge,
    I-15 at the eastern edge.
  </desc>
  <!-- drawing -->
</svg>
```

Rules:

- `<title>` is announced by screen readers; browsers display it as a
  tooltip. Keep it to a short phrase (≤10 words).
- `<desc>` carries the long description. If the meaning is conveyed in
  surrounding text, `<desc>` can be omitted or brief.
- `focusable="false"` on all decorative inline SVGs. Chrome 95+ and
  Firefox will place SVGs in the tab order without it, creating
  keyboard-navigation noise. Not an IE-only concern.
- Contrast - graphical objects: 3:1 against their background (WCAG
  1.4.11 Non-text Contrast).
- Contrast - text inside SVG (`<text>` elements in diagrams, maps,
  labels): 4.5:1 for normal text, 3:1 for large (≥18 pt or ≥14 pt
  bold) - WCAG 1.4.3 Contrast (Minimum).

---

## Security sanitisation

When the SVG comes from a template, an LLM, or the wild, strip:

- **Elements:** `<script>`, `<foreignObject>`, `<iframe>`,
  `<animate*>` with `to` pointing at a script, `<handler>`, `<set>`
  with an event attribute.
- **XML preamble:** `<!DOCTYPE>` declarations, `<!ENTITY>`
  declarations, `<?xml-stylesheet?>` processing instructions.
  XXE via external-entity expansion (lxml / CairoSVG) can read server
  files; strip the preamble even if it looks inert.
- **CSS exfiltration:** `<style>` blocks containing `@import url(...)`
  or attribute-selector reads that beacon to a remote host. No script
  needed - CVE-2026-2441 used pure CSS to exfiltrate from Chrome.
- **Attributes:** any `on*` (`onclick`, `onload`, `onmouseover`, ...),
  `xlink:href` or `href` pointing off-host or at `data:` /
  `javascript:` URIs, `style` containing `url(data:...)`,
  `@import`, or `expression(...)`.
- **External references:** `<use href="https://...">` - must be local
  fragments only.

Grep cheat (two passes, second catches XXE + CSS exfil):

```bash
grep -nE '<script|<foreignObject|<iframe|on[a-z]+=|xlink:href="(https?|data|javascript):' file.svg
grep -nE '<!DOCTYPE|<!ENTITY|<\?xml-stylesheet|@import\s+url|expression\s*\(' file.svg
```

If any match returns, the SVG needs review before embedding.

For programmatic sanitisation (user-submitted SVG), use DOMPurify
with its SVG profile enabled. Track its CVE feed: CVE-2024-47875
(fixed in 3.1.3), CVE-2025-26791 (fixed in 3.2.4) both involved
SVG bypasses; assume more will follow.

---

## File hygiene

- Decimal precision: 2 fractional digits is always enough for cover
  art; 1 for icons.
- Strip default attributes: `fill="none"` on a `<g>` that all children
  override, empty `style=""`.
- `<defs>` carries only referenced declarations. Unreferenced defs are
  dead weight.
- Group with `<g>` when styling applies to multiple shapes; avoid
  single-child groups.
- SVGO is safe with most defaults, but **disable** `cleanupIds` if the
  SVG is referenced externally by id, and **disable** `removeViewBox`
  always.
- Hand-authored cover SVG target: under 8 KB. Generated-in-Illustrator
  output often runs 40-100 KB; hand-author when size matters.

---

## AI tells: the blacklist

- **Trees as 3-point polygons.** Universal LLM fallback. Ban outright.
- **Trees as lollipop circles on a stick.** Kindergarten motif.
- **Bare trees as line-plus-two-slashes.** Reads as a crucifix.
- **Symmetric palm fronds.** Real palms lean and fan unevenly.
- **Rhythmic zig-zag ridges.** Real ridges have irregular summit
  spacing and asymmetric flanks.
- **Sine-wave water.** Reads as corrugated metal.
- **Identical-width skyline rectangles.** Reads as bar code.
- **Concentric-ellipse canopies.** Reads as onion.
- **Radial gradient "sun" alone in a flat sky.** Add at least one
  secondary value - ember specks, cloud band, silhouetted foreground
  frame.
- **Rainbow multi-stop gradients.** Real skies have 2-4 stops in a
  narrow colour range; 5+ stops in disparate hues read as synthetic.
- **Decorative blob shapes.** Pure 2021 SaaS; no place in serious
  cover art.
- **Mirror-symmetric composition.** A perfectly symmetric landscape is
  a logo, not an illustration.
- **Saguaros with curly arms.** Real saguaro arms bend at a right
  angle. Curly-armed cactus is a cartoon.
- **Cloud as a cotton-ball ellipse.** Real clouds have flat bottoms
  (cumulus) or horizontal extent (stratus); pure ovals read as
  emoji.
- **Lightning as a smooth zigzag.** Real bolts have 3-5 irregular
  direction changes and short secondary branches.
- **Snowflakes as six-pointed stars.** At silhouette scale, snow is
  a scatter of small ellipses. Only draw the hexagonal form when the
  flake is the subject.
- **Symmetric suspension-bridge catenary.** Real cables hang with
  maximum sag at 1/8 span, not at the centre.

When you catch yourself reaching for any of these, stop. Pick from the
silhouette library instead.

---

## Review mode

When reviewing an existing SVG, first note what is working well (strong silhouette choices, effective atmospheric perspective, clean file structure). Then report findings in this order:

1. **Readability violations** - silhouettes that fail the 30-metre
   test, misidentifiable species.
2. **Security** - script, foreignObject, on-handlers, external refs.
3. **Accessibility** - missing role, title, desc; decorative SVG
   announced to screen readers.
4. **Engine compatibility** - features that won't render in the target
   engine.
5. **AI tells** - patterns from the blacklist.
6. **File hygiene** - decimal bloat, orphan defs, dev comments.

Report each issue in situation-behaviour-impact format: where it appears, what the pattern is, why it fails the hierarchy. If a fix is uncertain (e.g. ambiguous engine support), offer the most conservative option and flag it for testing.

### Finding format

```
### [SEVERITY] Short title
**File:** path/to/file.svg, lines X-Y
**Pattern:** what's there
**Why it fails:** which rule from the skill it violates
**Fix:** specific replacement, with SVG snippet if non-trivial
```

Severity: CRITICAL (drawing is illegible or unsafe), HIGH (species
misidentification, a11y failure, engine incompat), MEDIUM (AI tell),
LOW (hygiene).

Return the findings table and punch list directly in the assistant
message. Do not write a separate review file unless the user asks.

---

## Checklist: run through this before shipping any SVG

- [ ] Every silhouette passes the 30-metre test.
- [ ] No 3-point-polygon conifers.
- [ ] No line-plus-slashes bare trees.
- [ ] No symmetric palm fronds.
- [ ] No rhythmic-zig-zag ridges.
- [ ] No sine-wave water.
- [ ] No identical-width skyline rectangles.
- [ ] Atmospheric perspective applied - three-plane model minimum.
- [ ] Single dominant focal point.
- [ ] Horizon not at dead centre.
- [ ] Palette is 5-7 colours, CSS variables preferred if the host
      provides them.
- [ ] No `<script>`, `<foreignObject>`, no `on*` handlers.
- [ ] No off-host `xlink:href` / `href` / `data:` / `javascript:`.
- [ ] No `<!DOCTYPE>`, `<!ENTITY>`, `<?xml-stylesheet?>`, or
      `@import` inside `<style>`.
- [ ] `role="img"` + `<title>` + `<desc>` for informational art;
      `aria-hidden="true"` + `focusable="false"` for decorative.
- [ ] Informational graphical objects meet 3:1 contrast (WCAG
      1.4.11); `<text>` inside SVG meets 4.5:1 normal / 3:1 large
      (WCAG 1.4.3).
- [ ] Filter primitives either render in the target engine or have a
      fallback that works without them.
- [ ] Stroke-width floor met for target medium (0.4 / 0.2 / 0.1
      user-units on 800-unit viewBox for offset / digital / screen).
- [ ] Text converted to paths OR restricted to system-safe families
      for print-bound SVG.
- [ ] Raster fallback produced for email / epub2 / Kindle delivery
      if applicable.
- [ ] `<defs>` has no orphans.
- [ ] Decimal precision ≤ 2.
- [ ] No dev comments, no TODOs, no trailing whitespace.
- [ ] Containing PDF / page rebuilt; the SVG renders correctly in the
      actual target engine.

---

## Further reading

- MDN SVG tutorial, https://developer.mozilla.org/en-US/docs/Web/SVG
- Sara Soueidan's SVG articles, https://www.sarasoueidan.com/
- Josh W. Comeau's interactive guide to paths
- W3C SVG 2 specification
- Andrew Loomis, *Creative Illustration* (silhouette + tone pattern)
- David Sibley, sibleyguides.com (species ID by gestalt silhouette)
- John Muir Laws, johnmuirlaws.com (conifer branching method)
- Turner / Bierstadt / Hokusai / Hiroshige (historical references for
  atmospheric landscape composition)
- OWASP SVG sanitisation guidance
- DOMPurify SVG profile (for programmatic sanitisation)
- WeasyPrint SVG support notes in the project docs
