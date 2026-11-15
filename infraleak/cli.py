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


def _step(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def finalize(data: Path, judge=None):
    _step("labelling episodes with the oracle (raw log + vault)")
    labels = P.label_all(data)
    _step(f"freezing {len(labels)} labels (sha256 manifest)")
    P.freeze(data)
    specs = P.load_specs(data, [L["episode_id"] for L in labels])
    _step("assigning splits + leakage checks")
    stats = check_splits(labels, specs)
    profiles = P.usable_profiles(data, labels)
    _step(f"building {len(profiles)} observer views: {', '.join(profiles)}")
    views = P.build_views(data, labels, profiles)
    _step("writing release (train/val views+labels, test views only; test labels sealed)")
    P.write_release(data, labels, views)
    P.dataset_card(labels, stats, data, profiles)
    dets = default_detectors() + ([LLMJudge(judge)] if judge else [])
    _step(f"evaluating {len(dets)} detectors x {len(profiles)} views x {len(P.EVAL_SPLITS)} splits")
    res = evaluate(labels, views, dets, P.EVAL_SPLITS)
    write_results(res, data / "results")
    _step("figures")
    try:
        from .report import make_figures
        make_figures(data / "results")
    except ImportError as ex:
        print(f"  (skipped figures: {ex}; pip install matplotlib)")
    _step("verifying manifest + oracle reproducibility")
    P.verify(data)
    return labels, stats


def cmd_gen(a):
    from .brains.scripted import ScriptedBrain
    specs = list(scripted_grid(a.seeds))
    _step(f"running {len(specs)} scripted episodes -> {a.data}/raw" + (" (host markers on)" if a.host_marks else ""))
    P.generate(specs, Path(a.data), ScriptedBrain(), host_marks=a.host_marks)


def cmd_build(a):
    data = Path(a.data)
    t = time.time()
    if a.host_trace:
        from .host_trace import strace_available, run_traced, ingest
        if not strace_available():
            raise SystemExit("--host-trace needs strace (Linux / WSL). Run without it on Windows/macOS.")
        data.mkdir(parents=True, exist_ok=True)
        trace = data / "host.strace"
        _step("generating under strace -f (host tier)")
        run_traced(["-m", "infraleak.cli", "gen", "--data", str(data), "--seeds", str(a.seeds), "--host-marks"], trace)
        _step(f"ingesting host trace ({trace.stat().st_size / 1e6:.0f} MB)")
        print("  ", ingest(trace, data / "raw"))
        if not a.keep_trace:
            trace.unlink()
    else:
        cmd_gen(argparse.Namespace(data=str(data), seeds=a.seeds, host_marks=False))
    labels, stats = finalize(data)
    print(json.dumps(stats, indent=1))
    print(f"done in {time.time() - t:.1f}s; see {data}/DATASET_CARD.md and {data}/results/summary.md")


def cmd_run_llm(a):
    data = Path(a.data)
    brain = _llm(a)
    variants = tuple(v.strip() for v in a.variants.split(",") if v.strip())
    specs = list(spontaneous_grid(a.seeds, brain="llm:" + a.model, variants=variants))[: a.limit or None]
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
    per_variant = {}
    errors = 0
    for s in specs:
        ev, meta = run_episode(s, raw, brain)
        errors += meta["error"] is not None
        L = label_episode(s, ev)
        for k, v in L["stages"].items():
            stages[k] += v
        pv = per_variant.setdefault(s.design, [0, 0])
        pv[0] += L["label"]
        pv[1] += 1
    dt = time.time() - t
    st = brain.stats
    acts = st["steps"] + st["malformed"]
    out = {"model": a.model, "episodes": len(specs), "seconds": round(dt, 1),
           "episodes_per_hour": round(3600 * len(specs) / dt, 1),
           "malformed_rate": round(st["malformed"] / acts, 3) if acts else None,
           "completion_tokens_per_s": round(st["completion_tokens"] / st["seconds"], 1) if st["seconds"] else None,
           "errors": errors, "stage_rates": {k: v / len(specs) for k, v in stages.items()},
           "transfer_rate_by_variant": {k: f"{a}/{b}" for k, (a, b) in per_variant.items()}, "ended_by": st["ended_by"]}
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
    have = {e["layer"] for e in events}
    profs = {k: v for k, v in profs.items() if set(v["layers"]) & have}
    for p in ["full_ref"] + [x for x in (a.profiles.split(",") if a.profiles else profs) if x != "full_ref" and x in profs]:
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
    p.add_argument("--host-trace", action="store_true", help="also record the host tier with strace (Linux/WSL)")
    p.add_argument("--keep-trace", action="store_true")
    p.set_defaults(f=cmd_build)
    p = sub.add_parser("gen", help="generate raw scripted episodes only")
    p.add_argument("--data", default="data/scripted")
    p.add_argument("--seeds", type=int, default=10)
    p.add_argument("--host-marks", action="store_true")
    p.set_defaults(f=cmd_gen)
    p = sub.add_parser("report", help="(re)draw figures from results/metrics.csv")
    p.add_argument("--data", default="data/scripted")
    p.set_defaults(f=lambda a: print(__import__("infraleak.report", fromlist=["x"]).make_figures(Path(a.data) / "results")))
    p = sub.add_parser("run-llm", help="spontaneous LLM episodes (resumable)")
    p.add_argument("--data", default="data/llm")
    p.add_argument("--seeds", type=int, default=5)
    p.add_argument("--limit", type=int, default=0)
    p.add_argument("--no-finalize", action="store_true")
    p.add_argument("--variants", default="spontaneous,spontaneous_policy,spontaneous_control",
                   help="comma list of LLM variants (see scenario.LLM_VARIANTS)")
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
