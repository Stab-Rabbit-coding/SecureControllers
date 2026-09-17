---
name: github-actions
description: >
  Create, debug, and review GitHub Actions workflows. Covers reusable
  workflows, composite actions, custom JS/Docker actions, matrix builds,
  OIDC deploys, self-hosted runners. Security-first with SHA pinning and
  artifact attestations.
paths: ".github/workflows/*.yml, .github/workflows/*.yaml, .github/actions/*/action.yml"
---

# GitHub Actions Skill

Generate production-grade workflows with security and maintainability baked in.

## No workflow ships untested

A workflow is not correct because it parses. Before you call one ready: validate the YAML against the GitHub Actions schema; dry-run it locally with `act` (or an equivalent) wherever the workflow allows; inspect the actual execution logs for errors and warnings rather than trusting the green tick; and confirm every referenced action resolves to a real, available version. A workflow that has skipped any of these steps is unverified - say so instead of presenting it as ready. Valid YAML is not a valid workflow; passing on your machine is not passing on the runner, whose environment differs in ways small changes expose; and production monitoring catches a defect too late, after it has already burned minutes, leaked a secret, or shipped a broken deploy. Where a step genuinely cannot be validated without a live runner, name which steps need live-runner verification rather than asserting the whole workflow is correct.

## Core Principles

GitHub Actions runs untrusted code with access to secrets, deployment credentials, and repo write permissions. Every default here minimises blast radius when something goes wrong.

### 1. Pin actions by full SHA, not tag

Tags are mutable; a compromised upstream can push malicious code to an existing tag. SHA pinning makes workflows reproducible and tamper-resistant.

```yaml
# Good - SHA-pinned with readable comment
- uses: actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd # v6.0.2

# Acceptable - tag with reminder to pin
- uses: actions/checkout@v6 # TODO: pin to SHA

# Bad - bare tag, no reminder
- uses: actions/checkout@v4
```

Always keep the human-readable tag as an inline comment.

**Get current SHAs** from the action's GitHub releases page (e.g. `https://github.com/actions/checkout/releases`). If you can't check, use the tag with `# TODO: pin to SHA` and tell the user. Recommend Renovate or Dependabot for the `github-actions` ecosystem.

**Never fabricate SHAs** - a wrong SHA silently fails at checkout. If unsure, use the tag.

**Immutable actions (2026):** GitHub now supports publishing actions as immutable OCI packages to ghcr.io via `actions/publish-immutable-action`. Tags on immutable actions can't be overwritten once published (infrastructure-level protection against tag hijacking, e.g. the March 2026 trivy-action incident). Reference by immutable tag when consuming; consider immutable publishing for your own actions.

**Action allowlisting (Feb 2026):** Repo/org admins can restrict permitted actions and reusable workflows on all plans. Recommend enabling as an additional layer beyond SHA pinning.

### 2. Least-privilege permissions

Declare top-level `permissions` and restrict to what's needed. The default `GITHUB_TOKEN` has broad write access.

```yaml
permissions:
  contents: read
```

Grant more at the job level if specific jobs need it (publishing, releases), not workflow-level.

### 3. Explicit shell and failure behaviour

Set `defaults.run.shell: bash` at workflow level (not `sh`) for `set -eo pipefail` semantics by default.

```yaml
defaults:
  run:
    shell: bash
```

### 4. Concurrency control

Prevent wasted runner minutes on superseded pushes:

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

Disable `cancel-in-progress` for deploys - you don't want a half-deployed state.

### 5. Secrets and environment variables

- Never echo secrets or use them in `if:` conditions (leaks into logs).
- Prefer GitHub Environments with protection rules for deployment secrets.
- OIDC federation over long-lived credentials for cloud deploys. See OIDC reference.

### 6. Artifact attestations

Signed build-provenance attestations for anything publishing artifacts (binaries, images, packages):

- `actions/attest-build-provenance` signs with Sigstore-backed SLSA provenance - Build Level 2 by default, Level 3 with reusable workflows.
- Consumers verify with `gh attestation verify`.
- Container images: `actions/attest` with the image digest.

### 7. Script injection prevention

Never interpolate `github.event.*` directly into `run:` blocks. PR titles, issue bodies, branch names, and commit messages are attacker-controlled.

```yaml
# DANGEROUS - attacker controls PR title
- run: echo "PR: ${{ github.event.pull_request.title }}"

# SAFE - pass through env (auto-quoted)
- run: echo "PR: $PR_TITLE"
  env:
    PR_TITLE: ${{ github.event.pull_request.title }}
```

### 8. Caching

Ecosystem-native caching first:

| Stack | Caching |
| --- | --- |
| Python | `actions/setup-python` with `cache: 'pip'` |
| Node | `actions/setup-node` with `cache: 'npm'` (or `pnpm`, `yarn`) |
| Docker | `docker/build-push-action` with `cache-from` / `cache-to` (GHA cache backend) |
| Generic | `actions/cache` with a well-chosen key |

### 9. Timeouts

Set `timeout-minutes` on every job. The default is 360 (6 hours) - silently burns minutes allocation.

---

## Workflow Structure

When creating a new workflow, use this skeleton and adapt:

```yaml
name: <descriptive-name>

on:
  # Choose triggers appropriate to the workflow purpose.
  # See "Trigger Patterns" below.

permissions:
  contents: read

defaults:
  run:
    shell: bash

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true  # false for deploy workflows

jobs:
  <job-name>:
    runs-on: ubuntu-latest  # or see "Runner Selection"
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v6 # TODO: pin to SHA
      # ... remaining steps
```

### Trigger Patterns

Choose triggers based on workflow purpose:

| Purpose | Triggers |
| --- | --- |
| CI (test on every change) | `push:` (branches), `pull_request:` (branches) |
| Deploy to staging | `push:` to `main` / `develop` |
| Deploy to production | `release:` (types: [published]), or manual `workflow_dispatch:` |
| Scheduled tasks | `schedule:` (cron) |
| Manual / parameterised | `workflow_dispatch:` with `inputs:` |
| Reusable (called by others) | `workflow_call:` with `inputs:` and `secrets:` |

For `pull_request`, prefer listing specific `types:` and `paths:` to avoid
unnecessary runs.

### Runner Selection

- Default to `ubuntu-latest` unless there's a reason not to.
- Matrix builds for multi-OS/version testing.
- Self-hosted runners: always a custom label, `runs-on: [self-hosted, <label>]`. Never bare `self-hosted` - security risk if you have multiple pools with different trust levels.

---

## Matrix Builds

```yaml
strategy:
  fail-fast: false  # let all combinations finish
  matrix:
    python-version: ['3.10', '3.11', '3.12']
    os: [ubuntu-latest, windows-latest]
    exclude:
      - os: windows-latest
        python-version: '3.10'
    include:
      - os: ubuntu-latest
        python-version: '3.13'
        experimental: true
```

**Quote version strings that look like floats** (`'3.10'` not `3.10` - YAML parses the latter as `3.1`). Very common mistake.

Use `continue-on-error: ${{ matrix.experimental || false }}` for experimental entries that shouldn't fail the build.

Only include combinations you actually need to cover. Every cell is real runner minutes, so prune the matrix to the versions and platforms whose behaviour genuinely differs rather than filling the grid for completeness.

---

## Reusable Workflows

For sharing logic across repos or reducing duplication:

```yaml
# .github/workflows/reusable-test.yml
name: Reusable Test

on:
  workflow_call:
    inputs:
      python-version:
        required: true
        type: string
    secrets:
      DEPLOY_KEY:
        required: false

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v6 # TODO: pin to SHA
      - uses: actions/setup-python@v6 # TODO: pin to SHA
        with:
          python-version: ${{ inputs.python-version }}
          cache: pip
      - run: pip install -r requirements.txt
      - run: pytest
```

Called via:

```yaml
jobs:
  test:
    uses: org/repo/.github/workflows/reusable-test.yml@main
    with:
      python-version: '3.12'
    secrets: inherit  # or pass individually
```

Key constraints:

- Nesting up to 10 levels deep (raised from 4 in Nov 2025).
- Max 50 reusable workflows per caller (raised from 20 in Nov 2025).
- `env` context doesn't propagate to the called workflow.
- Private-repo reusable workflows are same-repo only unless the repo's Actions settings allow otherwise.

---

## Composite Actions

For reusable steps (smaller than a workflow):

```yaml
# .github/actions/setup-project/action.yml
name: Setup Project
description: Install dependencies and configure environment

inputs:
  python-version:
    description: Python version to use
    required: false
    default: '3.12'

runs:
  using: composite
  steps:
    - uses: actions/setup-python@v6 # TODO: pin to SHA
      with:
        python-version: ${{ inputs.python-version }}
        cache: pip
    - run: pip install -r requirements.txt
      shell: bash
```

Composite actions require `shell:` on every `run:` step - no `defaults.run.shell`.

---

## Custom Actions

### JavaScript Actions

For rich GitHub API interaction or complex logic:

```text
my-action/
├── action.yml
├── src/
│   └── index.js
├── dist/
│   └── index.js      # bundled with ncc
├── package.json
└── README.md
```

The `action.yml` points at the bundled file:

```yaml
name: My Action
description: Does the thing
inputs:
  token:
    description: GitHub token
    required: true
runs:
  using: node20
  main: dist/index.js
```

Bundle with `@vercel/ncc` and commit `dist/` (or use a build-and-release workflow).

### Docker Actions

For tools/runtimes not on the runner, or a fully isolated environment:

```yaml
name: My Docker Action
description: Runs in a container
inputs:
  config:
    description: Path to config file
    required: true
runs:
  using: docker
  image: Dockerfile
```

Docker actions only run on Linux runners.

---

## Self-Hosted Runners

For private network access, GPU, specialised hardware, or cost control:

- Custom labels: `runs-on: [self-hosted, linux, gpu]`.
- Ephemeral runners (recreated per job) strongly preferred - persistent runners accumulate state and credentials across jobs.
- Runner groups with repo access policies to limit which repos use which runners.
- For Kubernetes scaling, point to Actions Runner Controller (ARC).

---

## Common Workflow Recipes

Read `references/recipes.md` for full examples. It covers:

- Python CI (pytest, linting, type checking)
- Docker build and push (to GHCR and Docker Hub)
- Perl CI (multiple Perl versions via `shogo82148/actions-setup-perl`)
- Multi-platform container builds (linux/amd64, linux/arm64)
- Release automation (changelog, GitHub Release, artifact upload)
- Terraform plan/apply with OIDC
- Dependabot auto-merge for minor/patch updates
- Scheduled vulnerability scanning
- Deploy to cloud (AWS, GCP, Azure) via OIDC

---

## Debugging Failing Workflows

1. **Read the error carefully** - most failures are in the message.
2. **Common gotchas:**
   - YAML version strings parsed as floats (`3.10` → `3.1`).
   - Missing `permissions` for the token in use.
   - `${{ }}` in `if:` is always cast to string; use `== 'true'` or `== true` deliberately.
   - `actions/checkout` defaults to shallow clone; some tools need `fetch-depth: 0`.
   - Env vars set in one step aren't available in another unless written to `$GITHUB_ENV`.
   - Secrets unavailable in forked PR workflows (by design).
3. **`ACTIONS_STEP_DEBUG`** for opaque failures: set the repo secret `ACTIONS_STEP_DEBUG` to `true` for verbose logging.
4. **`gh run view --log-failed` can be useless.** On workflows with a fan-in/aggregator job, it may return only that job's log, not the log of the job that actually failed. `gh api repos/<owner>/<repo>/actions/jobs/<job-id>/logs` gets the real per-job log.

---

## CI Traps (Silent Failures)

None of these error. The workflow stays green, or stays plausible, while doing something other than what it says - each was hit and verified in one day's CI work on a fork.

1. **A cache whose restore key never matches its save key freezes forever.** `restore: key: test-durations` against `save: key: test-durations-${{ github.run_id }}` never matches, falls back to prefix search, and GitHub caches are immutable - so every run lands on the *oldest* surviving entry. A month of runs planned their test sharding against one blob created a month earlier, and the symptom looked like health (byte-identical slices) rather than staleness. **Check:** confirm the restore key can actually match a saved key, and log the restored file's age or hash so staleness is visible.

2. **`merge-multiple: true` flattens artefacts that share a filename.** Eight shards each uploading `test_durations.json` produced a "merged" artefact holding one shard's worth, no collision warning. Give each shard's artefact a distinct filename, or download without merging and combine deliberately.

3. **`cancel-in-progress` makes concurrent dispatches eat each other.** `concurrency: { group: x-${{ github.ref }}, cancel-in-progress: true }` means several `workflow_dispatch` runs against the same ref cancel each other. Dispatching eight runs to characterise a 1-in-6 flake returned seven cancellations and one usable result - and a cancelled run isn't a failed run, so the sample looked clean rather than incomplete. **To sample a flake, dispatch serially:** wait for each run to finish before starting the next.

4. **On a fork whose PRs target upstream, `on: pull_request` never fires.** No PR exists *within* the fork, so nothing triggers it. Combined with `push: branches: [main]`, feature branches get no CI at all - and because the run list is simply empty rather than red, nobody notices. Add `push` on the branches you actually develop on, or `workflow_dispatch`, and confirm a run appears before trusting the absence of red.

5. **Upstream repos gate first-time contributors.** The PR's run sits at `conclusion: action_required` awaiting a maintainer's approval, and no check runs attach - `gh pr checks` reports "no checks reported", which reads like a misconfiguration on your side. It is not; nothing on the contributor's side can change it. Read the run's `conclusion` field rather than debugging the workflow file.

6. **Never re-run an existing CI run to gather evidence.** A re-run overwrites that run's recorded conclusion, destroying the historical record you were trying to read (one agent flipped a green run to red this way while building a control). Dispatch a *new* run instead.

---

## Security Checklist

When reviewing or generating a workflow, verify:

- [ ] `permissions:` declared at workflow level (restrictive)
- [ ] Actions pinned by SHA with tag comment
- [ ] No secrets in `if:` conditions or `echo` statements
- [ ] `pull_request_target` used carefully (if at all) - explain the risks
      if the user asks for it
- [ ] Third-party actions are from trusted publishers or audited
- [ ] `timeout-minutes` set on every job
- [ ] Concurrency group set appropriately
- [ ] OIDC preferred over static cloud credentials
- [ ] Self-hosted runner labels are specific, not bare `self-hosted`
- [ ] Production deployments use GitHub Environments with protection rules
      (required reviewers, wait timers, branch/tag constraints)
- [ ] Consider repository rulesets for branch protection over legacy branch
      protection rules (rulesets are more composable and can be org-wide)
- [ ] Untrusted input (`github.event.*`) is never interpolated directly into
      `run:` blocks — always passed through `env:` variables
- [ ] Published artifacts have signed provenance attestations
      (`actions/attest-build-provenance`)
- [ ] Action allowlisting is enabled at org or repo level (if applicable)

---

## Output Format

1. YAML with a `name:` field.
2. Inline comments on non-obvious choices.
3. Suggest a filename for `.github/workflows/` files (lowercase, hyphenated: `ci.yml`, `deploy-prod.yml`).
4. Custom actions: output the full directory structure with all required files.
5. Complex setups: prose explanation first, then YAML.
