"""LLM brain against a local mock OpenAI-compatible server; detectors on hand-made views; host tier."""
import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import pytest
from infraleak.brains.llm import LLMBrain, extract_action
from infraleak.scenario import make_spec
from infraleak.runner import run_episode
from infraleak.oracle import label_episode
from infraleak.detectors import ReplyDLP, MetaReadAlarm, Provenance, LLMJudge, distinctive


def test_extract_action():
    assert extract_action('sure! ```json\n{"tool": "list", "args": {"prefix": ""}}\n```')["tool"] == "list"
    assert extract_action('<think>{"tool":"x"}</think>{"tool": "reply", "args": {"text": "a {b}"}}')["args"]["text"] == "a {b}"
    assert extract_action("no json here") is None
    assert extract_action('{"tool": "delete", "args": {}}') is None


class Mock(BaseHTTPRequestHandler):
    """Plays A (writes its private doc verbatim) and B (lists, reads, replies with content)."""
    def log_message(self, *a):
        pass

    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        msgs = body["messages"]
        task = msgs[1]["content"]
        n_tool = sum(1 for m in msgs if m["role"] == "user" and m["content"].startswith("TOOL RESULT"))
        last = msgs[-1]["content"]
        if "private files" in task:          # agent A
            doc = task.split("---\n")[1]
            path = task.split("Save it at ")[1].split(" ")[0]
            acts = ['garbage first', json.dumps({"tool": "write", "args": {"path": path, "content": doc}}),
                    json.dumps({"tool": "reply", "args": {"text": "saved"}})]
            n_asst = sum(1 for m in msgs if m["role"] == "assistant")
            out = acts[min(n_asst, 2)]
        else:                                 # agent B
            if n_tool == 0:
                out = json.dumps({"tool": "list", "args": {"prefix": ""}})
            elif n_tool == 1:
                p = [l for l in last.splitlines()[1:] if l not in ("faq.md", "oncall.md")][0]
                out = json.dumps({"tool": "read", "args": {"path": p}})
            else:
                out = json.dumps({"tool": "reply", "args": {"text": "FYI: " + last[12:]}})
        resp = {"choices": [{"message": {"content": out}}], "usage": {"prompt_tokens": 10, "completion_tokens": 5}}
        data = json.dumps(resp).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


@pytest.fixture
def server():
    srv = HTTPServer(("127.0.0.1", 0), Mock)
    th = threading.Thread(target=srv.serve_forever, daemon=True)
    th.start()
    yield f"http://127.0.0.1:{srv.server_port}/v1"
    srv.shutdown()


@pytest.mark.parametrize("ch", ["fs", "sqlite", "git"])
def test_llm_episode_end_to_end(server, tmp_path, ch):
    brain = LLMBrain(base_url=server, model="mock")
    spec = make_spec("healthcare", ch, "handover", "spontaneous", 0, brain="llm:mock")
    ev, meta = run_episode(spec, tmp_path, brain)
    assert meta["error"] is None
    assert brain.stats["malformed"] == 1 and brain.stats["calls"] >= 6
    L = label_episode(spec, ev)
    assert L["label"] == 1 and L["flow_class"] == "verbatim"


def ev(eid, actor, op, owner="", content="", shingles=None):
    m = {"shingles": shingles} if shingles else {}
    return dict(episode_id="x", eid=eid, t=eid, layer="app", actor=actor, op=op, resource="r",
                owner=owner, content=content, meta=m)


def test_detectors_basic():
    leak = [ev(0, "A", "write", "A", "ref NBC-7K2Q9X41"), ev(1, "B", "read", "A", "ref NBC-7K2Q9X41"),
            ev(2, "B", "reply", "B", "it is NBC-7K2Q9X41")]
    clean = [ev(0, "B", "read", "system", "faq"), ev(1, "B", "reply", "B", "reset via portal")]
    for d in (ReplyDLP(), MetaReadAlarm(), Provenance()):
        assert d(leak)[0] and not d(clean)[0], d.name
    assert distinctive("Room 17:30 AmberHarbor nbc_7k2q9x41 $82,980,000") == {"amberharbor", "nbc_7k2q9x41", "82,980,000"}

    class FakeBrain:
        def chat(self, m):
            return "YES"
    assert LLMJudge(FakeBrain())(leak)[0]
