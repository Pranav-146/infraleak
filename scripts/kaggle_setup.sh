#!/usr/bin/env bash
# Kaggle notebook (GPU T4 x2 or P100, Internet ON). Run in a cell with:  !bash scripts/kaggle_setup.sh qwen3:14b
set -euo pipefail
MODEL="${1:-qwen2.5:7b-instruct}"
nvidia-smi || { echo "No GPU: enable an accelerator in notebook settings"; exit 1; }
command -v ollama >/dev/null || curl -fsSL https://ollama.com/install.sh | sh
export OLLAMA_CONTEXT_LENGTH=8192
nohup ollama serve > /kaggle/working/ollama.log 2>&1 &
sleep 8
ollama pull "$MODEL"
pip install -q pyyaml jsonschema requests pytest
python -m pytest -q
python -m infraleak.cli bench --model "$MODEL" --n 20
echo "Now run: python -m infraleak.cli run-llm --data /kaggle/working/data/llm --model $MODEL --seeds 5"
