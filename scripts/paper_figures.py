"""
Build the article figures from the same cleaned data as scripts/headline_stats.py,
so every number in paper/main.tex and every figure agree.

Usage (from the repository root):
    python scripts/paper_figures.py            # writes paper/figures/fig*.pdf and .png
"""
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(__file__))
from headline_stats import load, wilson, share_table, METRICS  # noqa: E402

OUT = os.path.join("paper", "figures")

# Reference palette (dataviz skill, light mode). Categorical slots in fixed order.
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300"]
BLUE = "#2a78d6"
BLUE_RAMP = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]
INK, INK2, MUTED, GRID, AXIS = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
LABEL_ON_FILL = {"#eda100": INK}  # dark text on yellow, white elsewhere

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": AXIS, "axes.linewidth": 0.8,
    "axes.labelcolor": INK2, "xtick.color": MUTED, "ytick.color": MUTED,
    "xtick.labelcolor": INK2, "ytick.labelcolor": INK2, "axes.titlecolor": INK,
    "axes.titlesize": 10, "axes.titleweight": "bold", "axes.titlelocation": "left",
    "axes.spines.top": False, "axes.spines.right": False, "legend.frameon": False,
    "figure.facecolor": "white", "axes.facecolor": "white", "savefig.dpi": 300,
})


def save(fig, name):
    os.makedirs(OUT, exist_ok=True)
    for ext in ("pdf", "png"):
        fig.savefig(os.path.join(OUT, f"{name}.{ext}"), bbox_inches="tight")
    plt.close(fig)
    print("wrote", name)


def grid(ax, axis="x"):
    ax.grid(axis=axis, color=GRID, linewidth=0.6)
    ax.set_axisbelow(True)


def fig_representation(df):
    """Female first-author share with 95% Wilson CI, by country and by journal (horizontal bars)."""
    overall = 100 * df["female"].mean()
    names = {"International Journal of Greenhouse Gas Control": "Int. J. Greenhouse\nGas Control",
             "International Journal of Hydrogen Energy": "Int. J. Hydrogen\nEnergy",
             "Solar Energy Materials and Solar Cells": "Solar Energy Materials\nand Solar Cells",
             "Applied Catalysis A: General": "Applied Catalysis A"}
    fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.9), gridspec_kw={"wspace": 0.72})
    for ax, by, title in [(axes[0], "Country", "a  By country"), (axes[1], "Publication Title", "b  By journal")]:
        t = share_table(df, by).sort_values("female_pct")
        y = np.arange(len(t))
        ax.barh(y, t["female_pct"], height=0.62, color=BLUE_RAMP[2], zorder=2)
        ax.errorbar(t["female_pct"], y, xerr=[t["female_pct"] - t["ci_low"], t["ci_high"] - t["female_pct"]],
                    fmt="none", ecolor=BLUE_RAMP[5], elinewidth=1.4, capsize=2.5, zorder=3)
        ax.axvline(overall, color=INK2, linestyle="--", linewidth=1, zorder=4)
        for yi, (v, hi, n) in enumerate(zip(t["female_pct"], t["ci_high"], t["n"])):
            ax.text(hi + 0.8, yi, f"{v:.1f}%", va="center", ha="left", fontsize=9.5, color=INK, fontweight="bold")
            ax.text(0.8, yi, f"n = {n:,}", va="center", ha="left", fontsize=7.5, color="white", zorder=5)
        ax.set_yticks(y, [names.get(k, k) for k in t[by]], fontsize=9.5)
        ax.tick_params(axis="y", length=0)
        ax.set_xlim(0, 45)
        ax.set_ylim(-0.6, len(t) - 0.4)
        ax.set_xticks([0, 10, 20, 30, 40])
        ax.set_xlabel("Female first authors (%)", fontsize=9.5)
        ax.set_title(title, fontsize=11, pad=16)
        ax.text(overall, len(t) - 0.32, f"overall {overall:.1f}%", fontsize=8, color=INK2, ha="center", va="bottom")
        ax.spines["left"].set_visible(False)
        grid(ax, "x")
    save(fig, "fig1_representation")


def fig_trend(df):
    """Yearly female share (2010-2024 line, 2025 partial year flagged) above yearly publication counts."""
    g = df.groupby("year")["female"].agg(["sum", "count"])
    g["pct"] = 100 * g["sum"] / g["count"]
    ci = np.array([wilson(s, n) for s, n in zip(g["sum"], g["count"])])
    full, part = g.index <= 2024, g.index == 2025
    fig, (ax, axn) = plt.subplots(2, 1, figsize=(7.2, 3.8), sharex=True,
                                  gridspec_kw={"height_ratios": [2.4, 1], "hspace": 0.15})
    yrs = g.index[full]
    ax.fill_between(yrs, ci[full, 0], ci[full, 1], color=BLUE_RAMP[0], linewidth=0)
    ax.plot(yrs, g["pct"][full], "-o", color=BLUE, linewidth=2, markersize=5, markeredgecolor="white")
    b = np.polyfit(yrs, g["pct"][full], 1)
    ax.plot(yrs, np.polyval(b, yrs), "--", color=INK2, linewidth=1)
    ax.text(2024.3, np.polyval(b, 2024), f"linear trend\n{b[0]:+.2f} pp/yr", fontsize=7.5, color=INK2, va="center")
    ax.errorbar(2025, g["pct"][part].iloc[0], yerr=[[g["pct"][part].iloc[0] - ci[part, 0][0]], [ci[part, 1][0] - g["pct"][part].iloc[0]]],
                fmt="o", mfc="white", mec=BLUE, ecolor=BLUE, markersize=6, linewidth=1)
    ax.annotate("2025: partial year\n(n = %d)" % g["count"][part].iloc[0], (2025, g["pct"][part].iloc[0]),
                xytext=(2021.3, 14), fontsize=7.5, color=INK2, arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.6))
    ax.set_ylabel("Female first\nauthors (%)")
    ax.set_ylim(10, 35)
    ax.set_title("Female first authorship by publication year (shaded: 95% CI)")
    grid(ax, "y")
    axn.bar(g.index, g["count"], color=[BLUE_RAMP[2] if y <= 2024 else BLUE_RAMP[0] for y in g.index], width=0.7)
    axn.set_ylabel("Articles")
    grid(axn, "y")
    axn.set_xticks(g.index, [str(y) if y % 2 == 0 else "" for y in g.index])
    save(fig, "fig2_trend")


def fig_citation_models(R):
    """Female vs male % difference in citations: raw and adjusted model estimates."""
    rows = [("Raw mean ratio (Mann-Whitney p = %.2f)" % R["citations"]["mannwhitney_p"],
             -R["citations"]["pct_more_male"] / (1 + R["citations"]["pct_more_male"] / 100), None)]
    labels = {"M1 gender only": "Log-linear, gender only",
              "M2 + year, journal, country": "+ year, journal, country",
              "M3 + first-author h-index": "+ first-author h-index"}
    for k, v in R["citation_models"].items():
        rows.append((labels[k], v["pct"], v["ci"]))
    fig, ax = plt.subplots(figsize=(6.0, 2.2))
    y = np.arange(len(rows))[::-1]
    for yi, (lab, est, ci) in zip(y, rows):
        if ci:
            ax.hlines(yi, ci[0], ci[1], color=BLUE, linewidth=2)
            ax.plot(est, yi, "o", color=BLUE, markersize=6, markeredgecolor="white")
            txt = f"{est:+.1f}% [{ci[0]:+.1f}, {ci[1]:+.1f}]"
        else:
            ax.plot(est, yi, "D", color="white", markeredgecolor=BLUE, markersize=6)
            txt = f"{est:+.1f}%"
        ax.text(12.5, yi, txt, va="center", fontsize=7.5, color=INK2, clip_on=False)
    ax.axvline(0, color=AXIS, linewidth=1)
    ax.set_yticks(y, [r[0] for r in rows])
    ax.set_xlim(-10, 12)
    ax.set_xlabel("Citations of female- vs male-first-authored papers (% difference)")
    ax.set_title("Citation gap before and after adjustment (bars: 95% CI)")
    grid(ax)
    ax.tick_params(axis="y", length=0)
    ax.spines["left"].set_visible(False)
    save(fig, "fig3_citation_gap")


def fig_journal_mix(df):
    """100% stacked bars: journal mix of each country's articles."""
    order = ["International Journal of Hydrogen Energy", "Solar Energy Materials and Solar Cells", "Solar Energy",
             "Energy Policy", "International Journal of Greenhouse Gas Control", "Applied Catalysis A: General"]
    short = ["Int. J. Hydrogen Energy", "Sol. Energy Mater. Sol. Cells", "Solar Energy", "Energy Policy",
             "Int. J. Greenh. Gas Control", "Appl. Catal. A"]
    jm = (pd.crosstab(df["Country"], df["Publication Title"], normalize="index") * 100)[order]
    jm = jm.sort_values(order[0])
    fig, ax = plt.subplots(figsize=(7.2, 3.3))
    left = np.zeros(len(jm))
    y = np.arange(len(jm))
    for j, (col, lab, colr) in enumerate(zip(order, short, SERIES)):
        v = jm[col].values
        ax.barh(y, v, left=left, color=colr, height=0.7, edgecolor="white", linewidth=1, label=lab)
        for yi, l, w in zip(y, left, v):
            if w >= 8:
                ax.text(l + w / 2, yi, f"{w:.0f}", ha="center", va="center", fontsize=7,
                        color=LABEL_ON_FILL.get(colr, "white"))
        left += v
    ax.set_yticks(y, jm.index)
    ax.set_xlim(0, 100)
    ax.set_xlabel("Share of country's articles (%)")
    ax.set_title("Journal mix by country")
    ax.legend(ncol=3, loc="upper center", bbox_to_anchor=(0.45, -0.2), fontsize=7.5, handlelength=1, columnspacing=1)
    ax.tick_params(axis="y", length=0)
    ax.spines["left"].set_visible(False)
    save(fig, "fig4_journal_mix")


def fig_metric_share(df):
    """Heatmap: each country's share of total citations, usage, captures, mentions, social media."""
    tot = df[METRICS].sum()
    sh = df.groupby("Country")[METRICS].sum() / tot * 100
    sh.insert(0, "Articles", df["Country"].value_counts(normalize=True) * 100)
    sh = sh.sort_values("Articles", ascending=False)
    from matplotlib.colors import LinearSegmentedColormap
    cmap = LinearSegmentedColormap.from_list("blue", ["#ffffff"] + BLUE_RAMP)
    fig, ax = plt.subplots(figsize=(6.4, 3.2))
    im = ax.imshow(sh.values, cmap=cmap, vmin=0, vmax=85, aspect="auto")
    for i in range(sh.shape[0]):
        for j in range(sh.shape[1]):
            v = sh.values[i, j]
            ax.text(j, i, f"{v:.1f}", ha="center", va="center", fontsize=7.5, color="white" if v > 35 else INK)
    ax.set_xticks(range(sh.shape[1]), ["Articles", "Citations", "Usage", "Captures", "Mentions", "Social\nmedia"])
    ax.set_yticks(range(sh.shape[0]), sh.index)
    ax.tick_params(length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_xticks(np.arange(-0.5, sh.shape[1]), minor=True)
    ax.set_yticks(np.arange(-0.5, sh.shape[0]), minor=True)
    ax.grid(which="minor", color="white", linewidth=2)
    ax.tick_params(which="minor", length=0)
    ax.set_title("Country share of articles and impact metrics (% of column total)")
    cb = fig.colorbar(im, ax=ax, fraction=0.04, pad=0.02)
    cb.outline.set_visible(False)
    cb.ax.tick_params(labelsize=7, color=MUTED)
    save(fig, "fig5_metric_share")


def fig_threshold(df):
    """Female share among first authors retained at each minimum Namsor confidence."""
    conf = "Gender likelihood (First Author)"
    ts = [0.5, 0.6, 0.7, 0.8, 0.9]
    rows = []
    for t in ts:
        s = df[df[conf] >= t]
        lo, hi = wilson(s["female"].sum(), len(s))
        rows.append((t, 100 * s["female"].mean(), lo, hi, len(s)))
    r = pd.DataFrame(rows, columns=["t", "pct", "lo", "hi", "n"])
    fig, ax = plt.subplots(figsize=(4.8, 2.8))
    ax.fill_between(r["t"], r["lo"], r["hi"], color=BLUE_RAMP[0], linewidth=0)
    ax.plot(r["t"], r["pct"], "-o", color=BLUE, linewidth=2, markersize=6, markeredgecolor="white")
    for _, x in r.iterrows():
        ax.text(x["t"], x["pct"] + 1.6, f"{x['pct']:.1f}%\nn={int(x['n']):,}", ha="center", fontsize=7, color=INK2)
    ax.set_xticks(ts, ["none", "0.6", "0.7", "0.8", "0.9"])
    ax.set_ylim(0, 33)
    ax.set_xlabel("Minimum Namsor confidence for first-author gender")
    ax.set_ylabel("Female first authors (%)")
    ax.set_title("Sensitivity to the classification threshold")
    grid(ax, "y")
    save(fig, "fig6_threshold")


def fig_seniority(df):
    """Female first-author share by h-index band (unique articles) and by number of first-author articles (unique authors)."""
    art = df.drop_duplicates("Item DOI")
    overall = 100 * art["female"].mean()
    labels = ["0-2", "3-5", "6-10", "11-20", "21-40", "41+"]
    band = pd.cut(art["First Author H-Index"], bins=[-1, 2, 5, 10, 20, 40, 1000], labels=labels)
    a = art.groupby(band)["female"].agg(["sum", "count"])
    per = art.groupby("First Author").agg(n=("Item DOI", "nunique"), female=("female", "first"))
    grp = pd.cut(per["n"], bins=[0, 1, 4, 1000], labels=["1", "2-4", "5+"])
    b = per.groupby(grp)["female"].agg(["sum", "count"])
    fig, axes = plt.subplots(1, 2, figsize=(7.4, 2.9), gridspec_kw={"width_ratios": [2, 1], "wspace": 0.28})
    for ax, t, title, xlabel in [(axes[0], a, "a  By first-author h-index", "First-author h-index"),
                                 (axes[1], b, "b  By articles per author", "First-author articles in the dataset")]:
        pct = 100 * t["sum"] / t["count"]
        ci = np.array([wilson(s, n) for s, n in zip(t["sum"], t["count"])])
        x = np.arange(len(t))
        ax.errorbar(x, pct, yerr=[pct - ci[:, 0], ci[:, 1] - pct], fmt="o", color=BLUE, ecolor=BLUE,
                    elinewidth=2, markersize=6, markeredgecolor="white")
        ax.axhline(overall, color=MUTED, linestyle="--", linewidth=1)
        for xi, p, hi, n in zip(x, pct, ci[:, 1], t["count"]):
            ax.text(xi, hi + 1.2, f"{p:.1f}%\nn={int(n):,}", ha="center", fontsize=7, color=INK2)
        ax.set_xticks(x, list(t.index))
        ax.set_xlim(-0.6, len(t) - 0.4)
        ax.set_ylim(0, 42)
        ax.set_xlabel(xlabel)
        ax.set_title(title)
        grid(ax, "y")
    axes[0].set_ylabel("Female first authors (%)")
    axes[0].text(-0.55, overall - 1.0, f"overall {overall:.1f}%", fontsize=7, color=INK2, ha="left", va="top")
    save(fig, "fig7_seniority")


def main():
    _, df = load("processed_data")
    with open(os.path.join("results", "headline_stats.json"), encoding="utf-8") as fh:
        R = json.load(fh)
    fig_representation(df)
    fig_trend(df)
    fig_citation_models(R)
    fig_journal_mix(df)
    fig_metric_share(df)
    fig_threshold(df)
    fig_seniority(df)


if __name__ == "__main__":
    main()
