"""Host tier (prototype): parse strace output into file-access events. Wiring into episodes is Phase II
(the AgentSight/Agent-Warden style eBPF tier). Kept here so the schema is exercised now."""
from __future__ import annotations
import re
import subprocess
import tempfile
from pathlib import Path

LINE = re.compile(r'^(?P<pid>\d+)\s+(?P<call>openat|read|write|unlink|rename)\((?P<args>.*)\)\s+=\s+(?P<ret>-?\d+)')
PATH = re.compile(r'"([^"]*)"')


def parse_strace(text: str, root_filter: str | None = None):
    out = []
    for raw in text.splitlines():
        m = LINE.match(raw.strip())
        if not m:
            continue
        p = PATH.search(m.group("args"))
        path = p.group(1) if p and m.group("call") in ("openat", "unlink", "rename") else ""
        if root_filter and path and not path.startswith(root_filter):
            continue
        if m.group("call") == "openat" and not path:
            continue
        mode = "write" if m.group("call") == "openat" and re.search(r"O_WRONLY|O_RDWR|O_CREAT", m.group("args")) else None
        out.append({"pid": int(m.group("pid")), "call": m.group("call"), "path": path,
                    "ret": int(m.group("ret")), "mode": mode or ("read" if m.group("call") == "openat" else None)})
    return out


def probe(root: str | None = None):
    """Run a tiny read+write under strace and return parsed events (checks the host tier works here)."""
    d = Path(root or tempfile.mkdtemp())
    (d / "probe.txt").write_text("hello")
    code = f"open(r'{d}/probe.txt').read(); open(r'{d}/out.txt','w').write('x')"
    r = subprocess.run(["strace", "-f", "-e", "trace=openat", "-o", "/dev/stdout", "python3", "-c", code],
                       capture_output=True, text=True)
    return [e for e in parse_strace(r.stdout, str(d))]
