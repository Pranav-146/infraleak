# Baseline results (episode level)

Recall/FPR with Wilson 95% CI. Detectors only ever see the observer view, never labels.


## test_id  (n=72, positives=33)

| profile | detector | precision | recall [95% CI] | FPR [95% CI] | F1 | recall by class |
|---|---|---|---|---|---|---|
| full_ref | reply_dlp | 1.00 | 0.76 [0.59-0.87] | 0.00 [0.00-0.09] | 0.86 | para 0.00, verb 0.78 |
| full_ref | meta_read_alarm | 0.97 | 1.00 [0.90-1.00] | 0.03 [0.00-0.13] | 0.99 | para 1.00, verb 1.00 |
| full_ref | provenance | 1.00 | 0.97 [0.85-0.99] | 0.00 [0.00-0.09] | 0.98 | para 0.00, verb 1.00 |
| app_full | reply_dlp | 1.00 | 0.76 [0.59-0.87] | 0.00 [0.00-0.09] | 0.86 | para 0.00, verb 0.78 |
| app_full | meta_read_alarm | 0.97 | 1.00 [0.90-1.00] | 0.03 [0.00-0.13] | 0.99 | para 1.00, verb 1.00 |
| app_full | provenance | 1.00 | 0.97 [0.85-0.99] | 0.00 [0.00-0.09] | 0.98 | para 0.00, verb 1.00 |
| app_sinks | reply_dlp | 1.00 | 0.76 [0.59-0.87] | 0.00 [0.00-0.09] | 0.86 | para 0.00, verb 0.78 |
| app_sinks | meta_read_alarm | 0.97 | 1.00 [0.90-1.00] | 0.03 [0.00-0.13] | 0.99 | para 1.00, verb 1.00 |
| app_sinks | provenance | 0.00 | 0.00 [0.00-0.10] | 0.00 [0.00-0.09] | 0.00 | para 0.00, verb 0.00 |
| app_hash | reply_dlp | 0.00 | 0.00 [0.00-0.10] | 0.00 [0.00-0.09] | 0.00 | para 0.00, verb 0.00 |
| app_hash | meta_read_alarm | 0.97 | 1.00 [0.90-1.00] | 0.03 [0.00-0.13] | 0.99 | para 1.00, verb 1.00 |
| app_hash | provenance | 1.00 | 0.97 [0.85-0.99] | 0.00 [0.00-0.09] | 0.98 | para 1.00, verb 0.97 |
| app_meta | reply_dlp | 0.00 | 0.00 [0.00-0.10] | 0.00 [0.00-0.09] | 0.00 | para 0.00, verb 0.00 |
| app_meta | meta_read_alarm | 0.97 | 1.00 [0.90-1.00] | 0.03 [0.00-0.13] | 0.99 | para 1.00, verb 1.00 |
| app_meta | provenance | 0.00 | 0.00 [0.00-0.10] | 0.00 [0.00-0.09] | 0.00 | para 0.00, verb 0.00 |
| service_meta | reply_dlp | 0.00 | 0.00 [0.00-0.10] | 0.00 [0.00-0.09] | 0.00 | para 0.00, verb 0.00 |
| service_meta | meta_read_alarm | 1.00 | 0.48 [0.33-0.65] | 0.00 [0.00-0.09] | 0.65 | para 1.00, verb 0.47 |
| service_meta | provenance | 0.00 | 0.00 [0.00-0.10] | 0.00 [0.00-0.09] | 0.00 | para 0.00, verb 0.00 |
| b_only | reply_dlp | 1.00 | 0.76 [0.59-0.87] | 0.00 [0.00-0.09] | 0.86 | para 0.00, verb 0.78 |
| b_only | meta_read_alarm | 0.97 | 1.00 [0.90-1.00] | 0.03 [0.00-0.13] | 0.99 | para 1.00, verb 1.00 |
| b_only | provenance | 1.00 | 0.97 [0.85-0.99] | 0.00 [0.00-0.09] | 0.98 | para 0.00, verb 1.00 |
| reply_only | reply_dlp | 1.00 | 0.76 [0.59-0.87] | 0.00 [0.00-0.09] | 0.86 | para 0.00, verb 0.78 |
| reply_only | meta_read_alarm | 0.00 | 0.00 [0.00-0.10] | 0.00 [0.00-0.09] | 0.00 | para 0.00, verb 0.00 |
| reply_only | provenance | 0.00 | 0.00 [0.00-0.10] | 0.00 [0.00-0.09] | 0.00 | para 0.00, verb 0.00 |
| app_meta_drop50 | reply_dlp | 0.00 | 0.00 [0.00-0.10] | 0.00 [0.00-0.09] | 0.00 | para 0.00, verb 0.00 |
| app_meta_drop50 | meta_read_alarm | 0.94 | 0.48 [0.33-0.65] | 0.03 [0.00-0.13] | 0.64 | para 1.00, verb 0.47 |
| app_meta_drop50 | provenance | 0.00 | 0.00 [0.00-0.10] | 0.00 [0.00-0.09] | 0.00 | para 0.00, verb 0.00 |

## test_ood_domain  (n=180, positives=100)

| profile | detector | precision | recall [95% CI] | FPR [95% CI] | F1 | recall by class |
|---|---|---|---|---|---|---|
| full_ref | reply_dlp | 1.00 | 0.87 [0.79-0.92] | 0.00 [0.00-0.05] | 0.93 | para 0.00, verb 0.88 |
| full_ref | meta_read_alarm | 0.96 | 1.00 [0.96-1.00] | 0.05 [0.02-0.12] | 0.98 | para 1.00, verb 1.00 |
| full_ref | provenance | 1.00 | 0.99 [0.95-1.00] | 0.00 [0.00-0.05] | 0.99 | para 0.00, verb 1.00 |
| app_full | reply_dlp | 1.00 | 0.87 [0.79-0.92] | 0.00 [0.00-0.05] | 0.93 | para 0.00, verb 0.88 |
| app_full | meta_read_alarm | 0.96 | 1.00 [0.96-1.00] | 0.05 [0.02-0.12] | 0.98 | para 1.00, verb 1.00 |
| app_full | provenance | 1.00 | 0.99 [0.95-1.00] | 0.00 [0.00-0.05] | 0.99 | para 0.00, verb 1.00 |
| app_sinks | reply_dlp | 1.00 | 0.87 [0.79-0.92] | 0.00 [0.00-0.05] | 0.93 | para 0.00, verb 0.88 |
| app_sinks | meta_read_alarm | 0.96 | 1.00 [0.96-1.00] | 0.05 [0.02-0.12] | 0.98 | para 1.00, verb 1.00 |
| app_sinks | provenance | 0.00 | 0.00 [0.00-0.04] | 0.00 [0.00-0.05] | 0.00 | para 0.00, verb 0.00 |
| app_hash | reply_dlp | 0.00 | 0.00 [0.00-0.04] | 0.00 [0.00-0.05] | 0.00 | para 0.00, verb 0.00 |
| app_hash | meta_read_alarm | 0.96 | 1.00 [0.96-1.00] | 0.05 [0.02-0.12] | 0.98 | para 1.00, verb 1.00 |
| app_hash | provenance | 0.99 | 0.96 [0.90-0.98] | 0.01 [0.00-0.07] | 0.97 | para 1.00, verb 0.96 |
| app_meta | reply_dlp | 0.00 | 0.00 [0.00-0.04] | 0.00 [0.00-0.05] | 0.00 | para 0.00, verb 0.00 |
| app_meta | meta_read_alarm | 0.96 | 1.00 [0.96-1.00] | 0.05 [0.02-0.12] | 0.98 | para 1.00, verb 1.00 |
| app_meta | provenance | 0.00 | 0.00 [0.00-0.04] | 0.00 [0.00-0.05] | 0.00 | para 0.00, verb 0.00 |
| service_meta | reply_dlp | 0.00 | 0.00 [0.00-0.04] | 0.00 [0.00-0.05] | 0.00 | para 0.00, verb 0.00 |
| service_meta | meta_read_alarm | 0.99 | 0.70 [0.60-0.78] | 0.01 [0.00-0.07] | 0.82 | para 0.00, verb 0.71 |
| service_meta | provenance | 0.00 | 0.00 [0.00-0.04] | 0.00 [0.00-0.05] | 0.00 | para 0.00, verb 0.00 |
| b_only | reply_dlp | 1.00 | 0.87 [0.79-0.92] | 0.00 [0.00-0.05] | 0.93 | para 0.00, verb 0.88 |
| b_only | meta_read_alarm | 0.96 | 1.00 [0.96-1.00] | 0.05 [0.02-0.12] | 0.98 | para 1.00, verb 1.00 |
| b_only | provenance | 1.00 | 0.99 [0.95-1.00] | 0.00 [0.00-0.05] | 0.99 | para 0.00, verb 1.00 |
| reply_only | reply_dlp | 1.00 | 0.87 [0.79-0.92] | 0.00 [0.00-0.05] | 0.93 | para 0.00, verb 0.88 |
| reply_only | meta_read_alarm | 0.00 | 0.00 [0.00-0.04] | 0.00 [0.00-0.05] | 0.00 | para 0.00, verb 0.00 |
| reply_only | provenance | 0.00 | 0.00 [0.00-0.04] | 0.00 [0.00-0.05] | 0.00 | para 0.00, verb 0.00 |
| app_meta_drop50 | reply_dlp | 0.00 | 0.00 [0.00-0.04] | 0.00 [0.00-0.05] | 0.00 | para 0.00, verb 0.00 |
| app_meta_drop50 | meta_read_alarm | 0.96 | 0.45 [0.36-0.55] | 0.03 [0.01-0.09] | 0.61 | para 1.00, verb 0.44 |
| app_meta_drop50 | provenance | 0.00 | 0.00 [0.00-0.04] | 0.00 [0.00-0.05] | 0.00 | para 0.00, verb 0.00 |

## test_ood_channel  (n=180, positives=87)

| profile | detector | precision | recall [95% CI] | FPR [95% CI] | F1 | recall by class |
|---|---|---|---|---|---|---|
| full_ref | reply_dlp | 1.00 | 0.74 [0.63-0.82] | 0.00 [0.00-0.04] | 0.85 | para 0.00, verb 0.76 |
| full_ref | meta_read_alarm | 0.92 | 1.00 [0.96-1.00] | 0.09 [0.04-0.16] | 0.96 | para 1.00, verb 1.00 |
| full_ref | provenance | 1.00 | 0.97 [0.90-0.99] | 0.00 [0.00-0.04] | 0.98 | para 0.00, verb 1.00 |
| app_full | reply_dlp | 1.00 | 0.74 [0.63-0.82] | 0.00 [0.00-0.04] | 0.85 | para 0.00, verb 0.76 |
| app_full | meta_read_alarm | 0.92 | 1.00 [0.96-1.00] | 0.09 [0.04-0.16] | 0.96 | para 1.00, verb 1.00 |
| app_full | provenance | 1.00 | 0.97 [0.90-0.99] | 0.00 [0.00-0.04] | 0.98 | para 0.00, verb 1.00 |
| app_sinks | reply_dlp | 1.00 | 0.74 [0.63-0.82] | 0.00 [0.00-0.04] | 0.85 | para 0.00, verb 0.76 |
| app_sinks | meta_read_alarm | 0.92 | 1.00 [0.96-1.00] | 0.09 [0.04-0.16] | 0.96 | para 1.00, verb 1.00 |
| app_sinks | provenance | 0.00 | 0.00 [0.00-0.04] | 0.00 [0.00-0.04] | 0.00 | para 0.00, verb 0.00 |
| app_hash | reply_dlp | 0.00 | 0.00 [0.00-0.04] | 0.00 [0.00-0.04] | 0.00 | para 0.00, verb 0.00 |
| app_hash | meta_read_alarm | 0.92 | 1.00 [0.96-1.00] | 0.09 [0.04-0.16] | 0.96 | para 1.00, verb 1.00 |
| app_hash | provenance | 1.00 | 0.92 [0.84-0.96] | 0.00 [0.00-0.04] | 0.96 | para 1.00, verb 0.92 |
| app_meta | reply_dlp | 0.00 | 0.00 [0.00-0.04] | 0.00 [0.00-0.04] | 0.00 | para 0.00, verb 0.00 |
| app_meta | meta_read_alarm | 0.92 | 1.00 [0.96-1.00] | 0.09 [0.04-0.16] | 0.96 | para 1.00, verb 1.00 |
| app_meta | provenance | 0.00 | 0.00 [0.00-0.04] | 0.00 [0.00-0.04] | 0.00 | para 0.00, verb 0.00 |
| service_meta | reply_dlp | 0.00 | 0.00 [0.00-0.04] | 0.00 [0.00-0.04] | 0.00 | para 0.00, verb 0.00 |
| service_meta | meta_read_alarm | 0.92 | 1.00 [0.96-1.00] | 0.09 [0.04-0.16] | 0.96 | para 1.00, verb 1.00 |
| service_meta | provenance | 0.00 | 0.00 [0.00-0.04] | 0.00 [0.00-0.04] | 0.00 | para 0.00, verb 0.00 |
| b_only | reply_dlp | 1.00 | 0.74 [0.63-0.82] | 0.00 [0.00-0.04] | 0.85 | para 0.00, verb 0.76 |
| b_only | meta_read_alarm | 0.92 | 1.00 [0.96-1.00] | 0.09 [0.04-0.16] | 0.96 | para 1.00, verb 1.00 |
| b_only | provenance | 1.00 | 0.97 [0.90-0.99] | 0.00 [0.00-0.04] | 0.98 | para 0.00, verb 1.00 |
| reply_only | reply_dlp | 1.00 | 0.74 [0.63-0.82] | 0.00 [0.00-0.04] | 0.85 | para 0.00, verb 0.76 |
| reply_only | meta_read_alarm | 0.00 | 0.00 [0.00-0.04] | 0.00 [0.00-0.04] | 0.00 | para 0.00, verb 0.00 |
| reply_only | provenance | 0.00 | 0.00 [0.00-0.04] | 0.00 [0.00-0.04] | 0.00 | para 0.00, verb 0.00 |
| app_meta_drop50 | reply_dlp | 0.00 | 0.00 [0.00-0.04] | 0.00 [0.00-0.04] | 0.00 | para 0.00, verb 0.00 |
| app_meta_drop50 | meta_read_alarm | 0.86 | 0.49 [0.39-0.60] | 0.08 [0.04-0.15] | 0.63 | para 0.67, verb 0.49 |
| app_meta_drop50 | provenance | 0.00 | 0.00 [0.00-0.04] | 0.00 [0.00-0.04] | 0.00 | para 0.00, verb 0.00 |

## val  (n=72, positives=32)

| profile | detector | precision | recall [95% CI] | FPR [95% CI] | F1 | recall by class |
|---|---|---|---|---|---|---|
| full_ref | reply_dlp | 1.00 | 0.75 [0.58-0.87] | 0.00 [0.00-0.09] | 0.86 | verb 0.75 |
| full_ref | meta_read_alarm | 0.91 | 1.00 [0.89-1.00] | 0.07 [0.03-0.20] | 0.96 | verb 1.00 |
| full_ref | provenance | 1.00 | 1.00 [0.89-1.00] | 0.00 [0.00-0.09] | 1.00 | verb 1.00 |
| app_full | reply_dlp | 1.00 | 0.75 [0.58-0.87] | 0.00 [0.00-0.09] | 0.86 | verb 0.75 |
| app_full | meta_read_alarm | 0.91 | 1.00 [0.89-1.00] | 0.07 [0.03-0.20] | 0.96 | verb 1.00 |
| app_full | provenance | 1.00 | 1.00 [0.89-1.00] | 0.00 [0.00-0.09] | 1.00 | verb 1.00 |
| app_sinks | reply_dlp | 1.00 | 0.75 [0.58-0.87] | 0.00 [0.00-0.09] | 0.86 | verb 0.75 |
| app_sinks | meta_read_alarm | 0.91 | 1.00 [0.89-1.00] | 0.07 [0.03-0.20] | 0.96 | verb 1.00 |
| app_sinks | provenance | 0.00 | 0.00 [0.00-0.11] | 0.00 [0.00-0.09] | 0.00 | verb 0.00 |
| app_hash | reply_dlp | 0.00 | 0.00 [0.00-0.11] | 0.00 [0.00-0.09] | 0.00 | verb 0.00 |
| app_hash | meta_read_alarm | 0.91 | 1.00 [0.89-1.00] | 0.07 [0.03-0.20] | 0.96 | verb 1.00 |
| app_hash | provenance | 1.00 | 1.00 [0.89-1.00] | 0.00 [0.00-0.09] | 1.00 | verb 1.00 |
| app_meta | reply_dlp | 0.00 | 0.00 [0.00-0.11] | 0.00 [0.00-0.09] | 0.00 | verb 0.00 |
| app_meta | meta_read_alarm | 0.91 | 1.00 [0.89-1.00] | 0.07 [0.03-0.20] | 0.96 | verb 1.00 |
| app_meta | provenance | 0.00 | 0.00 [0.00-0.11] | 0.00 [0.00-0.09] | 0.00 | verb 0.00 |
| service_meta | reply_dlp | 0.00 | 0.00 [0.00-0.11] | 0.00 [0.00-0.09] | 0.00 | verb 0.00 |
| service_meta | meta_read_alarm | 0.82 | 0.44 [0.28-0.61] | 0.07 [0.03-0.20] | 0.57 | verb 0.44 |
| service_meta | provenance | 0.00 | 0.00 [0.00-0.11] | 0.00 [0.00-0.09] | 0.00 | verb 0.00 |
| b_only | reply_dlp | 1.00 | 0.75 [0.58-0.87] | 0.00 [0.00-0.09] | 0.86 | verb 0.75 |
| b_only | meta_read_alarm | 0.91 | 1.00 [0.89-1.00] | 0.07 [0.03-0.20] | 0.96 | verb 1.00 |
| b_only | provenance | 1.00 | 1.00 [0.89-1.00] | 0.00 [0.00-0.09] | 1.00 | verb 1.00 |
| reply_only | reply_dlp | 1.00 | 0.75 [0.58-0.87] | 0.00 [0.00-0.09] | 0.86 | verb 0.75 |
| reply_only | meta_read_alarm | 0.00 | 0.00 [0.00-0.11] | 0.00 [0.00-0.09] | 0.00 | verb 0.00 |
| reply_only | provenance | 0.00 | 0.00 [0.00-0.11] | 0.00 [0.00-0.09] | 0.00 | verb 0.00 |
| app_meta_drop50 | reply_dlp | 0.00 | 0.00 [0.00-0.11] | 0.00 [0.00-0.09] | 0.00 | verb 0.00 |
| app_meta_drop50 | meta_read_alarm | 0.95 | 0.62 [0.45-0.77] | 0.03 [0.00-0.13] | 0.75 | verb 0.62 |
| app_meta_drop50 | provenance | 0.00 | 0.00 [0.00-0.11] | 0.00 [0.00-0.09] | 0.00 | verb 0.00 |
