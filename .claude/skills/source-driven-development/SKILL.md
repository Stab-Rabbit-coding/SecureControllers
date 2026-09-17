---
name: source-driven-development
description: Grounds every implementation decision in official documentation. Use when you want authoritative, source-cited code free from outdated patterns. Use when building with any framework or library where correctness matters.
---

# Source-Driven Development

## Overview

Every framework-specific code decision must be backed by official documentation. Don't implement from memory — verify, cite, and let the user see your sources. Training data goes stale, APIs get deprecated, best practices evolve. This skill ensures the user gets code they can trust because every pattern traces back to an authoritative source they can check.

## When to Use

- The user wants code that follows current best practices for a given framework
- Building boilerplate, starter code, or patterns that will be copied across a project
- The user explicitly asks for documented, verified, or "correct" implementation
- Implementing features where the framework's recommended approach matters (forms, routing, data fetching, state management, auth)
- Reviewing or improving code that uses framework-specific patterns
- Any time you are about to write framework-specific code from memory

**When NOT to use:**

- Correctness does not depend on a specific version (renaming variables, fixing typos, moving files)
- Pure logic that works the same across all versions (loops, conditionals, data structures)
- The user explicitly wants speed over verification ("just do it quickly")

## The Process

```text
DETECT ──→ FETCH ──→ IMPLEMENT ──→ CITE
  │          │           │            │
  ▼          ▼           ▼            ▼
 What       Get the    Follow the   Show your
 stack?     relevant   documented   sources
            docs       patterns
```

### Step 1: Detect Stack and Versions

Read the project's dependency file to identify exact versions:

```text
package.json    → Node/React/Vue/Angular/Svelte
composer.json   → PHP/Symfony/Laravel
requirements.txt / pyproject.toml → Python/Django/Flask
go.mod          → Go
Cargo.toml      → Rust
Gemfile         → Ruby/Rails
```

State what you found explicitly:

```text
STACK DETECTED:
- React 19.1.0 (from package.json)
- Vite 6.2.0
- Tailwind CSS 4.0.3
→ Fetching official docs for the relevant patterns.
```

If versions are missing or ambiguous, **ask the user**. Don't guess — the version determines which patterns are correct.

### Step 2: Fetch Official Documentation

Fetch the specific documentation page for the feature you're implementing. Not the homepage, not the full docs — the relevant page.

**Source hierarchy (in order of authority):**

| Priority | Source | Example |
| ---------- | -------- | --------- |
| 1 | Official documentation | react.dev, docs.djangoproject.com, symfony.com/doc |
| 2 | Official blog / changelog | react.dev/blog, nextjs.org/blog |
| 3 | Web standards references | MDN, web.dev, html.spec.whatwg.org |
| 4 | Browser/runtime compatibility | caniuse.com, node.green |

**Not authoritative — never cite as primary sources:**

- Stack Overflow answers
- Blog posts or tutorials (even popular ones)
- AI-generated documentation or summaries
- Your own training data (that is the whole point — verify it)
- **Code comments, `NOTE:`s and commit messages in your own repo.** These are claims at the same evidentiary level as a finding, not facts to reason from. An in-tree claim is covered by no test and contradicted by nothing in the repo, so it reads like established fact and the next reader builds on it. A neowall comment justified a hardcoded value with "KWin 6 closes a BACKGROUND surface that asks to ignore other exclusive zones", and a commit blamed the NVIDIA driver. The machine is an AMD card running X11/Cinnamon: no KDE, no Wayland, no NVIDIA. The behaviour could not have been observed, and the comment was covering a regression the protocol header in `protocols/` contradicted outright.

**If a claim cites a platform, establish that someone had that platform.** `lspci`, `$XDG_CURRENT_DESKTOP`, `$XDG_SESSION_TYPE` and `uname` settle it in seconds, and an unobservable claim is a fabricated one. Claims citing a spec, man page or protocol header are **not** suspect: verify against the source and move on. This is a check on platform-behaviour assertions, not a hunt through every comment in the tree.

Never write a comment asserting external behaviour you have not observed. If you cannot verify it, mark it `UNVERIFIED:` rather than dressing a guess as a measurement.

**Be precise with what you fetch:**

```text
BAD:  Fetch the React homepage
GOOD: Fetch react.dev/reference/react/useActionState

BAD:  Search "django authentication best practices"
GOOD: Fetch docs.djangoproject.com/en/6.0/topics/auth/
```

After fetching, extract the key patterns and note any deprecation warnings or migration guidance.

When official sources conflict with each other (e.g. a migration guide contradicts the API reference), surface the discrepancy to the user and verify which pattern actually works against the detected version.

### Step 3: Implement Following Documented Patterns

Write code that matches what the documentation shows:

- Use the API signatures from the docs, not from memory
- If the docs show a new way to do something, use the new way
- If the docs deprecate a pattern, don't use the deprecated version
- If the docs don't cover something, flag it as unverified

**When docs conflict with existing project code:**

```text
CONFLICT DETECTED:
The existing codebase uses useState for form loading state,
but React 19 docs recommend useActionState for this pattern.
(Source: react.dev/reference/react/useActionState)

Options:
A) Use the modern pattern (useActionState) — consistent with current docs
B) Match existing code (useState) — consistent with codebase
→ Which approach do you prefer?
```

Surface the conflict. Don't silently pick one.

### Step 4: Cite Your Sources

Every framework-specific pattern gets a citation. The user must be able to verify every decision.

**In code comments:**

```typescript
// React 19 form handling with useActionState
// Source: https://react.dev/reference/react/useActionState#usage
const [state, formAction, isPending] = useActionState(submitOrder, initialState);
```

**In conversation:**

```text
I'm using useActionState instead of manual useState for the
form submission state. React 19 replaced the manual
isPending/setIsPending pattern with this hook.

Source: https://react.dev/blog/2024/12/05/react-19#actions
"useTransition now supports async functions [...] to handle
pending states automatically"
```

**Citation rules:**

- Full URLs, not shortened
- Prefer deep links with anchors where possible (e.g. `/useActionState#usage` over `/useActionState`) — anchors survive doc restructuring better than top-level pages
- Quote the relevant passage when it supports a non-obvious decision
- Include browser/runtime support data when recommending platform features
- If you cannot find documentation for a pattern, say so explicitly:

```text
UNVERIFIED: I could not find official documentation for this
pattern. This is based on training data and may be outdated.
Verify before using in production.
```

Honesty about what you couldn't verify is more valuable than false confidence.

**Citing code rather than docs:**

The same version discipline applies when the source is a source file, and it is easier to get wrong there. A URL with no version on it looks obviously weak. A `file:line` with no commit on it looks complete.

**A `file:line` is true only relative to a named tree.** Verify it against that tree, not in your editor:

```bash
git show 5aa206f:src/wayland_core.c | sed -n '536p'
```

A neowall commit message said `wl->initialized` is set at `wayland_core.c:536` of upstream commit `5aa206f`. It was right. A reviewer "corrected" it to `:544`, which is where the line sits once our own patch is applied: it had read the working tree rather than the commit the sentence cited. The false version went into the commit message and then into a draft issue for an upstream maintainer, and it survived three reviews. It was caught when someone finally read the blob.

- **Pin the ref the way you pin the version.** "`wayland_core.c:536` of `5aa206f`" is a citation. "`wayland_core.c:536`" is a citation to whatever you happen to have checked out, and it expires the next time anyone edits the file.
- **Opening the working copy does not verify a citation that names another commit.** It is the natural move and it silently measures the wrong tree, because line numbers move under the very patch the sentence is describing.
- **Every citation in an outward-facing artefact gets a blob-level check before it ships**, and cite only refs the reader can resolve. A fork-local scaffolding hash dangles for everyone but you.

## Common Rationalizations

| Rationalization | Reality |
| --- | --- |
| "I'm confident about this API" | Confidence is not evidence. Training data contains outdated patterns that look correct but break against current versions. Verify. |
| "Fetching docs wastes tokens" | Hallucinating an API wastes more. The user debugs for an hour, then discovers the function signature changed. One fetch prevents hours of rework. |
| "The docs won't have what I need" | If the docs don't cover it, that's valuable information — the pattern may not be officially recommended. |
| "I'll just mention it might be outdated" | A disclaimer doesn't help. Either verify and cite, or clearly flag it as unverified. Hedging is the worst option. |
| "This is a simple task, no need to check" | Simple tasks with wrong patterns become templates. The user copies your deprecated form handler into ten components before discovering the modern approach exists. |

## Red Flags

- Writing framework-specific code without checking the docs for that version
- Using "I believe" or "I think" about an API instead of citing the source
- Implementing a pattern without knowing which version it applies to
- Citing Stack Overflow or blog posts instead of official documentation
- Using deprecated APIs because they appear in training data
- Reasoning from an in-tree comment or commit message as though it were a verified fact
- Settling a `file:line` citation by opening the working copy when the sentence names a different commit
- Citing a `file:line` with no ref behind it, or a ref the reader cannot resolve
- Asserting behaviour of a platform (GPU, compositor, kernel, browser) that nobody working on this code has ever run
- Not reading `package.json` / dependency files before implementing
- Delivering code without source citations for framework-specific decisions
- Fetching an entire docs site when only one page is relevant

## Verification

After implementing with source-driven development:

- [ ] Framework and library versions were identified from the dependency file
- [ ] Official documentation was fetched for framework-specific patterns
- [ ] All sources are official documentation, not blog posts or training data
- [ ] Code follows the patterns shown in the current version's documentation
- [ ] Non-trivial decisions include source citations with full URLs
- [ ] No deprecated APIs are used (checked against migration guides)
- [ ] Conflicts between docs and existing code were surfaced to the user
- [ ] Every `file:line` citation names a ref, and was checked against that ref's blob (`git show <ref>:<path>`) rather than the working copy
- [ ] Anything that could not be verified is explicitly flagged as unverified
- [ ] No decision rests on an in-tree comment or commit message that was itself never verified
- [ ] Any comment asserting external platform behaviour is either sourced to a spec/doc or marked `UNVERIFIED:`
