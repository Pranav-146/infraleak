"""Host tier (real strace run, Linux only) and figure generation."""
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from infraleak.host_trace import TRACE_CALLS, ingest, parse_strace, strace_available

ROOT = Path(__file__).resolve().parent.parent

needs_strace = pytest.mark.skipif(not strace_available(), reason="strace not available (Linux/WSL only)")


@needs_strace
def test_host_tier_end_to_end(tmp_path):
    code = (f"import sys; sys.path.insert(0, {str(ROOT)!r})\n"
            "from pathlib import Path\n"
            "from infraleak.scenario import make_spec\n"
            "from infraleak.brains.scripted import ScriptedBrain\n"
            "from infraleak.runner import run_episode\n"
            "b = ScriptedBrain()\n"
            "for ch in ['fs', 'sqlite', 'git']:\n"
            "    for d in ['pos_verbatim', 'neg_control']:\n"
            f"        run_episode(make_spec('finance', ch, 'notes', d, 0), Path({str(tmp_path / 'raw')!r}), b, host_marks=True)\n")
    trace = tmp_path / "t.strace"
    subprocess.run(["strace", "-f", "-qq", "-y", "-e", f"trace={TRACE_CALLS}", "-o", str(trace), sys.executable, "-c", code],
                   check=True)
    stats = ingest(trace, tmp_path / "raw")
    assert stats["episodes_with_host"] == 6
    res = {}
    for d in (tmp_path / "raw").iterdir():
        spec = json.loads((d / "spec.json").read_text())
        evs = [json.loads(l) for l in (d / "events.jsonl").read_text().splitlines()]
        assert [e["eid"] for e in evs] == list(range(len(evs)))           # renumbered, ordered
        host = [e for e in evs if e["layer"] == "host"]
        assert host and all(e["content"] == "" for e in host)
        res[(spec["channel"], spec["design"])] = any(e["actor"] == "B" and e["op"] == "read" and e["owner"] == "A"
                                                     for e in host)
    # filesystem: host tier separates leak from control (per-file opens)
    assert res[("fs", "pos_verbatim")] and not res[("fs", "neg_control")]
    # sqlite: one db file -> host tier cannot tell them apart (both show B reading A-written data)
    assert res[("sqlite", "pos_verbatim")] and res[("sqlite", "neg_control")]


def test_parse_relative_paths_and_children():
    trace = "\n".join([
        '10 clone3({flags=CLONE_VFORK}, 88) = 11',
        '11 chdir("/tmp/world-aaaaaaaaaaaa-x/repo") = 0',
        '11 openat(AT_FDCWD, ".git/HEAD", O_RDONLY) = 3',
        '11 rename("/tmp/world-aaaaaaaaaaaa-x/repo/.git/a.lock", "/tmp/world-aaaaaaaaaaaa-x/repo/.git/a") = 0',
        '10 pread64(3</tmp/world-aaaaaaaaaaaa-x/workspace.db>, "", 4096, 0) = 4096',
    ])
    rs = parse_strace(trace)
    assert rs[0]["path"] == "/tmp/world-aaaaaaaaaaaa-x/repo/.git/HEAD"
    assert rs[1]["path"].endswith("/.git/a") and rs[1]["mode"] == "write"
    assert rs[2]["path"].endswith("workspace.db") and rs[2]["mode"] == "read"


def test_figures(tmp_path):
    pytest.importorskip("matplotlib")
    from infraleak.report import make_figures
    src = ROOT / "reports" / "baselines_scripted.csv"
    (tmp_path / "metrics.csv").write_text(src.read_text())
    out = make_figures(tmp_path)
    names = {Path(p).name for p in out}
    assert {"degradation.png", "degradation.svg", "recall_fpr.png", "recall_fpr.svg"} <= names
    assert (tmp_path / "figures" / "degradation.png").stat().st_size > 10_000
