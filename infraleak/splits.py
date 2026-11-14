"""Split assignment. Splits are by scenario *template* (and held-out seeds), never by random event.

test_ood_domain  : every legal-domain episode               (unseen organisation / vocabulary)
test_ood_channel : every git-channel episode (non-legal)    (unseen infrastructure)
test_ood_class   : paraphrase positives + paraphrase decoys (unseen flow class)
remaining        : seed % 5 -> 0,1,2 train | 3 val | 4 test_id (held-out seeds, same templates)
"""
from __future__ import annotations
from collections import Counter, defaultdict

OOD_DOMAIN, OOD_CHANNEL = "legal", "git"
OOD_CLASS_DESIGNS = {"pos_paraphrase", "neg_decoy_para"}
SPLITS = ("train", "val", "test_id", "test_ood_domain", "test_ood_channel", "test_ood_class")


def assign_split(row) -> str:
    if row["domain"] == OOD_DOMAIN:
        return "test_ood_domain"
    if row["channel"] == OOD_CHANNEL:
        return "test_ood_channel"
    if row["design"] in OOD_CLASS_DESIGNS:
        return "test_ood_class"
    return {0: "train", 1: "train", 2: "train", 3: "val", 4: "test_id"}[row["seed"] % 5]


def check_splits(labels, specs) -> dict:
    """Leakage checks between train and every evaluation split. Raises AssertionError on violation."""
    by = defaultdict(list)
    for L in labels:
        by[L["split"]].append(L)
    train = by["train"]
    tr_dom = {L["domain"] for L in train}
    tr_ch = {L["channel"] for L in train}
    tr_des = {L["design"] for L in train}
    tr_seed = {(L["template_id"], L["seed"]) for L in train}
    assert OOD_DOMAIN not in tr_dom and all(L["domain"] == OOD_DOMAIN for L in by["test_ood_domain"])
    assert OOD_CHANNEL not in tr_ch and all(L["channel"] == OOD_CHANNEL for L in by["test_ood_channel"])
    assert not (OOD_CLASS_DESIGNS & tr_des)
    for s in ("val", "test_id"):
        assert not ({(L["template_id"], L["seed"]) for L in by[s]} & tr_seed)
    ids = [L["episode_id"] for L in labels]
    assert len(ids) == len(set(ids)), "duplicate episode ids"

    def codes(ls):
        out = set()
        for L in ls:
            for s in specs[L["episode_id"]].secrets:
                if s["sid"] == "code":
                    out.add(s["text"])
        return out
    trc = codes(train)
    for s in SPLITS[1:]:
        assert not (trc & codes(by[s])), f"secret value shared between train and {s}"
    return {s: dict(n=len(by[s]), pos=sum(L["label"] for L in by[s]),
                    by_class=dict(Counter(L["flow_class"] for L in by[s]))) for s in SPLITS}
