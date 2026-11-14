"""LLM agent over any OpenAI-compatible /chat/completions endpoint (Ollama, vLLM, llama.cpp server)."""
from __future__ import annotations
import json
import re
import time
import requests

from ..prompts import system_prompt, task_prompt

TOOLS = ("list", "read", "write", "search", "reply")


def extract_action(text: str):
    """Pull the first JSON object with a valid 'tool' out of model text. Returns dict or None."""
    if not text:
        return None
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.S)
    text = re.sub(r"```(?:json)?", "", text)
    start = text.find("{")
    while start != -1:
        depth, instr, esc = 0, False, False
        for i in range(start, len(text)):
            c = text[i]
            if instr:
                if esc:
                    esc = False
                elif c == "\\":
                    esc = True
                elif c == '"':
                    instr = False
            elif c == '"':
                instr = True
            elif c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    try:
                        obj = json.loads(text[start:i + 1])
                    except json.JSONDecodeError:
                        break
                    if isinstance(obj, dict) and obj.get("tool") in TOOLS and isinstance(obj.get("args", {}), dict):
                        obj.setdefault("args", {})
                        return obj
                    break
        start = text.find("{", start + 1)
    return None


class LLMBrain:
    name = "llm"

    def __init__(self, base_url="http://localhost:11434/v1", model="qwen2.5:7b-instruct", api_key="ollama",
                 temperature=0.7, max_tokens=700, max_steps=12, timeout=180, no_think=None, seed=None):
        self.base_url, self.model, self.api_key = base_url.rstrip("/"), model, api_key
        self.temperature, self.max_tokens, self.max_steps, self.timeout = temperature, max_tokens, max_steps, timeout
        self.no_think = ("qwen3" in model.lower()) if no_think is None else no_think
        self.seed = seed
        self.stats = {"steps": 0, "malformed": 0, "calls": 0, "prompt_tokens": 0, "completion_tokens": 0,
                      "seconds": 0.0, "ended_by": {}}

    def chat(self, messages):
        body = {"model": self.model, "messages": messages, "temperature": self.temperature,
                "max_tokens": self.max_tokens}
        if self.seed is not None:
            body["seed"] = self.seed
        t0 = time.time()
        r = requests.post(f"{self.base_url}/chat/completions", json=body, timeout=self.timeout,
                          headers={"Authorization": f"Bearer {self.api_key}"})
        r.raise_for_status()
        j = r.json()
        self.stats["calls"] += 1
        self.stats["seconds"] += time.time() - t0
        u = j.get("usage") or {}
        self.stats["prompt_tokens"] += u.get("prompt_tokens", 0)
        self.stats["completion_tokens"] += u.get("completion_tokens", 0)
        return j["choices"][0]["message"].get("content") or ""

    def run_agent(self, actor, spec, h):
        sys = system_prompt(spec, actor) + ("\n/no_think" if self.no_think else "")
        msgs = [{"role": "system", "content": sys}, {"role": "user", "content": task_prompt(spec, actor)}]
        bad = 0
        for _ in range(self.max_steps):
            out = self.chat(msgs)
            act = extract_action(out)
            msgs.append({"role": "assistant", "content": out})
            if act is None:
                self.stats["malformed"] += 1
                bad += 1
                if bad >= 3:
                    self._end("malformed")
                    return
                msgs.append({"role": "user", "content": "Invalid. Reply with ONE JSON object like "
                             '{"tool": "list", "args": {"prefix": ""}}'})
                continue
            bad = 0
            self.stats["steps"] += 1
            tool, a = act["tool"], act["args"]
            if tool == "reply":
                h.reply(str(a.get("text", "")))
                self._end("reply")
                return
            if tool == "list":
                res = h.list(str(a.get("prefix", "")))
            elif tool == "read":
                res = h.read(str(a.get("path", "")))
            elif tool == "write":
                res = h.write(str(a.get("path", "")), str(a.get("content", "")))
            else:
                res = h.search(str(a.get("query", "")))
            msgs.append({"role": "user", "content": "TOOL RESULT:\n" + res[:4000]})
        self._end("max_steps")

    def _end(self, why):
        self.stats["ended_by"][why] = self.stats["ended_by"].get(why, 0) + 1
