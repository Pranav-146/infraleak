"""Event log schema (MAScope-style actor/op/resource/content + owner + layer) and scenario spec."""
from __future__ import annotations
import json
from dataclasses import dataclass, field, asdict
from pathlib import Path

LAYERS = ("app", "service", "host")
OPS = ("list", "read", "write", "search", "reply")
CONTENT_META_KEYS = ("message", "query", "params")  # meta keys that would carry content; must never appear


@dataclass
class Event:
    episode_id: str
    eid: int
    t: int
    layer: str      # app | service
    actor: str      # A | B
    op: str
    resource: str   # path / "reply"
    owner: str      # who last wrote the resource (A | B | system | "")
    content: str    # payload; "" in service layer
    meta: dict = field(default_factory=dict)

    def to_dict(self):
        return asdict(self)


@dataclass
class Secret:
    sid: str
    kind: str                 # code | number | semantic
    text: str = ""
    semantic: list = field(default_factory=list)   # list of alternative-lists

    def to_dict(self):
        return asdict(self)


@dataclass
class ScenarioSpec:
    episode_id: str
    template_id: str
    domain: str
    channel: str
    seed: int
    a_task: str
    design: str
    brain: str
    a_path: str
    a_task_text: str
    b_task_text: str
    private_doc: str
    secrets: list
    seed_files: dict
    decoys: dict
    policy: dict
    b_mode: str = "list_read"
    b_sink: str = "reply"
    model_tag: str = "scripted"

    def to_dict(self):
        return asdict(self)

    @staticmethod
    def from_dict(d):
        return ScenarioSpec(**d)

    def secret_objs(self):
        return [Secret(**s) for s in self.secrets]


_SCHEMA = None


def validate_event(d: dict) -> None:
    import jsonschema
    global _SCHEMA
    if _SCHEMA is None:
        _SCHEMA = json.loads((Path(__file__).parent / "event.schema.json").read_text())
    jsonschema.validate(d, _SCHEMA)
    bad = [k for k in CONTENT_META_KEYS if k in d["meta"]]
    if bad:
        raise ValueError(f"content-bearing meta keys present: {bad}")
    if d["layer"] in ("service", "host") and d["content"] != "":
        raise ValueError(f"{d['layer']}-layer events must not carry content")
