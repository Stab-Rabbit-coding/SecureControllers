# Suno input format (template)

How to structure a song so Suno renders it well. Combines Suno's own generated output with official-docs research (llm-wiki `sources/suno-prompting-best-practice.md`).

## Two fields, two syntaxes

Suno takes a **Style** field and a **Lyrics** field; they behave differently.

- **Lyrics box:** plain text is sung verbatim; `[bracket]` text is an instruction/tag, not sung (official). Recognised tags are honoured. It WILL sing bracket content that is anything but musical direction - confirmed firsthand, whatever the docs imply. Keep bracket content to recognised tags and terse musical cues only; never craft notes, meaning, or commentary.
- **Style box:** bracket-free keywords only - genre, mood, instrumentation traits, vocal tone, tempo. Brackets there reportedly break genre parsing. No artist names (officially blocked; describe by trait). Negative prompts: the Exclude Styles toggle (paid tiers), or inline "no X" / "without X".

## Limits (community-reported, not official - verify with `wc -m`)

- Style field ~1,000 characters. Lyrics ~5,000 (practical sweet spot ~3,000).

## Recognised bracket tags (official glossary)

- **Structure:** `[Intro] [Verse] [Pre-Chorus] [Chorus] [Bridge] [Drop] [Break] [Outro]`
- **Vocal:** `[Falsetto] [Belt] [Melisma] [Vocal Run] [Harmonization] [A Cappella] [Call and Response] [Scat] [Crooning] [Rapping]`
- **Instrumental-forcing:** `[Instrumental Break]`; `[a cappella]` strips instruments but keeps vocals.

## Working-doc shape

Keep one `.md` per song; copy the STYLE block into the style box and the tagged body into the lyrics box.

```text
# Title

STYLE (paste into style box, bracket-free):
comma list: genre, mood/energy, instrumentation with playing technique, vocal tone, BPM, Key, time; optional: no <excluded>

LYRICS (paste into lyrics box):
[Intro]
[short comma cue: instruments]
[Verse 1]
[optional vocal cue]
lyric lines, minimal punctuation
[Chorus] [Belt]
lyric line (ad-lib)
[Instrumental Break]
[Bridge]
...
[Outro]
...
```

## Rules

- **Style block:** name specific playing techniques (slap-and-pop bass, palm-muted riff, 16th-note scratches, tight dry snare), the vocal (male tenor, chest plus falsetto), synth/keys, arrangement density, then the numbers (BPM, Key, time). Traits only, no artist names, bracket-free.
- **Section tags:** short, one per section, from the recognised list.
- **Inline cues:** terse bracketed comma-lists, not sentences: `[slap bass, syncopated clean guitar, tight drums]`, `[bass solo]`, `[falsetto]`. Section instrument cue on its own line under the tag; vocal cue inline.
- **Brackets carry no meaning, rhyme, or craft notes** - those stay out of the file.
- **Ad-libs / backing:** in parentheses in the lyric: `(mmm)`, `(No no)`.
- **Lyrics:** minimal punctuation, no em-dashes; spell tricky bits phonetically (`X-Y-P-Q-R`). Instrumental section = a tag plus a bracket cue, no lyric lines.

## Note on instruction density (Suno v5.5)

The earlier finished songs use full-sentence brackets and rendered well. On v5.5 (current), **dense, rich instructions beat sparse ones** - more texture and personality in the refrains and vocals. The community "keep it terse" advice likely reflects older models. Default to rich, specific direction on v5.5; keep it trait-based and bracket-free in the style box. Terse comma-lists remain safe, just not the ceiling. Suno renders in pairs; the second take is often the stronger one.
