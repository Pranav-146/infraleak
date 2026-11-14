# Runbook

## Local (any OS with Python 3.10+, git)
```bash
pip install pyyaml jsonschema requests pytest
make test && make data && make show
```

## LLM episodes on Kaggle (free GPU)
1. New notebook → Settings: Accelerator **GPU T4 x2** (or P100), Internet **On**.
2. Cell: `!git clone https://github.com/<owner>/infraleak && cd infraleak && bash scripts/kaggle_setup.sh qwen3:14b`
3. Read the bench output. Proceed if malformed_rate < 0.15 and errors = 0.
4. Cell: `!cd infraleak && python -m infraleak.cli run-llm --data /kaggle/working/data/llm --model qwen3:14b --seeds 5`
   This gives 4 domains × 3 channels × 4 tasks × 5 seeds = 240 episodes. It is resumable, so after a session timeout
   just run the same cell again.
5. Download `/kaggle/working/data/llm` (Output tab), or zip it.

Model notes: `qwen2.5:7b-instruct` for dev and continuity with the earlier pilot; `qwen3:14b` as the main agent model
(thinking is disabled automatically through `/no_think`); `gpt-oss:20b` as a second family and as the judge.
Set `OLLAMA_CONTEXT_LENGTH=8192`, because Ollama's default context truncates long tool histories.

## Any OpenAI-compatible server
`--base-url http://host:port/v1 --model <name> --api-key <key>` works with vLLM, llama.cpp server, LM Studio and Ollama.
