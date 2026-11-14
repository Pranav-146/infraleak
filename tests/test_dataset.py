"""Generator, isolation, oracle-vs-design agreement, splits, views, freeze/tamper."""
import json
import shutil
import pytest
from pathlib import Path

from infraleak.scenario import scripted_grid, make_spec, DESIGNS
from infraleak.prompts import check_isolation, task_prompt
from infraleak.brains.scripted import ScriptedBrain
from infraleak.runner import run_episode
from infraleak.oracle import label_episode
from infraleak.views import load_profiles, apply_view
from infraleak.text import match_secret
from infraleak.schema import Secret
from infraleak import pipeline as P
from infraleak.cli import finalize


def test_spec_deterministic_and_unique():
    a = make_spec("finance", "fs", "notes", "pos_verbatim", 3)
    b = make_spec("finance", "fs", "notes", "pos_verbatim", 3)
    assert a.to_dict() == b.to_dict()
    codes = [s.secrets[1]["text"] for s in scripted_grid(3)]
    assert len(codes) == len(set(codes))


def test_isolation_b_prompt_has_no_secret():
    for s in scripted_grid(1):
        check_isolation(s)
        assert s.private_doc not in task_prompt(s, "B")


def test_decoys_never_match_secrets():
    for s in scripted_grid(2):
        for sec in s.secrets:
            for t in s.policy["allowed_disclosure"]:
                assert match_secret(t, Secret(**sec)) is None, (s.template_id, sec["sid"], t)


def test_oracle_agrees_with_design(tmp_path):
    b = ScriptedBrain()
    for spec in scripted_grid(1):
        ev, meta = run_episode(spec, tmp_path, b)
        assert meta["error"] is None
        L = label_episode(spec, ev)
        pos = DESIGNS[spec.design][2]
        assert L["label"] == int(pos), spec.template_id
        assert L["flow_class"] == (spec.design.split("_", 1)[1] if pos else "none")
        assert not L["unexplained"]
        if spec.design == "neg_read_only":
            assert L["stages"]["access"] and not L["stages"]["transfer"]


@pytest.fixture(scope="module")
def small(tmp_path_factory):
    data = tmp_path_factory.mktemp("d")
    P.generate(list(scripted_grid(5, a_tasks=["notes"])), data, ScriptedBrain())
    finalize(data)
    return data


def test_splits_and_release(small):
    labels = P.load_labels(small)
    splits = {L["split"] for L in labels}
    assert {"train", "test_id", "test_ood_domain", "test_ood_channel", "test_ood_class"} <= splits
    assert (small / "release" / "train" / "labels.jsonl").exists()
    assert not (small / "release" / "test_id" / "labels.jsonl").exists()   # test labels sealed
    assert (small / "sealed" / "test_id" / "labels.jsonl").exists()
    assert (small / "results" / "summary.md").exists()


def test_views_mask_and_are_deterministic(small):
    profs = load_profiles()
    L = next(x for x in P.load_labels(small) if x["design"] == "pos_verbatim")
    from infraleak.runner import load_episode
    spec, ev = load_episode(small / "raw", L["episode_id"])
    secret = spec.secrets[1]["text"]
    for name, cfg in profs.items():
        v1, v2 = apply_view(ev, name, cfg), apply_view(ev, name, cfg)
        assert v1 == v2
        dump = json.dumps(v1)
        if cfg["content"] in ("none", "hash"):
            assert secret not in dump, name
        if cfg["content"] == "sinks_only":
            assert all(e["content"] == "" for e in v1 if e["op"] in ("read", "search", "list"))
    assert len(apply_view(ev, "app_meta_drop50", profs["app_meta_drop50"])) <= len(apply_view(ev, "app_meta", profs["app_meta"]))


def test_freeze_detects_tampering(small, tmp_path):
    P.verify(small)
    copy = tmp_path / "copy"
    shutil.copytree(small, copy)
    f = next((copy / "raw").iterdir()) / "events.jsonl"
    f.write_text(f.read_text().replace('"A"', '"B"', 1))
    with pytest.raises(AssertionError):
        P.verify(copy)
