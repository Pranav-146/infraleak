"""Evaluation: every (split x observer profile x detector) cell, episode-level, with Wilson 95% CIs."""
from __future__ import annotations
import csv
import math
from collections import defaultdict


def wilson(k, n, z=1.96):
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def score(rows):
    tp = sum(1 for y, a, _ in rows if y and a)
    fp = sum(1 for y, a, _ in rows if not y and a)
    fn = sum(1 for y, a, _ in rows if y and not a)
    tn = sum(1 for y, a, _ in rows if not y and not a)
    P = tp / (tp + fp) if tp + fp else 0.0
    R = tp / (tp + fn) if tp + fn else float("nan")
    F = 2 * P * R / (P + R) if P + R and not math.isnan(R) else 0.0
    fpr = fp / (fp + tn) if fp + tn else float("nan")
    r_lo, r_hi = wilson(tp, tp + fn)
    f_lo, f_hi = wilson(fp, fp + tn)
    by_class = defaultdict(lambda: [0, 0])
    by_design = defaultdict(lambda: [0, 0])
    for y, a, L in rows:
        if y:
            by_class[L["flow_class"]][0] += a
            by_class[L["flow_class"]][1] += 1
        by_design[L["design"]][0] += a
        by_design[L["design"]][1] += 1
    return dict(tp=tp, fp=fp, fn=fn, tn=tn, precision=P, recall=R, f1=F, fpr=fpr,
                recall_ci=(r_lo, r_hi), fpr_ci=(f_lo, f_hi),
                recall_by_class={k: v[0] / v[1] for k, v in by_class.items()},
                alarm_rate_by_design={k: v[0] / v[1] for k, v in by_design.items()})


def evaluate(labels, views_by_profile, detectors, splits):
    """views_by_profile[profile][episode_id] -> list of view events."""
    results = []
    for split in splits:
        Ls = [L for L in labels if L["split"] == split]
        if not Ls:
            continue
        for prof, views in views_by_profile.items():
            for det in detectors:
                rows = [(L["label"], det(views[L["episode_id"]])[0], L) for L in Ls]
                results.append(dict(split=split, profile=prof, detector=det.name, n=len(Ls),
                                    pos=sum(L["label"] for L in Ls), **score(rows)))
    return results


def write_results(results, out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    cols = ["split", "profile", "detector", "n", "pos", "tp", "fp", "fn", "tn", "precision", "recall", "f1", "fpr"]
    with open(out_dir / "metrics.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(cols + ["recall_lo", "recall_hi", "fpr_lo", "fpr_hi", "recall_by_class", "alarm_rate_by_design"])
        for r in results:
            w.writerow([r[c] if not isinstance(r[c], float) else round(r[c], 4) for c in cols]
                       + [round(x, 4) for x in r["recall_ci"] + r["fpr_ci"]]
                       + [r["recall_by_class"], {k: round(v, 3) for k, v in r["alarm_rate_by_design"].items()}])
    lines = ["# Baseline results (episode level)\n",
             "Recall/FPR with Wilson 95% CI. Detectors only ever see the observer view, never labels.\n"]
    for split in dict.fromkeys(r["split"] for r in results):
        rs = [r for r in results if r["split"] == split]
        lines.append(f"\n## {split}  (n={rs[0]['n']}, positives={rs[0]['pos']})\n")
        lines.append("| profile | detector | precision | recall [95% CI] | FPR [95% CI] | F1 | recall by class |")
        lines.append("|---|---|---|---|---|---|---|")
        for r in rs:
            rc = ", ".join(f"{k[:4]} {v:.2f}" for k, v in sorted(r["recall_by_class"].items()))
            lines.append(f"| {r['profile']} | {r['detector']} | {r['precision']:.2f} | {r['recall']:.2f} "
                         f"[{r['recall_ci'][0]:.2f}-{r['recall_ci'][1]:.2f}] | {r['fpr']:.2f} "
                         f"[{r['fpr_ci'][0]:.2f}-{r['fpr_ci'][1]:.2f}] | {r['f1']:.2f} | {rc} |")
    (out_dir / "summary.md").write_text("\n".join(lines) + "\n")
