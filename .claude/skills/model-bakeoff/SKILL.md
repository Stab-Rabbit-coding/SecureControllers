---
name: model-bakeoff
description: Use when choosing between models or prompts by measuring them against ground truth - benchmarking extraction, classification or OCR candidates, comparing an incumbent against alternatives, or when a model evaluation has produced numbers you are about to act on.
---

# Model Bake-off

## Overview

You are comparing candidates against ground truth to pick one. The danger is not
picking the wrong model. The danger is **producing a number that looks like
evidence and is not**, then spending real money on it.

**Core principle: most of what kills a bake-off is not the model. It is the
harness, the sample, and the arithmetic.**

This skill assumes you already know to build ground truth by hand, to measure
recall as well as precision, and not to trust the incumbent's own output as
truth. Baseline testing showed agents reliably get those right. The five below
are the ones they reliably get wrong.

## The five that get missed

### 1. A failed request is not a model error

Rate limits, timeouts, transient 5xx, an upstream returning no choices: none of
these are facts about the model. Score them as misses and you have measured your
own infrastructure.

- Record `error` on the page/item, distinct from "the model returned nothing".
- Report failures separately. Never fold them into an accuracy or recall figure.
- **Retry the failures before you compare anything.** A candidate that never saw
  the input has not been measured on it.

> A 429 storm cost one candidate 7 of 46 pages. Its recall read as 74%. Retried,
> it was fine. That number would have eliminated the best model in the field.

### 2. Failures must stay local and visible

One bad item must not be able to end the run.

- Catch parse errors where you catch API errors: per item, recorded, continue.
  A model returning a bare JSON list instead of an object is normal, not fatal.
- **Set a per-request timeout.** A model that hangs is a model that fails. Without
  a timeout, one stalled candidate silently blocks every candidate behind it.
- Never silently drop a failed item. A vanished item cannot be counted as missed,
  so recall quietly flatters the model.

### 3. Compute the do-nothing baseline

What score does a model get for **never looking at the input**? Answer the
majority class every time, and see.

- Print it beside every result. A number without it is not interpretable.
- **Compute it from the current test set at run time. Never hard-code it** - it is
  a property of the sample, so it changes whenever the sample does. Three stale
  values circulating at once is how a gate stops gating.
- Report accuracy on the **non-majority items separately**. That is the number
  that says whether the model can read, rather than guess.

> An incumbent that had processed 40,000 rows scored 65.1% where the do-nothing
> baseline was 63.4%. It was 1.7 points better than not opening the page. Nobody
> had ever computed the baseline.

### 4. Measure cost, do not extrapolate it

- Run a handful of REAL items, record **actual input and output tokens**, and
  price from those.
- One sample item is not a measurement. Items vary: a dense page can be 3x a
  sparse one.
- Reasoning tokens bill as output and no estimator sees them. Treat any
  pre-run estimate as a floor and say so.

> A cost extrapolated from a single probe page said $47. Measured across 46 real
> pages, it was $70. The estimate was presented to the operator before the
> correction.

### 5. One run is not a measurement

- Run each candidate at least twice on the same items. Disagreement between a
  model and itself bounds how much you can trust its margin over another.
- Separate the runner from the scorer. The runner spends money and saves raw
  output to disk; the scorer reads that output and is free, offline, and
  re-runnable forever. You will re-score more often than you expect, and you
  should never pay twice for the same read.

## Failure modes worth naming in the report

Aggregate accuracy hides the errors that cost the most money.

| Check | Why |
|---|---|
| **Correlated / whole-item collapse** | Every row on a page sharing one wrong value is not noise, it inverts the item. Count collapsed items, not just wrong rows. |
| **Fabrication rate** | A confident wrong value in-distribution is the only error that spends money. "Low" is not a target; state it separately from accuracy. |
| **Fields the schema never asked for** | If the output schema omits a flag, no model will return it, and every model will look equally bad at it. That is your bug, not theirs. |
| **Values normalised before comparison** | `2/19/2026` vs `02/19/2026` compared as strings is a fake error rate. Parse, then compare. |

## Quick reference

```
Before running:
  [ ] ground truth built independently of every candidate
  [ ] do-nothing baseline computed from THIS set
  [ ] per-request timeout set
  [ ] runner saves raw output; scorer is separate and free

After running, before comparing:
  [ ] failed requests identified, retried, and reported separately
  [ ] cost taken from measured tokens, not an estimate
  [ ] each candidate run at least twice
  [ ] values normalised before comparison

In the report:
  [ ] baseline printed beside every score
  [ ] accuracy on non-majority items, separately
  [ ] collapsed items, fabrication rate, failures - each as its own number
```

## Rationalisations

| Excuse | Reality |
|---|---|
| "The failures are probably the model's fault" | Then say which, with the error. A 429 is not a misread. |
| "One page's tokens are enough to price it" | Items vary 3x. Measure a sample, not an example. |
| "The baseline is obviously low here" | Compute it. The one that shocked everyone was 63.4%, and the incumbent scored 65.1%. |
| "Running twice doubles the cost" | Scoring is free if you saved the output. Re-reading is not. |
| "The winner is clear, the details don't change it" | The details eliminated the best model in the field once already. |

## Red flags - stop and re-measure

- A candidate has failed items and you are about to compare scores anyway
- Your cost figure came from one item, or from a price list rather than a token count
- You cannot say what the do-nothing baseline is on this exact test set
- A model is "slow" and you are waiting rather than timing it out
- The evaluation crashed and you are re-running the whole thing rather than the failures
- You are about to promote a model on a single run
