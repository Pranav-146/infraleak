"""Observer views V_o(E): rule-based masking of the raw log. Deterministic (seeded by profile+episode+eid)."""
from __future__ import annotations
import hashlib
import re
from pathlib import Path
import yaml

DEFAULT_CFG = Path(__file__).resolve().parent.parent / "configs" / "visibility.yaml"
HASH_SALT = "infraleak-view-salt-v1"


def load_profiles(path=None):
    return yaml.safe_load(Path(path or DEFAULT_CFG).read_text())["profiles"]


def shingles(text: str, n: int = 3):
    w = re.findall(r"[a-z0-9]+", (text or "").lower())
    grams = {" ".join(w[i:i + n]) for i in range(max(0, len(w) - n + 1))} or ({" ".join(w)} if w else set())
    return sorted(hashlib.sha256((HASH_SALT + g).encode()).hexdigest()[:12] for g in grams)


def _keep(profile_name, episode_id, eid, rate):
    if rate <= 0:
        return True
    h = int(hashlib.sha256(f"{profile_name}|{episode_id}|{eid}".encode()).hexdigest()[:8], 16) / 0xFFFFFFFF
    return h >= rate


def apply_view(events, profile_name, profile):
    out = []
    for e in events:
        if e["layer"] not in profile["layers"] or e["actor"] not in profile["actors"]:
            continue
        if profile["ops"] != "all" and e["op"] not in profile["ops"]:
            continue
        if not _keep(profile_name, e["episode_id"], e["eid"], profile.get("drop", 0.0)):
            continue
        v = dict(e)
        v["meta"] = dict(e["meta"])
        mode = profile["content"]
        if mode == "none" or (mode == "sinks_only" and e["op"] not in ("write", "reply")):
            v["content"] = ""
        elif mode == "hash":
            v["meta"]["shingles"] = shingles(e["content"])
            v["content"] = ""
        v["meta"]["content_visible"] = bool(v["content"]) or (e["content"] == "" and mode == "all")
        out.append(v)
    return out
