# Workflow Recipes

Concrete, copy-adaptable workflow examples. Each recipe follows the
security and structure conventions from the main SKILL.md.

**Note on SHA pinning:** These recipes use version tags for readability.
When generating workflows for a user, look up the current SHA from the
action's GitHub releases page if you have web search. If you don't,
use the tag with a `# TODO: pin to SHA` comment.

## Table of Contents

1. [Python CI](#python-ci)
2. [Docker Build and Push to GHCR](#docker-build-and-push-to-ghcr)
3. [Perl CI](#perl-ci)
4. [Multi-Platform Container Build](#multi-platform-container-build)
5. [Release Automation](#release-automation)
6. [OIDC Cloud Deploy (AWS)](#oidc-cloud-deploy-aws)
7. [OIDC Cloud Deploy (GCP)](#oidc-cloud-deploy-gcp)
8. [OIDC Cloud Deploy (Azure)](#oidc-cloud-deploy-azure)
9. [Dependabot Auto-Merge](#dependabot-auto-merge)
10. [Scheduled Vulnerability Scan](#scheduled-vulnerability-scan)
11. [Terraform Plan/Apply](#terraform-planapply)
12. [Generic Node/TypeScript CI](#generic-nodetypescript-ci)

---

## Python CI

```yaml
name: Python CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: read

defaults:
  run:
    shell: bash

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    strategy:
      fail-fast: false
      matrix:
        python-version: ['3.11', '3.12', '3.13']
    steps:
      - uses: actions/checkout@v6 # TODO: pin to SHA

      - uses: actions/setup-python@v6 # TODO: pin to SHA
        with:
          python-version: ${{ matrix.python-version }}
          cache: pip

      - run: pip install -r requirements.txt -r requirements-dev.txt

      - name: Lint
        run: ruff check .

      - name: Format check
        run: ruff format --check .

      - name: Type check
        run: mypy src/

      - name: Test
        run: pytest --tb=short -q
```

Adapt: swap `ruff` for `flake8`/`black` if the project uses those.
Add `--cov` and coverage upload if wanted.

---

## Docker Build and Push to GHCR

```yaml
name: Docker Build

on:
  push:
    branches: [main]
    tags: ['v*']
  pull_request:
    branches: [main]

permissions:
  contents: read
  packages: write

defaults:
  run:
    shell: bash

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  build:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    steps:
      - uses: actions/checkout@v6 # TODO: pin to SHA

      - uses: docker/setup-buildx-action@v4 # TODO: pin to SHA

      - uses: docker/login-action@v4 # TODO: pin to SHA
        if: github.event_name != 'pull_request'
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - uses: docker/metadata-action@v6 # TODO: pin to SHA
        id: meta
        with:
          images: ghcr.io/${{ github.repository }}
          tags: |
            type=ref,event=branch
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha

      - uses: docker/build-push-action@v7 # TODO: pin to SHA
        with:
          context: .
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

---

## Perl CI

```yaml
name: Perl CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: read

defaults:
  run:
    shell: bash

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 20
    strategy:
      fail-fast: false
      matrix:
        perl-version: ['5.38', '5.40']
    steps:
      - uses: actions/checkout@v6 # TODO: pin to SHA

      - uses: shogo82148/actions-setup-perl@v1 # TODO: pin to SHA
        with:
          perl-version: ${{ matrix.perl-version }}

      - name: Install dependencies
        run: cpanm --installdeps --notest .

      - name: Run tests
        run: prove -lr t/

      - name: Perl critic (optional)
        run: |
          cpanm --notest Perl::Critic
          perlcritic --severity 4 lib/
        continue-on-error: true
```

Adapt: use `--with-develop` on `cpanm` for author tests. Add
`Devel::Cover` for coverage if wanted.

---

## Multi-Platform Container Build

```yaml
name: Multi-Platform Build

on:
  push:
    tags: ['v*']

permissions:
  contents: read
  packages: write

jobs:
  build:
    runs-on: ubuntu-latest
    timeout-minutes: 45
    steps:
      - uses: actions/checkout@v6 # TODO: pin to SHA

      - uses: docker/setup-qemu-action@v4 # TODO: pin to SHA

      - uses: docker/setup-buildx-action@v4 # TODO: pin to SHA

      - uses: docker/login-action@v4 # TODO: pin to SHA
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - uses: docker/metadata-action@v6 # TODO: pin to SHA
        id: meta
        with:
          images: ghcr.io/${{ github.repository }}

      - uses: docker/build-push-action@v7 # TODO: pin to SHA
        with:
          context: .
          platforms: linux/amd64,linux/arm64
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

---

## Release Automation

```yaml
name: Release

on:
  push:
    tags: ['v*']

permissions:
  contents: write

defaults:
  run:
    shell: bash

jobs:
  release:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v6 # TODO: pin to SHA
        with:
          fetch-depth: 0  # needed for changelog generation

      - name: Generate changelog
        id: changelog
        run: |
          # Get commits since last tag
          PREV_TAG=$(git describe --tags --abbrev=0 HEAD^ 2>/dev/null || echo "")
          if [ -n "$PREV_TAG" ]; then
            CHANGES=$(git log "${PREV_TAG}..HEAD" --pretty=format:"- %s (%h)" --no-merges)
          else
            CHANGES=$(git log --pretty=format:"- %s (%h)" --no-merges)
          fi
          {
            echo "changelog<<EOF"
            echo "$CHANGES"
            echo "EOF"
          } >> "$GITHUB_OUTPUT"

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v2 # TODO: pin to SHA
        with:
          body: ${{ steps.changelog.outputs.changelog }}
          generate_release_notes: true
```

---

## OIDC Cloud Deploy (AWS)

```yaml
name: Deploy to AWS

on:
  push:
    branches: [main]

permissions:
  contents: read
  id-token: write  # required for OIDC

defaults:
  run:
    shell: bash

concurrency:
  group: deploy-aws
  cancel-in-progress: false  # never cancel deployments

jobs:
  deploy:
    runs-on: ubuntu-latest
    timeout-minutes: 20
    environment: production  # protection rules apply
    steps:
      - uses: actions/checkout@v6 # TODO: pin to SHA

      - uses: aws-actions/configure-aws-credentials@v4 # TODO: pin to SHA
        with:
          role-to-assume: arn:aws:iam::123456789012:role/github-actions
          aws-region: eu-west-1

      # ... deployment steps
```

Requires: AWS IAM OIDC identity provider configured with
`token.actions.githubusercontent.com` as the provider URL.

---

## OIDC Cloud Deploy (GCP)

```yaml
      - uses: google-github-actions/auth@v2 # TODO: pin to SHA
        with:
          workload_identity_provider: projects/123456/locations/global/workloadIdentityPools/github/providers/github-actions
          service_account: deploy@project-id.iam.gserviceaccount.com
```

Requires: GCP Workload Identity Federation configured.

---

## OIDC Cloud Deploy (Azure)

```yaml
      - uses: azure/login@v2 # TODO: pin to SHA
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
```

Requires: Azure AD federated credential configured for the repo.

---

## Dependabot Auto-Merge

```yaml
name: Dependabot Auto-Merge

on:
  pull_request:

permissions:
  contents: write
  pull-requests: write

jobs:
  auto-merge:
    runs-on: ubuntu-latest
    timeout-minutes: 5
    if: github.actor == 'dependabot[bot]'
    steps:
      - uses: dependabot/fetch-metadata@v2 # TODO: pin to SHA
        id: metadata

      - name: Auto-merge minor and patch updates
        if: >-
          steps.metadata.outputs.update-type == 'version-update:semver-minor' ||
          steps.metadata.outputs.update-type == 'version-update:semver-patch'
        run: gh pr merge --auto --squash "$PR_URL"
        env:
          PR_URL: ${{ github.event.pull_request.html_url }}
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

---

## Scheduled Vulnerability Scan

```yaml
name: Security Scan

on:
  schedule:
    - cron: '30 6 * * 1'  # Monday 06:30 UTC
  workflow_dispatch:

permissions:
  contents: read
  security-events: write

jobs:
  codeql:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    steps:
      - uses: actions/checkout@v6 # TODO: pin to SHA

      - uses: github/codeql-action/init@v3 # TODO: pin to SHA
        with:
          languages: python  # adapt to your stack

      - uses: github/codeql-action/analyze@v3 # TODO: pin to SHA
```

---

## Terraform Plan/Apply

```yaml
name: Terraform

on:
  push:
    branches: [main]
    paths: ['infra/**']
  pull_request:
    branches: [main]
    paths: ['infra/**']

permissions:
  contents: read
  id-token: write
  pull-requests: write

defaults:
  run:
    shell: bash
    working-directory: infra

concurrency:
  group: terraform-${{ github.ref }}
  cancel-in-progress: false

jobs:
  plan:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v6 # TODO: pin to SHA

      - uses: hashicorp/setup-terraform@v3 # TODO: pin to SHA

      # Add OIDC auth step for your cloud provider here

      - run: terraform init

      - run: terraform plan -out=tfplan
        if: github.event_name == 'pull_request'

      - run: terraform apply -auto-approve
        if: github.ref == 'refs/heads/main' && github.event_name == 'push'
```

---

## Generic Node/TypeScript CI

```yaml
name: Node CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: read

defaults:
  run:
    shell: bash

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    strategy:
      fail-fast: false
      matrix:
        node-version: ['20', '22']
    steps:
      - uses: actions/checkout@v6 # TODO: pin to SHA

      - uses: actions/setup-node@v4 # TODO: pin to SHA
        with:
          node-version: ${{ matrix.node-version }}
          cache: npm

      - run: npm ci

      - name: Lint
        run: npm run lint

      - name: Type check
        run: npx tsc --noEmit

      - name: Test
        run: npm test
```
