# Dataset card (auto-generated)

Episodes: 3840  
Positives (oracle transfer): 1440  
Oracle version: 1.0.0

## Splits

| split | episodes | positives | flow classes |
|---|---|---|---|
| train | 864 | 288 | {'none': 576, 'verbatim': 144, 'reformatted': 144} |
| val | 288 | 96 | {'reformatted': 48, 'none': 192, 'verbatim': 48} |
| test_id | 288 | 96 | {'verbatim': 48, 'none': 192, 'reformatted': 48} |
| test_ood_domain | 960 | 360 | {'reformatted': 120, 'none': 600, 'paraphrase': 120, 'verbatim': 120} |
| test_ood_channel | 960 | 360 | {'none': 600, 'paraphrase': 120, 'verbatim': 120, 'reformatted': 120} |
| test_ood_class | 480 | 240 | {'none': 240, 'paraphrase': 240} |

## Design vs oracle label

| design | oracle flow class | episodes |
|---|---|---|
| neg_clean | none | 480 |
| neg_control | none | 480 |
| neg_decoy | none | 480 |
| neg_decoy_para | none | 480 |
| neg_read_only | none | 480 |
| pos_paraphrase | paraphrase | 480 |
| pos_reformatted | reformatted | 480 |
| pos_verbatim | verbatim | 480 |

## Stage counts

- exposure: 2400
- access: 1920
- transfer: 1440

## Observer profiles

| profile | layers | content | actors | ops | drop | note |
|---|---|---|---|---|---|---|
| full_ref | app,service | all | A,B | all | 0.0 | reference only - not a deployable observer |
| app_full | app | all | A,B | all | 0.0 | agent-framework tracing with payloads |
| app_sinks | app | sinks_only | A,B | all | 0.0 | egress-style capture: outputs visible, read results not |
| app_hash | app | hash | A,B | all | 0.0 | privacy-preserving tracing: hashed shingles |
| app_meta | app | none | A,B | all | 0.0 | who/what/when/where only |
| service_meta | service | none | A,B | all | 0.0 | DB statement log / git command log; fs has no service tier |
| b_only | app | all | B | all | 0.0 | only agent B is instrumented |
| reply_only | app | all | B | reply | 0.0 | classic output DLP |
| app_meta_drop50 | app | none | A,B | all | 0.5 | lossy telemetry, 50% events dropped (seeded) |
