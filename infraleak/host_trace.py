"""Host tier: real syscall telemetry (strace) joined to episodes.

How it works
  1. Episodes are generated under `strace -f` (Linux only). Every backend operation is preceded by a marker
     open() whose path encodes (t, actor). Both agents share one Python process in this testbed, so the marker
     plays the role a process tree plays in deployment (AgentSight-style per-agent attribution).
  2. `ingest()` parses the trace, keeps only syscalls that touch an episode's world directory, and turns them
     into `layer="host"` events: op = read/write/list, resource = path relative to the world, owner = last
     host-level writer of that path. Host events never carry content.
What the host tier can and cannot see is the point: on fs it sees per-file opens; on SQLite it sees only the
one database file; on git it sees opaque object files under .git/objects.
"""
from __future__ import annotations
import json
import posixpath
import re
import subprocess
import sys
import tempfile
from collections import defaultdict
from pathlib import Path

TRACE_CALLS = "pread64,pwrite64,openat,unlink,unlinkat,rename,renameat,renameat2,chdir,clone,clone3,vfork,fork"
LINE = re.compile(r'^(?P<pid>\d+)\s+(?P<call>\w+)\((?P<args>.*)\)\s+=\s+(?P<ret>-?\d+|\?)')
STR = re.compile(r'"((?:[^"\\]|\\.)*)"')
WORLD = re.compile(r"/world-(?P<eid>[0-9a-f]{12})-[^/]+/(?P<rel>.*)$")
MARK = re.compile(r"^\.mark/(?P<t>\d+)-(?P<actor>A|B|system)$")
WRITE_FLAGS = re.compile(r"O_WRONLY|O_RDWR|O_CREAT|O_TRUNC")


def strace_available() -> bool:
    try:
        return subprocess.run(["strace", "-V"], capture_output=True).returncode == 0
    except OSError:
        return False


def _lines(fh):
    """Yield complete syscall lines, stitching '<unfinished ...>' / '<... resumed>' pairs."""
    pending = {}
    for raw in fh:
        raw = raw.rstrip("\n")
        m = re.match(r"^(\d+)\s+(.*)$", raw)
        if not m:
            continue
        pid, rest = m.group(1), m.group(2)
        if rest.endswith("<unfinished ...>"):
            pending[pid] = rest[: -len("<unfinished ...>")].rstrip()
            continue
        r = re.match(r"^<\.\.\. \w+ resumed>(.*)$", rest)
        if r:
            rest = pending.pop(pid, "") + r.group(1)
        yield f"{pid} {rest}"


def parse_strace(text_or_lines, root_filter: str | None = None):
    """Generic parser -> dicts (pid, call, path, ret, mode). Relative paths resolved via tracked cwd."""
    it = text_or_lines.splitlines() if isinstance(text_or_lines, str) else text_or_lines
    cwd = {}
    out = []
    for line in _lines(l + "\n" for l in it) if isinstance(text_or_lines, str) else _lines(it):
        m = LINE.match(line)
        if not m:
            continue
        pid, call, args, ret = m.group("pid"), m.group("call"), m.group("args"), m.group("ret")
        ret = int(ret) if ret != "?" else -1
        if call in ("clone", "clone3", "vfork", "fork"):
            if ret > 0 and str(ret) not in cwd:      # child may already have logged its own chdir
                cwd[str(ret)] = cwd.get(pid)
            continue
        if call in ("pread64", "pwrite64"):
            fdp = re.match(r"\d+<([^>]*)>", args)
            if not fdp or ret < 0:
                continue
            path = fdp.group(1)
            if root_filter and not path.startswith(root_filter):
                continue
            out.append({"pid": int(pid), "call": call, "path": path, "ret": ret,
                        "mode": "write" if call == "pwrite64" else "read"})
            continue
        strs = STR.findall(args)
        if call == "chdir":
            if ret == 0 and strs:
                cwd[pid] = strs[0] if strs[0].startswith("/") else posixpath.join(cwd.get(pid) or "/", strs[0])
            continue
        if not strs:
            continue
        path = strs[-1] if call.startswith("rename") else strs[0]
        if not path.startswith("/") and cwd.get(pid):
            path = posixpath.normpath(posixpath.join(cwd[pid], path))   # strace paths are always POSIX
        if root_filter and not path.startswith(root_filter):
            continue
        if call == "openat":
            mode = "list" if "O_DIRECTORY" in args else ("write" if WRITE_FLAGS.search(args) else "read")
        else:
            mode = "write"
        out.append({"pid": int(pid), "call": call, "path": path, "ret": ret, "mode": mode})
    return out


def host_events_from_trace(trace_path):
    """episode_id -> list of host event dicts (without eid), attributed via markers."""
    by_ep = defaultdict(list)
    owner = defaultdict(dict)
    ctx = {"ep": None, "t": 0, "actor": "system"}
    last = {}
    with open(trace_path, errors="replace") as fh:
        for r in parse_strace(fh):
            w = WORLD.search(r["path"])
            if not w:
                continue
            ep, rel = w.group("eid"), w.group("rel")
            mk = MARK.match(rel)
            if mk:
                ctx = {"ep": ep, "t": int(mk.group("t")), "actor": mk.group("actor")}
                continue
            if r["ret"] < 0 or rel.startswith(".mark"):
                continue
            t, actor = (ctx["t"], ctx["actor"]) if ctx["ep"] == ep else (0, "system")
            res = rel[len("shared/"):] if rel.startswith("shared/") else rel
            res = res or "/"
            op = r["mode"]
            key = (t, actor, op, res)
            if last.get(ep) == key:           # collapse repeated identical syscalls within one op
                continue
            last[ep] = key
            own = owner[ep].get(res, "")
            if op == "write":
                owner[ep][res] = actor
                own = actor
            by_ep[ep].append({"t": t, "actor": actor, "op": op, "resource": res, "owner": own,
                              "meta": {"syscall": r["call"], "pid": r["pid"]}})
    return by_ep


LAYER_RANK = {"host": 0, "service": 1, "app": 2}


def merge_into_episode(ep_dir: Path, host_events):
    f = Path(ep_dir) / "events.jsonl"
    evs = [json.loads(l) for l in f.read_text().splitlines() if l]
    evs = [e for e in evs if e["layer"] != "host"]
    eid = evs[0]["episode_id"]
    for i, h in enumerate(host_events):
        evs.append({"episode_id": eid, "eid": -1, "t": h["t"], "layer": "host", "actor": h["actor"], "op": h["op"],
                    "resource": h["resource"], "owner": h["owner"], "content": "", "meta": h["meta"], "_k": i})
    evs.sort(key=lambda e: (e["t"], LAYER_RANK[e["layer"]], e.get("_k", e["eid"])))
    with open(f, "w") as out:
        for i, e in enumerate(evs):
            e.pop("_k", None)
            e["eid"] = i
            out.write(json.dumps(e) + "\n")
    return len(host_events)


def ingest(trace_path, raw_dir: Path):
    by_ep = host_events_from_trace(trace_path)
    n = 0
    for ep, hevs in by_ep.items():
        d = Path(raw_dir) / ep
        if (d / "events.jsonl").exists():
            n += merge_into_episode(d, hevs)
            meta = json.loads((d / "run_meta.json").read_text())
            meta["host_events"] = len(hevs)
            (d / "run_meta.json").write_text(json.dumps(meta, indent=1))
    return {"episodes_with_host": len(by_ep), "host_events": n}


def run_traced(argv, trace_path):
    cmd = ["strace", "-f", "-qq", "-y", "-e", f"trace={TRACE_CALLS}", "-o", str(trace_path), sys.executable, *argv]
    r = subprocess.run(cmd)
    if r.returncode != 0:
        raise RuntimeError(f"traced run failed ({r.returncode})")


def probe(root: str | None = None):
    """Tiny read+write under strace; returns parsed events (checks the host tier works on this machine)."""
    d = Path(root or tempfile.mkdtemp())
    (d / "probe.txt").write_text("hello")
    code = f"open(r'{d}/probe.txt').read(); open(r'{d}/out.txt','w').write('x')"
    r = subprocess.run(["strace", "-f", "-e", "trace=openat", "-o", "/dev/stdout", sys.executable, "-c", code],
                       capture_output=True, text=True)
    return parse_strace(r.stdout, str(d))
