"""Figures from results/metrics.csv: the degradation curve(s) for the review.

degradation.png/.svg      best baseline informedness (recall - FPR) at each observer view, one line per test split.
                          0 = no better than chance or "alarm on everything"; F1 is NOT used for the headline
                          because always-alarm already scores F1 = 2p/(1+p) (0.67 at 50% positives).
recall_fpr.png/.svg       recall (top) and false-positive rate (bottom) per detector, per split
"""
from __future__ import annotations
import csv
from pathlib import Path

# Ordered from most to least visibility (left to right). Missing profiles are skipped.
VIEW_ORDER = ["app_full", "b_only", "app_sinks", "app_hash", "app_meta", "host_meta", "service_meta",
              "app_meta_drop50", "reply_only"]
VIEW_LABEL = {"app_full": "app\nfull", "b_only": "B only", "app_sinks": "outputs\nonly", "app_hash": "hashed",
              "app_meta": "metadata", "host_meta": "host\nsyscalls", "service_meta": "DB/git\nlog",
              "app_meta_drop50": "metadata\n50% loss", "reply_only": "reply\nonly"}
SPLITS = [("test_id", "held-out seeds"), ("test_ood_domain", "unseen domain"),
          ("test_ood_channel", "unseen channel"), ("test_ood_class", "unseen flow class")]
DETECTORS = [("reply_dlp", "pattern DLP"), ("meta_read_alarm", "cross-agent read alarm"),
             ("provenance", "token provenance")]
# reference categorical palette, slots 1-4 (validated: adjacent CVD dE >= 9.1); markers give secondary encoding
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100"]
MARKERS = ["o", "s", "D", "^"]
SURFACE, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"


def _load(results_dir: Path):
    rows = list(csv.DictReader(open(results_dir / "metrics.csv")))
    for r in rows:
        for k in ("recall", "fpr", "f1", "precision"):
            r[k] = float(r[k]) if r[k] not in ("", "nan") else float("nan")
    return rows


def _style(plt):
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.edgecolor": INK2,
                         "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
                         "axes.facecolor": SURFACE, "figure.facecolor": SURFACE, "axes.spines.top": False,
                         "axes.spines.right": False, "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.8,
                         "axes.axisbelow": True, "legend.frameon": False})


def make_figures(results_dir: Path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    _style(plt)
    results_dir = Path(results_dir)
    rows = _load(results_dir)
    present = {r["profile"] for r in rows}
    views = [v for v in VIEW_ORDER if v in present]
    splits = [(s, n) for s, n in SPLITS if any(r["split"] == s for r in rows)]
    get = {(r["split"], r["profile"], r["detector"]): r for r in rows}
    out = results_dir / "figures"
    out.mkdir(exist_ok=True)
    x = list(range(len(views)))

    # 1) headline degradation curve
    fig, ax = plt.subplots(figsize=(11, 4.6))
    ends = []
    for i, (s, name) in enumerate(splits):
        ys = [max(get[(s, v, d)]["recall"] - get[(s, v, d)]["fpr"] for d, _ in DETECTORS if (s, v, d) in get)
              for v in views]
        ax.plot(x, ys, color=SERIES[i], lw=2, marker=MARKERS[i], ms=7, mec=SURFACE, mew=1.5, label=name)
        ends.append([ys[-1], name])
    # direct labels at line ends, nudged apart so they never overlap
    ends.sort()
    for k in range(1, len(ends)):
        ends[k][0] = max(ends[k][0], ends[k - 1][0] + 0.055)
    for yv, name in ends:
        ax.annotate(name, (x[-1], yv), xytext=(10, 0), textcoords="offset points", va="center", color=INK2,
                    fontsize=9)
    ax.axhline(0, color=INK2, lw=1)
    ax.text(x[0], 0.03, "chance / alarm-on-everything", color=INK2, fontsize=8.5)
    ax.set_xticks(x, [VIEW_LABEL[v] for v in views])
    ax.set_ylim(-0.08, 1.03)
    ax.set_xlim(-0.3, len(views) - 0.3 + 1.3)
    ax.set_ylabel("best baseline: recall − false-positive rate")
    ax.set_title("Detection above chance collapses as the observer sees less  (oracle = 1.0 on every view)",
                 loc="left", color=INK, fontsize=12)
    ax.text(0, -0.30, "more visibility  →  less visibility", transform=ax.transAxes, color=INK2, fontsize=9)
    ax.legend(loc="upper right", ncol=4, fontsize=9, bbox_to_anchor=(1, 1.0))
    fig.tight_layout()
    for ext in ("png", "svg"):
        fig.savefig(out / f"degradation.{ext}", dpi=200)
    plt.close(fig)

    # 2) recall / FPR small multiples
    fig, axes = plt.subplots(2, len(splits), figsize=(4.1 * len(splits), 7.0), sharex=True, sharey=True)
    if len(splits) == 1:
        axes = [[axes[0]], [axes[1]]]
    for j, (s, name) in enumerate(splits):
        for row, metric in enumerate(("recall", "fpr")):
            ax = axes[row][j]
            for i, (d, dn) in enumerate(DETECTORS):
                ys = [get[(s, v, d)][metric] if (s, v, d) in get else float("nan") for v in views]
                ax.plot(x, ys, color=SERIES[i], lw=2, marker=MARKERS[i], ms=6, mec=SURFACE, mew=1.2, label=dn)
            ax.set_ylim(-0.05, 1.05)
            if row == 0:
                n = next(r for r in rows if r["split"] == s)
                ax.set_title(f"{name}\n(n={n['n']}, {n['pos']} leaks)", fontsize=10, color=INK, loc="left")
            if j == 0:
                ax.set_ylabel("recall  (higher better)" if row == 0 else "false-positive rate  (lower better)")
            ax.set_xticks(x, [VIEW_LABEL[v].replace("\n", " ") for v in views], fontsize=8, rotation=55,
                          ha="right", rotation_mode="anchor")
    h, l = axes[0][0].get_legend_handles_labels()
    fig.legend(h, l, loc="upper center", ncol=3, fontsize=10, bbox_to_anchor=(0.5, 1.0))
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    for ext in ("png", "svg"):
        fig.savefig(out / f"recall_fpr.{ext}", dpi=200)
    plt.close(fig)
    return sorted(str(p) for p in out.iterdir())
