---
name: songwriting
description: Use when writing, structuring, or polishing a song or its lyrics, including turning a rough idea or lyric sheet into a sectioned song with production direction for a text-to-music generator; especially for the operator's own tracks.
---

# Songwriting

## Overview

Co-write and structure songs that feel human and unmistakably his. Every session produces two things: the lyrics, and the per-section musical direction. Core principle: mean it all the way. Sincerity is the engine of both the love songs and the jokes; the moment you wink at a silly song, it dies.

## When to use

- Turning a rough lyric or idea into a full, sectioned song.
- Structuring lyrics for a text-to-music generator (Suno-style).
- Polishing lines: rhyme, syllable flow, imagery.
- Writing in his voice for his catalogue. Load `his-signature.md` first if it is present (see References).

Not for: music-theory questions (use `song-craft-reference.md`) or non-song prose.

## Hard rules

1. **Brackets hold musical annotations ONLY.** The generator sings any non-musical prose inside `[ ]`. Instrumentation, arrangement, dynamics, tempo, and vocal delivery go in brackets; keep them as terse comma-lists in Suno's native form (see `suno-format.md`), not prose sentences. Rhyme notes, meaning, callbacks, and craft commentary stay out of the bot-fed file (keep them in chat, or a separate notes file).
2. **No artist names.** Describe a style by its traits (tempo, instrumentation, energy), never by naming an artist or track. Applies to brackets, feel lines, and the styles field. Some ordinary music words also trip the generator's artist-name filter (a band shares the word); keep the running list in `blocked-words.md` and use the descriptive alternative.
3. **No darkness-as-menace imagery.** Let light, fire, cold, or entropy carry the threat instead. Standing cultural-sensitivity line.
4. **Mind the field limits:** the style field is about 1,000 characters, the lyrics about 5,000 (practical sweet spot ~3,000); community-reported, so verify with `wc -m`. See `suno-format.md`.

## Process

1. Gather the real material: the specific memory, the private in-jokes, the actual detail. Object-write it first (senses only, no feeling-words) before drafting a line.
2. Pick form and style traits. Match structure to genre (build-and-drop; verse / pre-chorus / chorus / bridge). Draft words and arrangement together; he thinks in both.
3. Draft against the craft floor (`song-craft-reference.md`), plus `his-signature.md` if it is present. Without it, ask the writer for their own voice traits rather than inventing them; everything else in this skill works unchanged.
4. Tighten: cut syllables until the lines move; prefer slant and internal rhyme; one concrete, un-generic image per section; plant early, pay off late.
5. Review pass: get an independent read from more than one model (for example a Fable pass and a Sonnet pass). Creative judgement varies by model, so compare rather than average. Check against the AI-tell list.
6. Iterate in the open: show adopted-versus-rejected options; give the real note, not praise; expect him to out-write a suggestion and build on it.

## Quick reference

| Want | Do |
| --- | --- |
| Line feels clunky | Cut syllables; read it aloud; land the key word just before a musical gap |
| Rhyme too sing-song | Swap perfect end-rhyme for slant, internal, or assonance |
| Section blurs into the next | Change syllable density or energy; give the bridge one job (turn, reveal, or stakes-raise) |
| Ending | Match the close to the song's spirit; earnest endings get no big button, just gone |
| Structure a bot song | Section tags in brackets (musical only), then lyrics; styles given as traits |

## Common mistakes

- Craft notes inside `[ ]`: the bot sings them. Keep brackets musical.
- Naming an artist for the vibe: describe the traits instead.
- Packed lines: they fight the melody. Cut.
- Forced perfect rhyme every line: reads as AI or nursery rhyme. Vary it.
- Generic imagery: object-write the real memory; use one camera-testable detail.

## References

- `his-signature.md`: a personal voice reference, **not distributed with this skill**. It is a private profile of one writer's style, so it is kept local and is absent from the published package. If it is not in this directory, skip it: the rest of the skill stands on its own, and any writer can supply their own equivalent as a file of the same name.
- `song-craft-reference.md`: song form, prosody, rhyme, harmony, build-and-drop conventions, AI tells.
- `suno-format.md`: the native Suno input template (styles block, section tags, terse inline cues).
- `blocked-words.md`: plain music words the generator misreads as artist names.
- Deeper sourcing: llm-wiki `sources/songwriting-craft-and-ai-lyric-tells.md`.
