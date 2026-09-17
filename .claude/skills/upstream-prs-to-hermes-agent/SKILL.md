---
name: upstream-prs-to-hermes-agent
description: Sends a change from a fork up to NousResearch/hermes-agent, or reviews a branch before it goes. Use when preparing an upstream PR, writing its body, or checking a fix is still needed upstream at all. Covers their CONTRIBUTING rules (and the one that is wrong), the contributor-check gate, the non-hermetic test suite, and why the human opens the PR.
---

# Upstream PRs to hermes-agent

Domain: open-source contribution to `NousResearch/hermes-agent`. Use when sending a change from a fork up to that repository, or reviewing a branch before it goes.

## What it does

Takes a change that already works locally and gets it into the shape the maintainers actually ask for, rather than the shape we remember them asking for. Their `CONTRIBUTING.md` and PR template are the source of truth, they change, and this skill is a stale copy of them by definition. So step 1 is always to re-read theirs.

## The rule that outranks the rest of this file

**Read their rules from the upstream tree every time. If this skill disagrees with what you read, they are right and this skill is out of date.** Fix the skill afterwards.

```bash
git fetch upstream
git show upstream/main:CONTRIBUTING.md
git show upstream/main:.github/PULL_REQUEST_TEMPLATE.md
git show upstream/main:AGENTS.md                      # architecture and workflow rules
git ls-tree -r --name-only upstream/main | grep -i '\.github/workflows'   # the gates that will actually run
```

Read the template as a *form to fill in*, not as prose to paraphrase. A maintainer scanning for its headings should find them.

## Step 1: does the defect still exist upstream?

Before anything else, check the code you are fixing at `upstream/main`, not in the fork.

```bash
git show upstream/main:path/to/file.py | sed -n 'START,ENDp'
```

A fork accumulates deletions and reverts. A bug that is real in the fork may have been fixed upstream months ago, and the fork simply lost the fix. If it is already fixed upstream, there is no PR to open: the finding belongs in the fork, and you have just discovered that the fork dropped an upstream hunk, which is worth reporting on its own.

**This is not hypothetical.** We prepared a fallback `api_mode` fix, and upstream already had the identical line, with issue references. The fork's rolling patch had eaten it.

## Step 2: search for duplicates

Their `CONTRIBUTING.md` asks for this, and its example command is wrong: it prints `gh search prs --repo ... --state all`, but `--state` only accepts `open` or `closed`. Omit the flag to search all states.

```bash
gh search prs    --repo NousResearch/hermes-agent "<terms>" --limit 5 --json number,title,state -q '.[] | "#\(.number) [\(.state)] \(.title)"'
gh search issues --repo NousResearch/hermes-agent "<terms>" --limit 5 --json number,title,state -q '.[] | "#\(.number) [\(.state)] \(.title)"'
```

Search several phrasings: the symptom, the identifier, the file. If an open PR already covers it, improving theirs beats opening a competing one.

If a search returns nothing, check the command actually ran. An invalid flag plus a redirected stderr looks exactly like a clean result.

## Step 3: shape the branch

- Base it on `upstream/main`, not on the fork's `main`. Confirm the tip: `git log --oneline -1 upstream/main`.
- Name it their way: `fix/`, `feat/`, `docs/`, `test/`, `refactor/` + short description. Fork-local prefixes (`upstream-fix/`, `restore/`) are ours, not theirs.
- Conventional Commits for the message: `<type>(<scope>): <description>`. Scopes in use: `cli`, `gateway`, `tools`, `skills`, `agent`, `install`, `whatsapp`, `security`, and others.
- One logical change per PR. No drive-by refactors riding along.

## Step 4: test, and only claim what you ran

Use the wrapper. On this repository a bare `pytest` is not hermetic: it drives the real text-to-speech tool and spawns a real browser.

```bash
bash scripts/run_tests.sh                      # full suite; the fork's copy may lack the +x bit
bash scripts/run_tests.sh tests/path/file.py   # single file
```

Their checklist contains "I've run `pytest tests/ -q` and all tests pass". If you ran four files, you have not run that. Either run the suite or leave the box unticked and say what you did run. An unticked box costs a review comment; a wrongly ticked one costs their trust.

State the platforms you tested on. They ask for this explicitly, and "Linux only" is a fine answer when it is the true one.

## Step 5: check the gates that will run

`.github/workflows/contributor-check.yml` fails the PR if the commit author's email is neither in `AUTHOR_MAP` in `scripts/release.py` nor a GitHub `+user@users.noreply.github.com` noreply address.

```bash
git log -1 --format='%ae' <branch>
git show upstream/main:scripts/release.py | grep -F "<that-email>"
```

If it is absent and is not a noreply address, the PR needs an `AUTHOR_MAP` entry.

Their CI also gates first-time contributors: the run for your PR sits at `conclusion: action_required` until a maintainer approves it, and **no check runs attach until they do**, so `gh pr checks` reports "no checks reported". That is not a failure on your side and nothing you can do will change it. Do not read it as a broken PR.

## Step 6: write the body into their template

Fill their headings: **What does this PR do** / **Related Issue** / **Type of Change** / **Changes Made** (with file paths) / **How to Test** (numbered reproduction, plus proof the fix works) / **Checklist** / platform tested.

For the prose inside it:

- Lead with the user-visible effect, then the mechanism. "The suite spoke through the speakers" before "`monkeypatch.delenv` records no undo entry".
- Cite `file:line` against the tree you name. A line number measured in your patched working copy is not a line number in `upstream/main`. Verify with `git show <ref>:<path>`.
- State what you tested. Do not append a paragraph defending the change against objections nobody has raised.
- Keep it as short as it can be while still resolving. Maintainer time is the scarce resource.

## Step 7: the human opens it

Opening a PR publishes to a public repository under the user's name and is not ours to trigger. Prepare the branch, prepare the body, show both, and ask.

Before asking, re-read the body for anything the user may not want disclosed upstream: internal paths, machine details, incident specifics, whose desk something happened on. Flag it and offer a depersonalised wording; the fact usually survives the edit.

One PR at a time. Until the last one is merged or closed, the next one waits, however ready it is. A queue of open PRs from one contributor reads as bombardment, and costs the goodwill the first one earned.

## If X then Y

- If the fix is already upstream, then say so and stop. There is no PR.
- If a rule in their `CONTRIBUTING.md` contradicts this skill, then follow theirs and update this file.
- If a command returns nothing, then check it did not error before reporting "no results".
- If you cannot honestly tick a checklist item, then leave it unticked and say why in the body.
- If you are unsure whether a claim in the body is true, then verify it against the named tree or drop it. An unverified detail in a public PR is worse than a missing one.
- If a PR from us is already open, then the next one waits.

## Verification before it goes

- [ ] Their `CONTRIBUTING.md` and PR template re-read **this session**, from `upstream/main`.
- [ ] Defect confirmed to exist at `upstream/main`.
- [ ] Duplicate search run, with commands that actually executed.
- [ ] Branch named `fix/…`-style, based on `upstream/main`.
- [ ] Commit message is Conventional Commits.
- [ ] Tests run via `scripts/run_tests.sh`; every ticked box is one you actually did.
- [ ] Author email passes `contributor-check.yml`.
- [ ] Body fills their template headings; `file:line` citations verified against the named ref.
- [ ] Platforms tested, stated.
- [ ] No other PR of ours is open and unresolved.
- [ ] Human has seen the body and said yes.
