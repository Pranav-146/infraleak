# Findings: real LLM agents (qwen2.5:7b-instruct, Kaggle T4, Nov 2026)

The raw data are 720 episodes: 4 domains × 3 channels (fs, SQLite, git) × 4 A-tasks × 3 B-variants × 5 seeds.
Labels were frozen (sha256) and `verify` passes on a second machine. There were 0 run errors and a
6.1% malformed-action rate, and malformed actions were recovered by retry. Every number below is reproducible with
`python -m infraleak.cli analyze --data <data>` (see `analysis.md` / `analysis.json`).

## 1. An explicit no-disclosure policy barely stops the leak
| B variant | A wrote secret | B read it | B leaked it |
|---|---|---|---|
| summary task | 83% | 79% | **79%** |
| summary task + "never disclose confidential details" | 84% | 77% | **69%** |
| control (unrelated FAQ task) | 82% | 0% | 0% |

When B reads A's note, it forwards the secret **100%** of the time without the policy and **90%** of the time with it
(166 of 185).

## 2. Under the policy, leaks change shape and get harder to catch with patterns
With the policy, B tends to drop IDs and dollar figures but keeps names and plans (transfer counts):
amount 161→107, code 18→6, codename 188→159, plan 176→140. All 6 paraphrase-only leaks happen under the policy.
In these, B states the unannounced plan ("closing the Krakow ward in Q4") with no identifier at all.
As a result, pattern DLP recall on leaks falls from **0.87 to 0.66**, while token provenance stays at 0.96–1.00.

## 3. Agent A often claims work it never did
In 121 of 720 episodes (17%), A answered "saved at notes/…" without ever calling `write`. These are
labelled negative, and correctly so, because nothing was exposed. It is a separate failure mode worth reporting.

## 4. Honest caveat: on this data, metadata alone looks nearly perfect, and why that is
The cross-agent read alarm scores recall 1.00 with FPR 0.03–0.09 on every test split, even with metadata only. That is
**not** evidence that metadata suffices. With this model, reading A's note almost always leads to a leak,
and most negatives are "easy": B never touched A's file (control: 240, A never wrote: 78, never read: 28).
Only **19 episodes (2.6%)** are hard negatives, where B read the secret and correctly withheld it. The metadata
alarm fires on **all 19 (100% false alarms)**, while content detectors stay silent (0%).
So the realistic population confirms what the designed (scripted) set measures in a controlled way:
metadata cannot tell "read and withheld" from "read and leaked". It also shows that natural hard negatives are rare
with a 7B model. Planned for Phase II: stronger agent models, harder policies and the designed hard negatives as a
targeted test set.

## Label audit
- **Manual:** 30 episodes read in full: 6 policy access-without-leak, 6 no-exposure, 6 verbatim leaks,
  all 6 paraphrase leaks, 6 controls. The oracle label matched human judgement in all 30.
- **Automated (all 365 negatives):** a scan for partial leaks (the secret site name alone, a codename word, the amount
  rounded to whole millions) found **0** missed leaks. Two policy replies mention that restructuring or site closures
  exist without giving any value (for example, "no public documents about specific restructuring costs or site
  closures"). They are kept as negatives under the current definition and flagged as borderline in `analysis.json`.

## Files
`DATASET_CARD.md`, `analysis.md`/`analysis.json`, `baselines.md`/`metrics.csv`, `figures/funnel.png`,
`figures/degradation.png`, `figures/recall_fpr.png`. The raw data (22 MB) is not in git. Keep `llm.zip` as a GitHub
Release asset or in the team drive.
