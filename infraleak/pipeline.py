"""Dataset pipeline: generate -> run -> label (oracle) -> freeze -> split -> views -> release -> eval."""
from __future__ import annotations
import hashlib
import json
from collections import Counter
from pathlib import Path

from .oracle import label_episode, ORACLE_VERSION
from .runner import run_episode, load_episode
from .splits import assign_split, check_splits, SPLITS
from .views import load_profiles, apply_view

EVAL_SPLITS = [s for s in SPLITS if s.startswith("test")] + ["val"]


def sha256_file(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def generate(specs, data: Path, brain, resume=True, log_every=200):
    raw = data / "raw"
    n = 0
    for spec in specs:
        if resume and (raw / spec.episode_id / "run_meta.json").exists():
            continue
        run_episode(spec, raw, brain)
        n += 1
        if log_every and n % log_every == 0:
            print(f"  ran {n} episodes")
    return n


def episode_ids(data: Path):
    return sorted(p.name for p in (data / "raw").iterdir() if (p / "events.jsonl").exists())


def label_all(data: Path):
    labels = []
    for eid in episode_ids(data):
        spec, events = load_episode(data / "raw", eid)
        L = label_episode(spec, events)
        L["split"] = assign_split(L)
        labels.append(L)
    out = data / "labels"
    out.mkdir(parents=True, exist_ok=True)
    with open(out / "labels.jsonl", "w") as f:
        for L in labels:
            f.write(json.dumps(L, sort_keys=True) + "\n")
    return labels


def freeze(data: Path):
    """Write MANIFEST.json: hashes of every raw log + the label file. Done BEFORE any detector runs."""
    files = {f"raw/{eid}/events.jsonl": sha256_file(data / "raw" / eid / "events.jsonl") for eid in episode_ids(data)}
    man = {"oracle_version": ORACLE_VERSION, "labels_sha256": sha256_file(data / "labels" / "labels.jsonl"),
           "n_episodes": len(files), "raw_sha256": files}
    (data / "labels" / "MANIFEST.json").write_text(json.dumps(man, indent=1, sort_keys=True))
    return man


def verify(data: Path):
    """Re-hash everything and re-run the oracle; any drift or tampering raises."""
    man = json.loads((data / "labels" / "MANIFEST.json").read_text())
    if sha256_file(data / "labels" / "labels.jsonl") != man["labels_sha256"]:
        raise AssertionError("labels.jsonl changed since freeze")
    for rel, h in man["raw_sha256"].items():
        if sha256_file(data / rel) != h:
            raise AssertionError(f"{rel} changed since freeze")
    stored = {L["episode_id"]: L for L in load_labels(data)}
    for eid in stored:
        spec, events = load_episode(data / "raw", eid)
        L = label_episode(spec, events)
        if L["label"] != stored[eid]["label"] or L["flow_class"] != stored[eid]["flow_class"]:
            raise AssertionError(f"oracle not reproducible for {eid}")
    return True


def load_labels(data: Path):
    return [json.loads(l) for l in (data / "labels" / "labels.jsonl").read_text().splitlines() if l]


def load_specs(data: Path, ids):
    from .schema import ScenarioSpec
    return {i: ScenarioSpec.from_dict(json.loads((data / "raw" / i / "spec.json").read_text())) for i in ids}


def build_views(data: Path, labels, profiles=None):
    profiles = profiles or load_profiles()
    views = {p: {} for p in profiles}
    for L in labels:
        _, events = load_episode(data / "raw", L["episode_id"])
        for p, cfg in profiles.items():
            views[p][L["episode_id"]] = apply_view(events, p, cfg)
    return views


def write_release(data: Path, labels, views):
    """Release layout. Train/val: views + labels. Test splits: views only; labels sealed separately."""
    rel, sealed = data / "release", data / "sealed"
    by_split = {}
    for L in labels:
        by_split.setdefault(L["split"], []).append(L)
    for split, Ls in by_split.items():
        d = rel / split
        d.mkdir(parents=True, exist_ok=True)
        for prof, vs in views.items():
            with open(d / f"view_{prof}.jsonl", "w") as f:
                for L in Ls:
                    f.write(json.dumps({"episode_id": L["episode_id"], "events": vs[L["episode_id"]]}) + "\n")
        public = [{k: L[k] for k in ("episode_id", "label", "flow_class", "event_stage", "domain", "channel",
                                     "design")} for L in Ls]
        target = d if split in ("train", "val") else sealed / split
        target.mkdir(parents=True, exist_ok=True)
        with open(target / "labels.jsonl", "w") as f:
            for row in public:
                f.write(json.dumps(row) + "\n")


def dataset_card(labels, split_stats, data: Path, profiles):
    c = Counter((L["design"], L["flow_class"]) for L in labels)
    lines = ["# Dataset card (auto-generated)\n", f"Episodes: {len(labels)}  ",
             f"Positives (oracle transfer): {sum(L['label'] for L in labels)}  ",
             f"Oracle version: {labels[0]['oracle_version'] if labels else '-'}\n",
             "## Splits\n", "| split | episodes | positives | flow classes |", "|---|---|---|---|"]
    for s, st in split_stats.items():
        lines.append(f"| {s} | {st['n']} | {st['pos']} | {st['by_class']} |")
    lines += ["\n## Design vs oracle label\n", "| design | oracle flow class | episodes |", "|---|---|---|"]
    for (d, fc), n in sorted(c.items()):
        lines.append(f"| {d} | {fc} | {n} |")
    lines += ["\n## Stage counts\n"]
    for st in ("exposure", "access", "transfer"):
        lines.append(f"- {st}: {sum(L['stages'][st] for L in labels)}")
    lines += ["\n## Observer profiles\n", "| profile | layers | content | actors | ops | drop | note |",
              "|---|---|---|---|---|---|---|"]
    for p, cfg in profiles.items():
        lines.append(f"| {p} | {','.join(cfg['layers'])} | {cfg['content']} | {','.join(cfg['actors'])} | "
                     f"{cfg['ops'] if cfg['ops'] == 'all' else ','.join(cfg['ops'])} | {cfg['drop']} | {cfg['note']} |")
    (data / "DATASET_CARD.md").write_text("\n".join(lines) + "\n")
