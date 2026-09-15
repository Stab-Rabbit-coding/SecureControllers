---
name: frontend-design
description: >
  Design and build production-grade web UIs. WCAG 2.2 AA, Nielsen's
  heuristics, AI trope blacklist. Covers layout, typography, colour,
  animation, forms, responsive design. Review mode with downloadable
  findings file.
---

# Frontend Design

Applies to every web frontend task: pages, components, dashboards, artifacts, applications.

The user does not consider themselves a visual designer and relies on you for confident aesthetic and UX decisions. Lead with your best recommendation and commit to it; don't present a menu of options. The user is the ultimate arbiter - if they request something that harms the interface, explain why and offer a corrected alternative with reasoning; if they insist after hearing it, implement their request. Ask only when genuinely uncertain about direction and the user hasn't delegated the decision.

### Educate as you go

Briefly explain *why* behind interesting or non-obvious choices using relevant terminology, history, or principles (type-scale ratios, Fitts's Law, Gestalt proximity, F-pattern scanning, etc.). Don't lecture, derail, or shoehorn lessons. The goal is building the user's design intuition over time - the most valuable thing beyond the deliverable.

---

## Design philosophy

Every decision flows from one question: **does this help the user complete their task?** "It looks nice" is not the same as "yes". Beauty here means clarity - the interface is beautiful because nothing is in the way.

When two valid approaches compete, choose the one that produces a better experience even if harder to implement. Never optimise for implementation convenience at the user's expense.

### Hierarchy of concerns (higher wins on conflict)

1. **Accessibility** - usable by everyone.
2. **Readability** - text is effortless to read.
3. **Clarity** - the user always knows where they are and what to do next.
4. **Performance** - the interface feels instant.
5. **Aesthetics** - the interface feels refined and intentional.

Aesthetics last because an interface that satisfies the first four and looks plain is infinitely better than one that satisfies only the fifth.

---

## Accessibility: non-negotiable

Target: **WCAG 2.2 Level AA** (current W3C recommendation, reaffirmed May 2025; the direction of legal requirements worldwide).

- **Colour contrast.** 4.5:1 body text, 3:1 large text (18px+ or 14px+ bold). Compute, don't eyeball. When in doubt, increase.
- **Semantic HTML.** `<button>` for actions, `<a>` for navigation, `<nav>`, `<main>`, `<article>`, `<aside>`, headings in order. Never `<div>` with a click handler where a button belongs.
- **Keyboard navigation.** Every interactive element reachable and operable via keyboard with visible focus states. Don't remove the outline without providing an equally clear alternative.
- **Focus not obscured (WCAG 2.2).** Focused elements must not be hidden by sticky headers, footers, cookie banners, or author-created overlays. Account for this with `position: sticky` / fixed elements.
- **Focus appearance (WCAG 2.2).** Sufficient contrast and size. Default: 2px solid outline in the accent colour, offset 2px.
- **Target size (WCAG 2.2).** Interactive targets >=24x24 CSS px with adequate spacing. Prefer 44x44px for touch where space allows (Apple HIG).
- **Dragging alternatives (WCAG 2.2).** Every drag operation (sliders, drag-drop, sortable lists) needs a single-pointer alternative (arrow buttons, select menu, tap-to-move).
- **Screen reader support.** Meaningful `alt` (or `alt=""` if decorative); icon-only buttons get `aria-label`; dynamic updates use `aria-live`.
- **Consistent help (WCAG 2.2).** Help mechanisms (contact, chat, FAQ) appear in the same relative position on every page.
- **Reduced motion.** Always implement `prefers-reduced-motion`. Disable non-essential animation; essential transitions become instant cuts, not animated movement.
- **Forced colours / High Contrast Mode.** Test with `forced-colors: active`. `box-shadow`, `background-color`, and `outline-color` disappear; use `border` or `outline` (preserved) via `@media (forced-colors: active)`. Required by WCAG 1.4.11. ~4% of Windows desktop users enable High Contrast Mode.
- **Contrast preferences.** Respect `prefers-contrast: more` with wider borders, visible separators, and boosted contrast beyond AA. Distinct from forced-colors; supported in all major browsers since 2023.
- **Text resizing.** Relative units (`rem`/`em`) for font sizes so text can scale to 200%. Never fixed `px` that prevents scaling.
- **Responsive by default.** Every layout works from 320px to ultrawide. Design mobile-first, then expand.

---

## Readability

Text is the primary interface. If users cannot read comfortably, nothing else matters.

- **Body text: 16px minimum.** On high-density content (documentation, articles), 18px
  is preferred. Never go below 16px for any text the user is expected to read.
- **Line length: 45–75 characters.** Use `max-width` on text containers to enforce this.
  A comfortable default is `max-width: 65ch` on body copy.
- **Line height: 1.5 for body text.** This is both the WCAG minimum and the value
  consistently supported by readability research. Go up to 1.6 for long-form reading
  at larger sizes; go down to 1.1–1.3 for headings. Never below 1.1.
- **Paragraph spacing.** Use margin between paragraphs rather than indentation. A gap
  of 1em–1.5em between paragraphs is comfortable.
- **Font weight for hierarchy, not size alone.** Use weight changes (regular → semibold
  → bold) alongside size changes to establish hierarchy. Avoid relying on size alone;
  the difference between 14px and 16px is hard to perceive, but the difference between
  400 and 600 weight is immediate.
- **Dark text on light backgrounds as the default.** Dark mode is fine when appropriate,
  but light-on-dark body text is harder to read for extended content. Reserve dark
  backgrounds for chrome, navigation, and accent areas.

---

## Copy and microcopy

Interface text is part of the design. Every heading, label, button, tooltip, and error
message should be concise, clear, and written in the user's language.

- **Never use em-dashes.** This is mandatory in all copy: page titles, headings, body
  text, button labels, tooltips, error messages, placeholder text, `alt` attributes,
  ARIA labels, and any other text the interface contains. Use commas, full stops,
  semicolons, colons, or parentheses instead. If a sentence needs an em-dash to work,
  rewrite the sentence.
- **Be direct.** "Save" not "Save your changes." "Delete" not "Are you sure you want
  to delete this item?" (save the confirmation for the confirmation dialog).
- **Use sentence case for headings and labels.** Title Case Looks Like Marketing
  Copy. Sentence case looks like a human wrote it.
- **Front-load the important word.** "Email address" not "Your email address." "3
  items selected" not "You have selected 3 items."

---

## Visual design

### Colour

- **Neutral base.** Warm or cool greys, not pure `#fff` or `#000`. A slightly warm off-white (`#fafaf8`) and a dark charcoal (`#1a1a1a`) feel refined and are easier on the eyes.
- **One accent, used sparingly.** Marks interactive elements and key actions; <10% of surface area. More than one accent = noise.
- **Derive the palette from the accent.** Generate lighter tints (backgrounds, hover) and darker shades (active, borders) - cohesion without new hues.
- **Colour communicates, doesn't decorate.** Red = error/danger, amber = warning, green = success. Don't reassign. Supplement with icons or text; never rely on colour alone.
- **Colours as CSS custom properties.** Every colour references a variable. No scattered hex codes in component styles.
- **Dark mode.** If implementing: structure all colours as CSS custom properties with light/dark values; design the dark palette independently (never invert mechanically); avoid pure white text on dark - use off-white `#e0e0e0`-`#f0f0f0` to reduce halation for users with astigmatism; re-verify contrast in the dark palette (muted accents that pass light mode may fall below 4.5:1 on dark surfaces); elevate via lighter surfaces, not shadows.

### Typography

- **Choose one typeface.** A single family with multiple weights beats a display/body pairing. If pairing, limit to two (heading + body) with proportional harmony (similar x-height, compatible rhythm).
- **Never use:** Inter, Roboto, Arial, system-ui as the sole font, Open Sans, Lato, Montserrat, Poppins, Space Grotesk. Not bad fonts - invisible through overuse. Choose something with character.
- **Good starting points:**
  - **Sans:** Geist, Satoshi, General Sans, Switzer, Cabinet Grotesk, Plus Jakarta Sans, Instrument Sans, DM Sans, Manrope, Outfit.
  - **Serif:** Newsreader, Lora, Source Serif 4, Fraunces, Crimson Pro.
  - **Mono:** JetBrains Mono, Fira Code, Berkeley Mono.
  - Suggestions, not a fixed list - the point is deliberate choice, not default.
- **Type scale.** 1.25 (major third) or 1.2 (minor third) between heading levels. Define in CSS custom properties.

### Layout

- **Avoid the three-column icon-grid.** The single most recognisable AI layout cliché: three cards, centred icons, bold titles, short descriptions. If content genuinely has three items, use a stacked list, asymmetric grid, or table instead.
- **Generous whitespace.** Padding and margins feel luxurious, not cramped. Breathing room feels intentional; dense feels cheap.
- **Asymmetry over symmetry.** Perfectly centred layouts are the path of least resistance. Subtle asymmetry (wider left column, offset heading, unequal grid) creates visual interest without sacrificing clarity.
- **Single-column for reading.** Sidebars and secondary columns compete for attention and reduce reading comfort.
- **Consistent spacing system.** A scale like 4, 8, 12, 16, 24, 32, 48, 64, 96 - only those values, no arbitrary pixels.

### Backgrounds and surfaces

- **Solid colours, not gradients, by default.** Gradients (especially blue-to-purple) are the strongest visual signal of AI-generated interfaces. If a gradient is genuinely right (hero, data viz), keep it subtle and avoid blue/purple/indigo.
- **Depth through subtle borders and shadows, not colour shifts.** 1px border in a darker shade, or a very soft box-shadow. Avoid heavy elevation (`shadow-lg`+) unless representing a true overlay.
- **No glassmorphism, aurora backgrounds, or noise textures by default.** Currently AI design clichés; use only when the specific context demands it and you can articulate why.

---

## Restrained dynamism

A completely static interface feels dead; a maximally animated one feels like a theme park. The balance sits closer to the static end - calm and quiet by default, with a few carefully chosen moments where motion adds meaning or delight. Cocktail bitters: one dash is not enough, two to four is perfect, the whole bottle ruins the drink.

### Where motion earns its place

- **Interaction feedback.** Hover/focus/active on buttons, toggles, controls - subtle colour shift, gentle scale (<=2-3%), border transition. 100-200ms, ease-out.
- **State changes.** Drawer opens, notification enters, section expands - animate so the user understands what changed. 150-300ms, ease-in-out.
- **One "moment" per page.** A staggered fade-in on first load, subtle hero parallax, animated SVG accent - just one. Your dash of bitters. A small surprise, not a performance.
- **Loading states.** Skeleton screen, progress bar, simple spinner. Branded but understated.

### Where motion does not belong

- **Continuous loops.** Nothing moves perpetually. If the user isn't interacting, the page is still.
- **Scroll-jacking.** Never override native scroll.
- **Parallax on every section.** One parallax element per page, maximum. Never on body text.
- **Entrance animations on every element.** Staggering twenty cards is a slideshow. Animate the container; let contents appear with it.
- **Animation for its own sake.** If you can't explain what the motion communicates, remove it.

### Implementation

- **CSS over JavaScript.** CSS animations are hardware-accelerated on the compositor thread. Use `transform` and `opacity`; avoid `width`, `height`, `top`, `left`, `margin`.
- **Respect `prefers-reduced-motion`.** Wrap all motion in a media query; decorative animation off, functional transitions become instant.
- **Keep durations short.** Micro-interactions 100-200ms, content transitions 200-400ms, page transitions 300-500ms max. Anything longer feels sluggish.

---

## AI design tropes: the blacklist

Not inherently bad - blacklisted because they're the statistical average of AI-generated interfaces and make your work instantly recognisable as machine-generated. Avoid unless the user explicitly requests one.

- **Purple/indigo/violet gradients.** The most common AI colour scheme (inherited from Tailwind's `indigo-500`). Avoid entirely.
- **Blue-to-purple gradient backgrounds**, especially on heroes or full-page.
- **Inter/Roboto/Arial defaults.** Choose a typeface with character.
- **Three-column card grid with centred icons.**
- **Rounded cards with `shadow-lg` on white backgrounds** - default Tailwind component aesthetic.
- **"Bento grid" dashboards with glassmorphism.** Trendy 2023-2024, now a cliché.
- **Excessive border-radius** (`border-radius: 9999px` on everything). Modest rounding (4-8px) or sharp corners - be deliberate.
- **Dark mode with neon accents** (cyan/magenta/electric blue on near-black).
- **Hero: oversized bold heading + subtitle + two buttons.** Differentiate with typography, spacing, or composition if this layout is genuinely right.
- **Decorative SVG blobs.**

When you catch yourself reaching for any of these, stop and make a different choice.

---

## UX principles

### Prime directive: fewer clicks, multiple paths

Every additional click, tap, or page load between the user and their goal is a cost.
Minimise that cost relentlessly. Flatten hierarchies, combine steps where possible, and
never force the user through a corridor when a shortcut exists.

Equally important: there should be more than one way to accomplish a task. Some users
navigate via menus, others via search, others via keyboard shortcuts, others via direct
manipulation. Do not force everyone through the same funnel. Where the interface allows
it, provide parallel paths to the same destination so users can work the way that suits
them.

These two principles reinforce each other. Multiple paths reduce clicks for different
user types; fewer clicks make each path feel fast.

### Information hierarchy

- **One primary action per view.** Make the one thing unmissable; secondary actions are visually quieter.
- **Progressive disclosure.** Show only what's needed at each step; hide advanced options, secondary info, edge cases behind expanders or secondary views.
- **Obvious interactive elements.** Buttons look like buttons; links look like links. Underline body-copy links (colour alone is insufficient). Visible hover/focus states.
- **Recognition over recall.** Users shouldn't remember information from one part of the interface to use another. Show options, use descriptive labels, keep context visible. (Nielsen: recognition beats recall.)

### System status

- **Always show what's happening.** Nielsen's first heuristic. Loading indicators for in-progress work, confirmations for saves, status for background processes. The user never wonders "did that work?"
- **Respond immediately.** Acknowledge every action within 100ms even if the result takes longer. A button that responds visually then shows a spinner beats a button that does nothing for two seconds.
- **Counts and progress.** Multi-step flows show the current step; filtered lists show match count; uploads show percentage or progress bar.

### Navigation

- **The user always knows where they are.** Active nav states, breadcrumbs for deep hierarchies, clear page titles.
- **Predictable placement.** Primary nav top or left; view-affecting actions in the page header or toolbar; destructive actions require confirmation.
- **Minimise navigation depth.** >3 clicks to reach any content means the information architecture needs rework.

### Forms and input

- **Label every input.** Visible, persistent label above or beside each field. Floating labels, placeholder-only labels, and icon-only fields are hostile to screen readers and to users who lose track while filling in.
- **Inline validation.** Errors at the point of error, not a banner at the top. Validate on blur, not every keystroke.
- **Sensible defaults.** Pre-fill what you can, pre-select the most common option.
- **Prevent errors before they happen.** Input masks, constrained selectors (date pickers over free text), disabled states for unavailable actions. (Nielsen: error prevention > good error messages.)

### Error states

- **Specific.** "Something went wrong" is useless. State what happened and what the user can do about it.
- **Kind.** Never blame the user. "Invalid input" → "Please enter a valid email address."
- **Visible.** Red border, icon, message text - all together, impossible to miss.
- **Offer a way out.** Retry button, undo option, link back to safety. Never strand the user.

---

## Review mode

When reviewing existing frontend code or design, evaluate against all the principles
above and report findings in this order:

1. **Accessibility violations**: missing alt text, broken keyboard nav, contrast
   failures, missing ARIA attributes.
2. **Readability problems**: small text, long line lengths, poor contrast, cramped
   spacing.
3. **UX issues**: unclear hierarchy, hidden actions, confusing navigation, poor
   error handling.
4. **AI trope usage**: any patterns from the blacklist.
5. **Performance concerns**: JavaScript-driven animations where CSS would suffice,
   layout thrashing, unnecessary re-renders.
6. **Aesthetic refinements**: spacing inconsistencies, colour harmony, typography
   issues.

### Review recommendations file

After completing a frontend review, produce a markdown file summarising the findings
and present it for download. The file should be self-contained.

Structure:

```
# Frontend Review: [filename(s) or component name]

**Reviewed:** [date]
**Files:** [list of files reviewed]

## Summary

[2–3 sentence overview.]

## Findings

### 1. Accessibility
### 2. Readability
### 3. UX
### 4. AI Tropes
### 5. Performance
### 6. Aesthetics

## Recommended actions

[Numbered list, ordered by priority.]
```

Save as `review-[name].md` and present for download.

---

## Checklist: run through this before presenting any frontend work

- [ ] Colour contrast meets WCAG 2.2 AA on all text (4.5:1 body, 3:1 large).
- [ ] Key tasks are reachable in the fewest clicks possible, with more than one
      path where the interface allows it.
- [ ] All interactive elements are keyboard-accessible with visible focus states.
- [ ] Focused elements are not obscured by sticky headers/footers/overlays.
- [ ] Interactive targets are at least 24x24px (prefer 44x44px for touch).
- [ ] Any drag operation has a single-pointer alternative.
- [ ] Font sizes use relative units (`rem`/`em`) for 200% text scaling.
- [ ] `prefers-reduced-motion` is respected; no decorative animation when active.
- [ ] Interface tested with `forced-colors: active`; all focus indicators, borders,
      and state changes remain visible.
- [ ] If dark mode is implemented: contrast ratios re-verified in dark palette,
      no pure white text on dark backgrounds.
- [ ] Body text is 16px+ with line height 1.5 and line length capped at ~65ch.
- [ ] No fonts from the blacklist (Inter, Roboto, Arial, etc.) used as the primary
      typeface.
- [ ] No purple/indigo gradient backgrounds.
- [ ] No three-column centred-icon card grid.
- [ ] Spacing uses a consistent scale; no arbitrary pixel values.
- [ ] Colours are defined as CSS custom properties.
- [ ] Layout works at 320px width.
- [ ] At most one decorative animation ("moment") per page/view.
- [ ] All animation durations are under 500ms.
- [ ] Every user action gets visible feedback within 100ms.
- [ ] Form inputs have visible, persistent labels.
- [ ] Error prevention is prioritised over error handling (constrained inputs,
      disabled unavailable actions, confirmation for destructive operations).
- [ ] Error states are specific, kind, visible, and offer a recovery path.
- [ ] No em-dashes in any copy: titles, headings, labels, body text, tooltips,
      error messages, alt text, ARIA labels.
- [ ] If reviewing: a recommendations markdown file has been produced and presented
      for download.
