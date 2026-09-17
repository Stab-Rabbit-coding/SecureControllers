---
name: research
description: >
  Use before dispatching any research subagent or doing external
  lookups directly. The house layer over generic deep research: source
  order, the control-slug and content-grep verification steps, house
  sources, briefing rules for fan-out, and the model-cost policy that
  stops mechanical research running on an oversized model.
---

# research

Domain: sourced external research - search, fetch, extract, verify, cite. House harness for factual research work: our sources, our verification gate, our model policy. Consult before dispatching any research subagent or doing external lookups directly.

Distinct from the built-in `deep-research` skill (which fans out search/fetch/verify/synthesize generically): this skill adds the project's own source order, the Brave Search key, the concrete control-slug + content-grep verification steps, and the model-cost discipline that prevents research work from silently running on an oversized model. Use both together where they overlap; this one is the house-specific layer.

## Configure these paths for your setup

The workflow below is built around a local-wiki-first habit. Three locations are specific to one machine; set them for your own setup and read the placeholders as those values throughout:

- `<WIKI_ROOT>` - root of your local wiki corpus, consulted before any web search.
- `<SEARCH_KEY_FILE>` - a file (such as an `.env`) holding `BRAVE_SEARCH_API_KEY`, your Brave Search API key.
- `<WIKI_INGEST_DOC>` - the doc describing how to ingest a new source into your wiki.

## Model policy

A subagent with no `model:` in its frontmatter inherits the parent session's model. On an Opus session that means every dispatched research task runs Opus by default, including the mechanical ones - overkill happens by accident, not by choice. Use the right model for the job; overkill is rarely helpful and usually just wastes tokens.

Fix it two ways: declare `model:` in the agent's own frontmatter for anything dispatched repeatedly (see `house-researcher.md`), or pass `model` on the `Agent` tool call for a one-off dispatch.

Note - the built-in `researcher` and `general-purpose` agent types **cannot be overridden by a local file**. Tested 2026-07-11: a `~/.claude/agents/researcher.md` with `model: sonnet` was ignored, and a dispatched `researcher` still loaded the built-in (no Write, no Bash, built-in system prompt). The harness reserves built-in names and only registers *new* ones. So for research, dispatch **`house-researcher`** (which does load our definition and carries `model: sonnet` + Write), or if you must use a built-in, pass `model` on the `Agent` call every time.

| Task shape | Model | Why |
| --- | --- | --- |
| Search, fetch, extract, cite a specific claim | Sonnet | Mechanical - no judgement call in the loop |
| Inventory / enumeration (list every X that matches Y) | Sonnet | Same |
| Mechanical comparison (spec vs implementation, version A vs B) | Sonnet | Comparison is structural, not evaluative |
| Summarisation of already-fetched material | Sonnet | Compression, not synthesis |
| Bulk fetch / dedup across many URLs | Haiku | Throughput matters more than judgement |
| Cross-source judgement: which of several contradictory sources is authoritative | Opus | Requires weighing evidence quality, not just reporting it |
| Adjudicating a genuine factual contradiction between sources | Opus | Same |
| Any claim where fabricating a plausible number is more likely than admitting a gap | Opus | Higher abstention discipline needed under ambiguity |

If a task doesn't clearly fit a row, default to Sonnet and escalate only the specific sub-question that needs judgement.

## Sourcing gate

**NO CLAIM WITHOUT A FETCHED URL AND A PASSING CONTENT-GREP.**

Every factual claim carries a URL the agent actually fetched, not one it constructed from memory or pattern-matched from a domain's URL structure. `UNVERIFIED` is a first-class, praised outcome, not a failure to hide - a gap honestly marked is more useful than a citation that dissolves under checking. Fleet agents have fabricated plausible-looking Wayback Machine timestamps when asked for archive URLs; the same failure mode applies to any URL an agent is tempted to guess rather than fetch.

HTTP 200 alone proves nothing - many sites soft-404 (serve a templated "not found" page with a 200 status). Two checks, both required, before a claim is marked verified:

**1. Control-slug test.** Fetch a deliberately bogus slug on the same domain and confirm it does not return 200:

```bash
curl -s -o /dev/null -w "%{http_code}\n" "https://example.com/definitely-not-a-real-page-xyz123"
```

If this returns 200, the domain soft-404s and status codes on it cannot be trusted at all - fall back entirely to content verification.

**2. Content grep.** Fetch the actual cited URL and grep the page body for the specific keyword or fact being claimed, not just confirm it loaded:

```bash
curl -s "https://example.com/real-page" | grep -io "the specific claimed fact or figure"
```

No match means the page doesn't say what's being cited - downgrade to `UNVERIFIED` or drop the claim, don't keep the citation.

If either check cannot be run (no `curl`, no shell access, a WebFetch-only environment), say so explicitly in the output rather than reporting the claim as verified anyway.

Skipping either check means the claim is unverified, not verified-with-caveats.

## House sources

1. **Run `wiki-first` before any web search.** It queries the local wiki corpus (`<WIKI_ROOT>`) and returns a verdict to act on: `ANSWERED` is a checked, cited answer that needs no web search; `PARTIAL` sends you to the web only for the parts it lists as unestablished; `COULD_NOT_ESTABLISH` means search now. See `wiki-first` for the query and verdict handling; don't restate its mechanism here.
2. **Brave Search** for web queries where the wiki has no coverage. The key lives in `<SEARCH_KEY_FILE>` as `BRAVE_SEARCH_API_KEY`:

   ```bash
   curl -s -H "X-Subscription-Token: $BRAVE_SEARCH_API_KEY" \
     "https://api.search.brave.com/res/v1/web/search?q=<url-encoded query>"
   ```

3. No Firecrawl key is present on this machine. Don't write or follow instructions that assume one.
4. **Ingest after lookup.** Once an external lookup returns something worth keeping, write it into the wiki per `<WIKI_INGEST_DOC>` (raw source under `raw/`, summary page under `wiki/sources/`, index and log updated) before the task is considered complete. An external fact that never makes it into the wiki gets re-fetched, or worse re-guessed, next time.

## Append as you go - survive interruption

The report file is the deliverable; the agent's chat reply is a summary of it. Write the file incrementally, not in one block at the end:

1. Write a skeleton file (question, empty Findings, empty Gaps, `Status: IN PROGRESS`) **before** the first search.
2. Append each finding to it the moment it passes the verification gate, while the source is in front of you.
3. Flip `Status` to `DONE` only when the research is actually complete.

A run that is interrupted, killed, or hits its turn limit at 90% complete must still leave 90% of the findings on disk. Holding findings in context and writing once at the end means an interruption loses everything - which bit us when two research agents with no Write tool had to dump long findings inline. Give every research subagent Write access and this rule.

## Briefing rules for fan-out

When dispatching multiple research subagents:

- Give each one the specific paths or domains in scope, the question its findings need to answer, an **output file path** to append to, and the sourcing gate above spelled out - never "based on your findings, fix it."
- Grant the subagent Write access. Without it, a subagent with a long finding has no way to persist it and either truncates or dumps it inline, which is worse for everyone reading the result.
- State the model per dispatch (from the table above) rather than leaving it to inherit by default. Prefer `house-researcher` (loads our definition) over the built-in `researcher` (does not).

## Red Flags - STOP

| Excuse | Reality |
| --- | --- |
| "The URL returned 200, so it's real" | 200 confirms the server responded, not that the page says what's claimed - soft-404s pass this check |
| "The URL pattern matches the site's other pages" | A plausible URL is not a fetched URL - fetch it or mark unverified |
| "I'm confident this is roughly right" | Confidence is not a citation - either it's sourced or it's flagged |
| "Writing it to the wiki can happen later" | Later rarely happens - ingest before closing the task, not after |
| "The subagent's summary is probably accurate" | A summary is a claim like any other - it needs the same gate |

## Guiding principle

A well-marked gap is a deliverable. A confident citation that fails a content-grep is a defect, not a stronger answer.
