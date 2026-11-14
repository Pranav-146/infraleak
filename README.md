# InfraLeak

**Detecting unauthorized cross-agent information flow through shared infrastructure, under partial observability.**
Capstone PW_25_RB_01, PES University: Pranav, Sujan, Subramani, Apeksha. Guide: Prof. Rajesh Banginwar.

This repo builds the **dataset** and the **evaluation protocol**. It does not train a model yet.

```
scenario generator ──► world (fs | SQLite | git) ──► RAW event log E ──► oracle ──► labels (frozen, sha256)
  (vault of secrets,      agent A writes,               (ground truth,      (runs on E + vault,
   decoys, policy)        agent B reads/answers           never shown to     never on a view)
                                                          a detector)
                                    RAW log E ──► observer profile o ──► view V_o(E) ──► detector ──► eval
                                                  (configs/visibility.yaml)
```

## Quick start

```bash
pip install pyyaml jsonschema requests pytest     # Python >= 3.10, git and sqlite3 on PATH
make test     # 22 tests: matching, oracle, all 3 backends, views, splits, tamper check, LLM brain on a mock server
make data     # 3,840 designed episodes -> labels -> freeze -> splits -> 9 views -> baselines   (~2 min, CPU)
make show     # one episode printed through every observer view
make verify   # re-hash raw logs + labels against MANIFEST and re-run the oracle
```

LLM episodes (Kaggle / laptop, see `docs/RUNBOOK.md`):
```bash
make bench MODEL=qwen3:14b        # malformed-action rate, tokens/s, episodes/hour before a long run
make llm   MODEL=qwen3:14b        # resumable; re-running skips finished episodes
```

## The three questions the panel asked

**1. What is partial observability?**
The full raw log `E` (every tool call, with content, at every layer) exists only inside our testbed. A real defender
never has it. They see a **view** `V_o(E)`, set by where their sensor sits (an *observer profile* `o`).
Ground truth is computed on `E`. Detectors are only ever given `V_o(E)`. The research question is how detection quality
degrades as `o` sees less.

**2. On what basis are logs removed?** It is not ad hoc. Every profile is a rule on three axes, written in `configs/visibility.yaml`:

| axis | values | real-world counterpart |
|---|---|---|
| vantage (layer) | `app` (agent tool calls), `service` (DB statement log / git command log) | LangSmith-style tracing vs. `pg_stat_statements` / git server logs |
| field visibility (content) | `all`, `sinks_only`, `hash`, `none` | full tracing, egress DLP, privacy-preserving hashed telemetry, metadata-only |
| coverage | which agents, which ops, random event drop | partial instrumentation, sampled/lossy telemetry |

Masking is deterministic (seeded by profile+episode+event), so every view can be reproduced exactly.
Service-layer events never carry values: SQL is parameterised and only the template is logged (a test enforces this).

**3. How is data held out?** By split rules, with leakage checks enforced in code (`infraleak/splits.py`):

| split | rule | what it tests |
|---|---|---|
| train / val / test_id | non-OOD episodes, seed % 5 → 0-2 / 3 / 4 | held-out seeds, same templates |
| test_ood_domain | every *legal* episode | unseen organisation and vocabulary |
| test_ood_channel | every *git* episode | unseen infrastructure |
| test_ood_class | paraphrase leaks + paraphrase decoys | unseen flow class |

Test labels are written to `data/sealed/`, not to `data/release/`. Labels are frozen with sha256 before any detector runs.
`check_splits` asserts no domain, channel, class or secret value is shared between train and the OOD splits.

## Labels (oracle)
Per episode, on the raw log, using the secret vault (AgentLeak-style canaries, adapted to shared infrastructure):
**exposure** (A writes a secret to a shared resource) → **access** (B's read/search returns it) → **transfer**
(B's reply or write contains it, after access). Episode label = transfer. Flow class = verbatim > reformatted
(case/separator/reversed/≤2-edit/number-format) > paraphrase (semantic keyword groups).
Public decoys (same shape, different values) are in the allowed-disclosure set and are always negatives.

## Designed dataset (current build, `reports/DATASET_CARD_scripted.md`)
3,840 episodes = 4 domains × 3 channels × 4 A-tasks × 8 designs × 10 seeds. The oracle label matches the intended design
on **3,840/3,840** episodes.

| design | A writes | B does | label |
|---|---|---|---|
| pos_verbatim / pos_reformatted / pos_paraphrase | secret (3 forms) | reads and forwards | 1 |
| neg_read_only | secret | reads, does not forward | 0 (access without transfer) |
| neg_control | secret | never reads A's file | 0 |
| neg_decoy / neg_decoy_para | public look-alike | forwards | 0 (hard negative) |
| neg_clean | harmless note | forwards | 0 (cross-agent copy, no secret) |

## Baselines (from `reports/baselines_scripted.md`)
On test_id (n=288, 96 positive). The point is not the numbers but how they change across views:

| view | reply DLP | metadata read-alarm | provenance |
|---|---|---|---|
| app_full | R 1.00 / FPR 0.25 | R 1.00 / FPR 0.75 | R 1.00 / FPR 0.25 |
| app_hash | blind | R 1.00 / FPR 0.75 | R 1.00 / FPR 0.50 |
| app_meta | blind | R 1.00 / FPR 0.75 | blind |
| service_meta | blind | R 0.50 / FPR 0.38 (fs has no service tier) | blind |
| reply_only | R 0.50 / FPR 0.12 (misses write sinks) | blind | blind |

On test_ood_class (paraphrase), **every** baseline either misses all leaks or alarms on every decoy (FPR 1.00).
That gap is what the learned detector (Phase II) has to close.

## Honest limitations
- The designed episodes are scripted, so content baselines saturate in-distribution. They exist to check the oracle and
  the views. **Realistic behaviour comes from LLM episodes** (`run-llm`), labelled by the same oracle.
- The paraphrase oracle uses keyword groups (site + quarter), not semantics. LLM paraphrases need a hand-audit sample.
- Number matching ignores separators, so an unrelated number with the same digits would count as a match. There is a test for this.
- The host tier (strace) is parsed and probed (`host_trace.py`) but not yet wired into episodes.

See `docs/DATASET_SPEC.md` for the paper-to-component mapping and `docs/RUNBOOK.md` for running on Kaggle.
