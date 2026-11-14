PY ?= python
SEEDS ?= 10
MODEL ?= qwen2.5:7b-instruct
BASE_URL ?= http://localhost:11434/v1

test:
	$(PY) -m pytest -q

data:            ## designed (scripted) dataset: generate, label, freeze, split, views, baselines, figures (~2 min)
	$(PY) -m infraleak.cli build --data data/scripted --seeds $(SEEDS)

data-host:       ## same, plus the host tier recorded with strace (Linux/WSL, ~9 min)
	$(PY) -m infraleak.cli build --data data/scripted --seeds $(SEEDS) --host-trace

report:          ## redraw figures from results/metrics.csv
	$(PY) -m infraleak.cli report --data data/scripted

show:            ## one episode through every observer view
	$(PY) -m infraleak.cli show --data data/scripted --design pos_reformatted --channel sqlite

verify:
	$(PY) -m infraleak.cli verify --data data/scripted

bench:           ## 20-episode model benchmark (needs an OpenAI-compatible server, e.g. Ollama)
	$(PY) -m infraleak.cli bench --model $(MODEL) --base-url $(BASE_URL) --n 20

llm:             ## spontaneous LLM episodes (resumable)
	$(PY) -m infraleak.cli run-llm --data data/llm --model $(MODEL) --base-url $(BASE_URL) --seeds 5

.PHONY: test data data-host report show verify bench llm
