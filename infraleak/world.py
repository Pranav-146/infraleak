"""Shared-infrastructure world: one interface (list/read/write/search) over three real backends.

fs     : plain directory on disk                       -> app-layer events only
sqlite : real SQLite db, parameterised statements      -> app + service (statement log) events
git    : real git repo, one commit per write           -> app + service (command log) events

App-layer events carry content (what the agent framework sees). Service-layer events carry only
metadata (statement / command template, rows, bytes): values are bound parameters and never logged.
"""
from __future__ import annotations
import json
import os
import posixpath
import sqlite3
import subprocess
from pathlib import Path

from .schema import Event


class PathError(ValueError):
    pass


def clean_path(p: str) -> str:
    p = (p or "").strip().replace("\\", "/")
    for pre in ("/shared/", "shared/", "./"):
        if p.startswith(pre):
            p = p[len(pre):]
    p = p.lstrip("/")
    n = posixpath.normpath(p) if p else ""
    if n in ("", "."):
        return ""
    if n.startswith("..") or "/../" in f"/{n}/":
        raise PathError(f"path escapes workspace: {p}")
    return n


class FSChannel:
    name = "fs"

    def __init__(self, root: Path):
        self.root = Path(root) / "shared"
        self.root.mkdir(parents=True, exist_ok=True)

    def seed(self, files):
        for p, c in files.items():
            self._w(p, c)

    def _w(self, p, c):
        f = self.root / p
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(c)

    def list(self, prefix):
        out = sorted(f.relative_to(self.root).as_posix() for f in self.root.rglob("*") if f.is_file())
        return [p for p in out if p.startswith(prefix)], None

    def read(self, p):
        f = self.root / p
        return (f.read_text() if f.is_file() else None), None

    def write(self, p, c, actor):
        self._w(p, c)
        return None

    def search(self, q):
        hits = []
        for p in self.list("")[0]:
            for i, line in enumerate((self.root / p).read_text().splitlines(), 1):
                if q.lower() in line.lower():
                    hits.append((p, i, line))
        return hits, None


class SQLiteChannel:
    name = "sqlite"

    def __init__(self, root: Path):
        self.db = sqlite3.connect(str(Path(root) / "workspace.db"))
        self.db.execute("CREATE TABLE IF NOT EXISTS notes(path TEXT PRIMARY KEY, author TEXT, body TEXT)")

    def seed(self, files):
        for p, c in files.items():
            self.db.execute("INSERT OR REPLACE INTO notes VALUES (?,?,?)", (p, "system", c))
        self.db.commit()

    def list(self, prefix):
        sql = "SELECT path FROM notes WHERE path LIKE ? ORDER BY path"
        rows = [r[0] for r in self.db.execute(sql, (prefix + "%",))]
        return rows, {"statement": sql, "rows": len(rows)}

    def read(self, p):
        sql = "SELECT body FROM notes WHERE path = ?"
        r = self.db.execute(sql, (p,)).fetchone()
        return (r[0] if r else None), {"statement": sql, "rows": int(r is not None), "bytes": len(r[0]) if r else 0}

    def write(self, p, c, actor):
        sql = "INSERT OR REPLACE INTO notes(path, author, body) VALUES (?,?,?)"
        self.db.execute(sql, (p, actor, c))
        self.db.commit()
        return {"statement": sql, "rows": 1, "bytes": len(c)}

    def search(self, q):
        sql = "SELECT path, body FROM notes WHERE body LIKE ? ORDER BY path"
        hits = []
        for p, body in self.db.execute(sql, (f"%{q}%",)):
            for i, line in enumerate(body.splitlines(), 1):
                if q.lower() in line.lower():
                    hits.append((p, i, line))
        return hits, {"statement": sql, "rows": len(hits)}


class GitChannel:
    name = "git"

    def __init__(self, root: Path):
        self.dir = Path(root) / "repo"
        self.dir.mkdir(parents=True, exist_ok=True)
        self._git("init", "-q", "-b", "main")

    def _git(self, *args, actor="system", check=True):
        env = dict(os.environ, GIT_AUTHOR_NAME=actor, GIT_AUTHOR_EMAIL=f"{actor}@agents.local",
                   GIT_COMMITTER_NAME=actor, GIT_COMMITTER_EMAIL=f"{actor}@agents.local",
                   GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1")
        r = subprocess.run(["git", *args], cwd=self.dir, env=env, capture_output=True, text=True)
        if check and r.returncode != 0:
            raise RuntimeError(r.stderr)
        return r

    def seed(self, files):
        for p, c in files.items():
            f = self.dir / p
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(c)
        self._git("add", "-A")
        self._git("commit", "-q", "-m", "seed workspace")

    def list(self, prefix):
        cmd = "git ls-tree -r --name-only HEAD"
        out = self._git("ls-tree", "-r", "--name-only", "HEAD").stdout.split()
        rows = [p for p in out if p.startswith(prefix)]
        return rows, {"statement": cmd, "rows": len(rows)}

    def read(self, p):
        r = self._git("show", f"HEAD:{p}", check=False)
        ok = r.returncode == 0
        return (r.stdout if ok else None), {"statement": "git show HEAD:<path>", "rows": int(ok),
                                            "bytes": len(r.stdout) if ok else 0}

    def write(self, p, c, actor):
        f = self.dir / p
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(c)
        self._git("add", p)
        self._git("commit", "-q", "-m", f"update {p}", actor=actor)
        sha = self._git("rev-parse", "--short", "HEAD").stdout.strip()
        return {"statement": "git add <path> && git commit", "rows": 1, "bytes": len(c), "commit": sha,
                "author": actor}

    def search(self, q):
        r = self._git("grep", "-i", "-F", "-n", "-e", q, "HEAD", check=False)
        hits = []
        for line in r.stdout.splitlines():
            _, p, i, text = line.split(":", 3)
            hits.append((p, int(i), text))
        return hits, {"statement": "git grep -i -F -n -e <query> HEAD", "rows": len(hits)}


CHANNEL_CLASSES = {"fs": FSChannel, "sqlite": SQLiteChannel, "git": GitChannel}


class World:
    def __init__(self, episode_id: str, channel: str, root: Path, seed_files: dict, host_marks: bool = False):
        self.episode_id = episode_id
        self.root, self.host_marks = Path(root), host_marks
        self.ch = CHANNEL_CLASSES[channel](Path(root))
        self.ch.seed(seed_files)
        self.owners = {p: "system" for p in seed_files}
        self.events: list[Event] = []
        self.t = 0
        self.replies: dict[str, str] = {}

    def _emit(self, layer, actor, op, resource, owner, content, meta):
        self.events.append(Event(self.episode_id, len(self.events), self.t, layer, actor, op, resource,
                                 owner, content, meta))

    def mark(self, actor):
        """Host-tier attribution marker: a deliberately failing open() whose path encodes (t, actor).
        Here both agents share one process; in deployment attribution comes from the process tree."""
        if self.host_marks:
            try:
                os.open(str(self.root / ".mark" / f"{self.t}-{actor}"), os.O_RDONLY)
            except OSError:
                pass

    def _op(self, actor, op, resource, owner, content, app_meta, svc_meta):
        self.t += 1
        if svc_meta is not None:
            self._emit("service", actor, op, resource, owner, "", svc_meta)
        self._emit("app", actor, op, resource, owner, content, app_meta)

    def t_next(self, actor):
        """Called just before a backend operation: marks the upcoming op's clock value t+1."""
        self.t += 1
        self.mark(actor)
        self.t -= 1

    def handle(self, actor: str) -> "AgentHandle":
        return AgentHandle(self, actor)


class AgentHandle:
    """Identity-bound tool surface given to one agent. Every call is logged."""

    def __init__(self, world: World, actor: str):
        self.w, self.actor = world, actor

    def list(self, prefix: str = "") -> str:
        prefix = clean_path(prefix)
        self.w.t_next(self.actor)
        rows, svc = self.w.ch.list(prefix)
        out = "\n".join(rows) if rows else "(empty)"
        self.w._op(self.actor, "list", prefix or "/", "", out, {"n": len(rows)}, svc)
        return out

    def read(self, path: str) -> str:
        try:
            p = clean_path(path)
        except PathError as e:
            self.w._op(self.actor, "read", str(path), "", f"ERROR: {e}", {"ok": False}, None)
            return f"ERROR: {e}"
        self.w.t_next(self.actor)
        body, svc = self.w.ch.read(p)
        out = body if body is not None else f"ERROR: {p} not found"
        self.w._op(self.actor, "read", p, self.w.owners.get(p, ""), out,
                   {"ok": body is not None, "bytes": len(body or "")}, svc)
        return out

    def write(self, path: str, content: str) -> str:
        try:
            p = clean_path(path)
        except PathError as e:
            self.w._op(self.actor, "write", str(path), "", f"ERROR: {e}", {"ok": False}, None)
            return f"ERROR: {e}"
        if not p:
            return "ERROR: empty path"
        self.w.t_next(self.actor)
        svc = self.w.ch.write(p, content, self.actor)
        self.w.owners[p] = self.actor
        self.w._op(self.actor, "write", p, self.actor, content, {"ok": True, "bytes": len(content)}, svc)
        return f"wrote {len(content)} bytes to {p}"

    def search(self, query: str) -> str:
        self.w.t_next(self.actor)
        hits, svc = self.w.ch.search(query)
        out = "\n".join(f"{p}:{i}: {line}" for p, i, line in hits) if hits else "(no matches)"
        owners = sorted({self.w.owners.get(p, "") for p, _, _ in hits})
        self.w._op(self.actor, "search", "search", ",".join(owners), f"query: {query}\n{out}",
                   {"n": len(hits), "paths": sorted({p for p, _, _ in hits})}, svc)
        return out

    def reply(self, text: str) -> str:
        self.w.replies[self.actor] = text
        self.w._op(self.actor, "reply", "reply", self.actor, text, {"bytes": len(text)}, None)
        return "reply sent"
