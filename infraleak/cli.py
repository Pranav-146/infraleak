"""Command line entry point:  python -m infraleak.cli <command> ..."""
from __future__ import annotations
import argparse
import json
import time
from pathlib import Path

from . import pipeline as P
from .detectors import default_detectors, LLMJudge
from .eval import evaluate, write_results
from .scenario import scripted_grid, spontaneous_grid
from .splits import check_splits
from .views import load_profiles, apply_view


def _llm(args):
    from .brains.llm import LLMBrain
    return LLMBrain(base_url=args.base_url, model=args.model, api_key=args.api_key,
                    temperature=args.temperature, max_steps=args.max_steps)


def finalize(data: Path, judge=None):
    labels = P.label_all(data)
    P.freeze(data)
    specs = P.load_specs(data, [L["episode_id"] for L in labels])
    stats = check_splits(labels, specs)
    profiles = load_profiles()
    views = P.build_views(data, labels, profiles)
    P.write_release(data, labels, views)
    P.dataset_card(labels, stats, data, profiles)
    dets = default_detectors() + ([LLMJudge(judge)] if judge else [])
    res = evaluate(labels, views, dets, P.EVAL_SPLITS)
    write_results(res, data / "results")
    P.verify(data)
    return labels, stats


def cmd_build(a):
    data = Path(a.data)
    t = time.time()
    specs = list(scripted_grid(a.seeds))
    from .brains.scripted import ScriptedBrain
    print(f"running {len(specs)} scripted episodes -> {data}/raw")
    P.generate(specs, data, ScriptedBrain())
    labels, stats = finalize(data)
    print(json.dumps(stats, indent=1))
    print(f"done in {time.time() - t:.1f}s; see {data}/DATASET_CARD.md and {data}/results/summary.md")


def cmd_run_llm(a):
    data = Path(a.data)
    brain = _llm(a)
    specs = list(spontaneous_grid(a.seeds, brain="llm:" + a.model))[: a.limit or None]
    print(f"{len(specs)} LLM episodes with {a.model} @ {a.base_url} (resumable)")
    t = time.time()
    n = P.generate(specs, data, brain, log_every=10)
    dt = time.time() - t
    print(f"ran {n} new episodes in {dt:.0f}s; brain stats: {brain.stats}")
    if not a.no_finalize:
        finalize(data)
        print(f"labels/views/results written under {data}")


def cmd_bench(a):
    """Model benchmark: malformed-action rate, tokens/s, episodes/hour, oracle stage rates."""
    from .runner import run_episode
    from .oracle import label_episode
    import tempfile
    brain = _llm(a)
    specs = list(spontaneous_grid(1, brain="bench"))[: a.n]
    raw = Path(tempfile.mkdtemp())
    t = time.time()
    stages = {"exposure": 0, "access": 0, "transfer": 0}
    errors = 0
    for s in specs:
        ev, meta = run_episode(s, raw, brain)
        errors += meta["error"] is not None
        for k, v in label_episode(s, ev)["stages"].items():
            stages[k] += v
    dt = time.time() - t
    st = brain.stats
    acts = st["steps"] + st["malformed"]
    out = {"model": a.model, "episodes": len(specs), "seconds": round(dt, 1),
           "episodes_per_hour": round(3600 * len(specs) / dt, 1),
           "malformed_rate": round(st["malformed"] / acts, 3) if acts else None,
           "completion_tokens_per_s": round(st["completion_tokens"] / st["seconds"], 1) if st["seconds"] else None,
           "errors": errors, "stage_rates": {k: v / len(specs) for k, v in stages.items()}, "ended_by": st["ended_by"]}
    print(json.dumps(out, indent=1))


def cmd_finalize(a):
    labels, stats = finalize(Path(a.data))
    print(json.dumps(stats, indent=1))


def cmd_verify(a):
    P.verify(Path(a.data))
    print("OK: raw logs and labels match MANIFEST, oracle reproducible")


def cmd_show(a):
    """Print one episode: raw log, oracle label, then what each observer profile sees."""
    from .runner import load_episode
    data = Path(a.data)
    labels = P.load_labels(data)
    L = next((x for x in labels if x["episode_id"] == a.episode or (a.design and x["design"] == a.design
              and x["channel"] == a.channel)), None)
    if L is None:
        raise SystemExit("no matching episode")
    spec, events = load_episode(data / "raw", L["episode_id"])
    print(f"=== episode {spec.episode_id}  template={spec.template_id}  seed={spec.seed}")
    print("--- secrets (vault; never shown to detectors):")
    for s in spec.secrets:
        print("   ", s["sid"], s["text"] or s["semantic"])
    print("--- [oracle:...] column is annotation for humans; it is NOT part of any view")
    print(f"--- oracle: label={L['label']} class={L['flow_class']} stages={L['stages']} edges={L['edges']}")
    profs = load_profiles()
    for p in ["full_ref"] + [x for x in (a.profiles.split(",") if a.profiles else profs) if x != "full_ref"]:
        v = apply_view(events, p, profs[p])
        print(f"\n--- view: {p}  ({profs[p]['note']})  {len(v)} events")
        for e in v:
            c = e["content"].replace("\n", " | ")[:110]
            extra = e["meta"].get("statement") or (f"{len(e['meta']['shingles'])} shingles" if "shingles" in e["meta"] else "")
            print(f"  [{e['eid']:2}] t={e['t']:2} {e['layer']:7} {e['actor']} {e['op']:6} {e['resource'][:28]:28} "
                  f"owner={e['owner'] or '-':6} [oracle:{L['event_stage'].get(str(e['eid']), '-'):8}] {c or extra}")


def main(argv=None):
    ap = argparse.ArgumentParser(prog="infraleak")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def llm_args(p):
        p.add_argument("--base-url", default="http://localhost:11434/v1")
        p.add_argument("--model", default="qwen2.5:7b-instruct")
        p.add_argument("--api-key", default="ollama")
        p.add_argument("--temperature", type=float, default=0.7)
        p.add_argument("--max-steps", type=int, default=12)

    p = sub.add_parser("build", help="scripted (designed) dataset end to end")
    p.add_argument("--data", default="data/scripted")
    p.add_argument("--seeds", type=int, default=10)
    p.set_defaults(f=cmd_build)
    p = sub.add_parser("run-llm", help="spontaneous LLM episodes (resumable)")
    p.add_argument("--data", default="data/llm")
    p.add_argument("--seeds", type=int, default=5)
    p.add_argument("--limit", type=int, default=0)
    p.add_argument("--no-finalize", action="store_true")
    llm_args(p)
    p.set_defaults(f=cmd_run_llm)
    p = sub.add_parser("bench", help="benchmark a model before a long run")
    p.add_argument("--n", type=int, default=20)
    llm_args(p)
    p.set_defaults(f=cmd_bench)
    p = sub.add_parser("finalize", help="label + freeze + split + views + eval on existing raw logs")
    p.add_argument("--data", required=True)
    p.set_defaults(f=cmd_finalize)
    p = sub.add_parser("verify")
    p.add_argument("--data", required=True)
    p.set_defaults(f=cmd_verify)
    p = sub.add_parser("show", help="print one episode through every observer view")
    p.add_argument("--data", default="data/scripted")
    p.add_argument("--episode", default="")
    p.add_argument("--design", default="pos_verbatim")
    p.add_argument("--channel", default="sqlite")
    p.add_argument("--profiles", default="")
    p.set_defaults(f=cmd_show)
    a = ap.parse_args(argv)
    a.f(a)


if __name__ == "__main__":
    main()
