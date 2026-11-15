# Dataset card (auto-generated)

Episodes: 720  
Positives (oracle transfer): 355  
Oracle version: 1.0.0

## Splits

| split | episodes | positives | flow classes |
|---|---|---|---|
| train | 216 | 103 | {'verbatim': 102, 'none': 113, 'paraphrase': 1} |
| val | 72 | 32 | {'none': 40, 'verbatim': 32} |
| test_id | 72 | 33 | {'none': 39, 'verbatim': 32, 'paraphrase': 1} |
| test_ood_domain | 180 | 100 | {'none': 80, 'verbatim': 99, 'paraphrase': 1} |
| test_ood_channel | 180 | 87 | {'none': 93, 'verbatim': 84, 'paraphrase': 3} |
| test_ood_class | 0 | 0 | {} |

## Design vs oracle label

| design | oracle flow class | episodes |
|---|---|---|
| spontaneous | none | 51 |
| spontaneous | verbatim | 189 |
| spontaneous_control | none | 240 |
| spontaneous_policy | none | 74 |
| spontaneous_policy | paraphrase | 6 |
| spontaneous_policy | verbatim | 160 |

## Stage counts

- exposure: 599
- access: 374
- transfer: 355

## Observer profiles

| profile | layers | content | actors | ops | drop | note |
|---|---|---|---|---|---|---|
| full_ref | app,service,host | all | A,B | all | 0.0 | reference only - not a deployable observer |
| app_full | app | all | A,B | all | 0.0 | agent-framework tracing with payloads |
| app_sinks | app | sinks_only | A,B | all | 0.0 | egress-style capture: outputs visible, read results not |
| app_hash | app | hash | A,B | all | 0.0 | privacy-preserving tracing: hashed shingles |
| app_meta | app | none | A,B | all | 0.0 | who/what/when/where only |
| service_meta | service | none | A,B | all | 0.0 | DB statement log / git command log; fs has no service tier |
| b_only | app | all | B | all | 0.0 | only agent B is instrumented |
| reply_only | app | all | B | reply | 0.0 | classic output DLP |
| app_meta_drop50 | app | none | A,B | all | 0.5 | lossy telemetry, 50% events dropped (seeded) |
