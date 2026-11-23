#!/usr/bin/env python3
"""brief_fig.py -- helpers for Owner Decision Brief figures (decision-brief skill).

    import sys; sys.path.insert(0, "<skill>/scripts"); import brief_fig as bf
    fig, ax = bf.sheet("Brief X - <question>")          # 2 x 3, one panel per check
    bf.force(ax[0, 0], (50, 0), (0, -40), 10.3, "gas load")   # arrow + "2.32 lbf (10.3 N)"
    bf.moment(ax[0, 0], (120, 0), 16.1e-3, "servo")   # curved arrow, "0.142 lbf-in (0.0161 N-m)"
    bf.margins(ax[0, 2], ["flap", "boss"], [2.5, 1.1], limit=2.0, unit="mm", limit_label="SLS rule")
    bf.save(fig, "docs/figures/brief_x_six_checks.png")       # stamps the review notice

Run directly for a demo sheet:  python3 brief_fig.py demo.png

License: MIT -- see LICENSES/MIT (SPDX-License-Identifier: MIT)
AI note: written by Claude (Anthropic) for the decision-brief skill, 2026-11-23.
"""

from __future__ import annotations

import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyArrowPatch  # noqa: E402

N_PER_LBF = 4.448222
MM_PER_IN = 25.4
NM_PER_LBFIN = 0.112985
CHECKS = (
    "1  Statics and dynamics",
    "2  Function",
    "3  Structural integrity",
    "4  Mechanism and component interactions",
    "5  Weight and balance",
    "6  Canonical shape",
)
STAMP = "Analytical, unreviewed - ENGINEERING REVIEW REQUIRED"


def lbf(newton: float) -> str:
    """'2.32 lbf (10.3 N)' -- imperial first, metric in parentheses."""
    return f"{newton / N_PER_LBF:.3g} lbf ({newton:.3g} N)"


def lbf_in(newton_m: float) -> str:
    return f"{newton_m / NM_PER_LBFIN:.3g} lbf-in ({newton_m:.3g} N-m)"


def inch(mm: float) -> str:
    return f"{mm / MM_PER_IN:.3f} in ({mm:.2f} mm)"


def sheet(title: str, checks=CHECKS, figsize=(19, 11.5)):
    """2 x 3 sheet, one panel per check, titled; returns (fig, ax)."""
    fig, ax = plt.subplots(2, 3, figsize=figsize)
    for a, t in zip(ax.flat, checks):
        a.set_title(t, loc="left", fontsize=10, fontweight="bold")
    fig.suptitle(f"{title}.  {STAMP}", fontsize=12)
    return fig, ax


def force(ax, tail, vec, newton: float, label: str = "", color="#c0392b", lw=2.0):
    """Arrow from `tail` along `vec` (plot units), labelled with its magnitude."""
    x, y = tail
    ax.add_patch(FancyArrowPatch((x, y), (x + vec[0], y + vec[1]), arrowstyle="-|>",
                                 mutation_scale=14, color=color, lw=lw))
    ax.annotate(f"{label} {lbf(newton)}".strip(), (x + vec[0], y + vec[1]), fontsize=8,
                color=color, xytext=(4, 4), textcoords="offset points")


def moment(ax, centre, newton_m: float, label: str = "", r=8.0, color="#8e44ad", ccw=True):
    """Curved arrow about `centre`, labelled with the moment."""
    x, y = centre
    a = FancyArrowPatch((x + r, y), (x, y + r), connectionstyle=f"arc3,rad={0.5 if ccw else -0.5}",
                        arrowstyle="-|>", mutation_scale=12, color=color, lw=1.6)
    ax.add_patch(a)
    ax.annotate(f"{label} {lbf_in(newton_m)}".strip(), (x + r, y + r), fontsize=8, color=color)


def margins(ax, labels, values, limit: float, unit="mm", limit_label="limit", higher_is_ok=True):
    """Horizontal bars against a limit line; red where the value fails the limit."""
    ok = [(v >= limit) if higher_is_ok else (v <= limit) for v in values]
    ax.barh(range(len(values)), values, color=["#3a9a5a" if o else "#d03030" for o in ok])
    ax.axvline(limit, color="k", ls="--")
    ax.text(limit, len(values) - 0.4, f" {limit_label} {limit:g} {unit}", fontsize=8)
    ax.set_yticks(range(len(values)), labels, fontsize=8.5)
    for i, v in enumerate(values):
        ax.text(v, i, f" {v:g} {unit}", va="center", fontsize=8)


def not_applicable(ax, reason: str):
    """A check that does not apply still gets its panel and its one-line reason."""
    ax.axis("off")
    ax.text(0.02, 0.6, "Does not apply:\n" + reason, fontsize=10, va="top", wrap=True)


def save(fig, path, dpi=90):
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    fig.savefig(path, dpi=dpi)
    plt.close(fig)
    return path


def _demo(out):
    fig, ax = sheet("Demo brief - flap hinge options")
    a = ax[0, 0]
    a.plot([0, 100], [0, 0], "k-", lw=5, alpha=0.3)
    force(a, (80, 30), (0, -28), 10.3, "gas")
    force(a, (10, -30), (0, 28), 6.0, "R1")
    moment(a, (50, 0), 0.0161, "servo")
    a.set_xlim(-5, 120)
    a.set_ylim(-40, 45)
    margins(ax[0, 2], ["flap", "boss (as drawn)", "boss dia 6"], [2.5, 1.1, 2.0], 2.0,
            limit_label="SLS rule")
    not_applicable(ax[1, 2], "internal parts only; the outer mould line is unchanged.")
    for a in (ax[0, 1], ax[1, 0], ax[1, 1]):
        a.text(0.5, 0.5, "(picture for this check)", ha="center", transform=a.transAxes)
    save(fig, out)


if __name__ == "__main__":
    _demo(sys.argv[1] if len(sys.argv) > 1 else "brief_fig_demo.png")
