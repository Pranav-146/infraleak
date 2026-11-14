"""Run one episode (A then B on a fresh shared backend) and write the raw log."""
from __future__ import annotations
import json
import shutil
import tempfile
import time
from pathlib import Path

from . import __version__
from .prompts import check_isolation
from .schema import validate_event
from .world import World


def run_episode(spec, raw_dir: Path, brain, keep_world=False):
    check_isolation(spec)
    ep_dir = Path(raw_dir) / spec.episode_id
    ep_dir.mkdir(parents=True, exist_ok=True)
    tmp = Path(tempfile.mkdtemp(prefix=f"world-{spec.episode_id}-"))
    t0 = time.time()
    try:
        w = World(spec.episode_id, spec.channel, tmp, spec.seed_files)
        before = dict(getattr(brain, "stats", {}))
        error = None
        for actor in ("A", "B"):
            try:
                brain.run_agent(actor, spec, w.handle(actor))
            except Exception as ex:  # keep the partial log, record failure
                error = f"{actor}: {type(ex).__name__}: {ex}"
                break
        events = [e.to_dict() for e in w.events]
        for e in events:
            validate_event(e)
        with open(ep_dir / "events.jsonl", "w") as f:
            for e in events:
                f.write(json.dumps(e) + "\n")
        (ep_dir / "spec.json").write_text(json.dumps(spec.to_dict(), indent=1))
        stats = {k: v for k, v in getattr(brain, "stats", {}).items() if not isinstance(v, dict)}
        delta = {k: stats[k] - before.get(k, 0) for k in stats}
        meta = {"episode_id": spec.episode_id, "brain": brain.name, "model": getattr(brain, "model", "scripted"),
                "seconds": round(time.time() - t0, 3), "n_events": len(events), "error": error,
                "brain_stats_delta": delta, "infraleak_version": __version__}
        (ep_dir / "run_meta.json").write_text(json.dumps(meta, indent=1))
        return events, meta
    finally:
        if not keep_world:
            shutil.rmtree(tmp, ignore_errors=True)


def load_episode(raw_dir: Path, episode_id: str):
    from .schema import ScenarioSpec
    d = Path(raw_dir) / episode_id
    spec = ScenarioSpec.from_dict(json.loads((d / "spec.json").read_text()))
    events = [json.loads(l) for l in (d / "events.jsonl").read_text().splitlines() if l]
    return spec, events
