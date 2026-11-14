# Baseline results (episode level)

Recall/FPR with Wilson 95% CI. Detectors only ever see the observer view, never labels.


## test_id  (n=288, positives=96)

| profile | detector | precision | recall [95% CI] | FPR [95% CI] | F1 | recall by class |
|---|---|---|---|---|---|---|
| full_ref | reply_dlp | 0.67 | 1.00 [0.96-1.00] | 0.25 [0.19-0.32] | 0.80 | refo 1.00, verb 1.00 |
| full_ref | meta_read_alarm | 0.36 | 1.00 [0.96-1.00] | 0.88 [0.82-0.91] | 0.53 | refo 1.00, verb 1.00 |
| full_ref | provenance | 0.67 | 1.00 [0.96-1.00] | 0.25 [0.19-0.32] | 0.80 | refo 1.00, verb 1.00 |
| app_full | reply_dlp | 0.67 | 1.00 [0.96-1.00] | 0.25 [0.19-0.32] | 0.80 | refo 1.00, verb 1.00 |
| app_full | meta_read_alarm | 0.40 | 1.00 [0.96-1.00] | 0.75 [0.68-0.81] | 0.57 | refo 1.00, verb 1.00 |
| app_full | provenance | 0.67 | 1.00 [0.96-1.00] | 0.25 [0.19-0.32] | 0.80 | refo 1.00, verb 1.00 |
| app_sinks | reply_dlp | 0.67 | 1.00 [0.96-1.00] | 0.25 [0.19-0.32] | 0.80 | refo 1.00, verb 1.00 |
| app_sinks | meta_read_alarm | 0.40 | 1.00 [0.96-1.00] | 0.75 [0.68-0.81] | 0.57 | refo 1.00, verb 1.00 |
| app_sinks | provenance | 0.00 | 0.00 [0.00-0.04] | 0.00 [0.00-0.02] | 0.00 | refo 0.00, verb 0.00 |
| app_hash | reply_dlp | 0.00 | 0.00 [0.00-0.04] | 0.00 [0.00-0.02] | 0.00 | refo 0.00, verb 0.00 |
| app_hash | meta_read_alarm | 0.40 | 1.00 [0.96-1.00] | 0.75 [0.68-0.81] | 0.57 | refo 1.00, verb 1.00 |
| app_hash | provenance | 0.50 | 1.00 [0.96-1.00] | 0.50 [0.43-0.57] | 0.67 | refo 1.00, verb 1.00 |
| app_meta | reply_dlp | 0.00 | 0.00 [0.00-0.04] | 0.00 [0.00-0.02] | 0.00 | refo 0.00, verb 0.00 |
| app_meta | meta_read_alarm | 0.40 | 1.00 [0.96-1.00] | 0.75 [0.68-0.81] | 0.57 | refo 1.00, verb 1.00 |
| app_meta | provenance | 0.00 | 0.00 [0.00-0.04] | 0.00 [0.00-0.02] | 0.00 | refo 0.00, verb 0.00 |
| service_meta | reply_dlp | 0.00 | 0.00 [0.00-0.04] | 0.00 [0.00-0.02] | 0.00 | refo 0.00, verb 0.00 |
| service_meta | meta_read_alarm | 0.40 | 0.50 [0.40-0.60] | 0.38 [0.31-0.45] | 0.44 | refo 0.50, verb 0.50 |
| service_meta | provenance | 0.00 | 0.00 [0.00-0.04] | 0.00 [0.00-0.02] | 0.00 | refo 0.00, verb 0.00 |
| host_meta | reply_dlp | 0.00 | 0.00 [0.00-0.04] | 0.00 [0.00-0.02] | 0.00 | refo 0.00, verb 0.00 |
| host_meta | meta_read_alarm | 0.36 | 1.00 [0.96-1.00] | 0.88 [0.82-0.91] | 0.53 | refo 1.00, verb 1.00 |
| host_meta | provenance | 0.00 | 0.00 [0.00-0.04] | 0.00 [0.00-0.02] | 0.00 | refo 0.00, verb 0.00 |
| b_only | reply_dlp | 0.67 | 1.00 [0.96-1.00] | 0.25 [0.19-0.32] | 0.80 | refo 1.00, verb 1.00 |
| b_only | meta_read_alarm | 0.40 | 1.00 [0.96-1.00] | 0.75 [0.68-0.81] | 0.57 | refo 1.00, verb 1.00 |
| b_only | provenance | 0.67 | 1.00 [0.96-1.00] | 0.25 [0.19-0.32] | 0.80 | refo 1.00, verb 1.00 |
| reply_only | reply_dlp | 0.67 | 0.50 [0.40-0.60] | 0.12 [0.09-0.18] | 0.57 | refo 0.50, verb 0.50 |
| reply_only | meta_read_alarm | 0.00 | 0.00 [0.00-0.04] | 0.00 [0.00-0.02] | 0.00 | refo 0.00, verb 0.00 |
| reply_only | provenance | 0.00 | 0.00 [0.00-0.04] | 0.00 [0.00-0.02] | 0.00 | refo 0.00, verb 0.00 |
| app_meta_drop50 | reply_dlp | 0.00 | 0.00 [0.00-0.04] | 0.00 [0.00-0.02] | 0.00 | refo 0.00, verb 0.00 |
| app_meta_drop50 | meta_read_alarm | 0.44 | 0.58 [0.48-0.68] | 0.37 [0.30-0.44] | 0.50 | refo 0.52, verb 0.65 |
| app_meta_drop50 | provenance | 0.00 | 0.00 [0.00-0.04] | 0.00 [0.00-0.02] | 0.00 | refo 0.00, verb 0.00 |

## test_ood_domain  (n=960, positives=360)

| profile | detector | precision | recall [95% CI] | FPR [95% CI] | F1 | recall by class |
|---|---|---|---|---|---|---|
| full_ref | reply_dlp | 0.67 | 0.67 [0.62-0.71] | 0.20 [0.17-0.23] | 0.67 | para 0.00, refo 1.00, verb 1.00 |
| full_ref | meta_read_alarm | 0.39 | 1.00 [0.99-1.00] | 0.93 [0.91-0.95] | 0.56 | para 1.00, refo 1.00, verb 1.00 |
| full_ref | provenance | 0.67 | 0.67 [0.62-0.71] | 0.20 [0.17-0.23] | 0.67 | para 0.00, refo 1.00, verb 1.00 |
| app_full | reply_dlp | 0.67 | 0.67 [0.62-0.71] | 0.20 [0.17-0.23] | 0.67 | para 0.00, refo 1.00, verb 1.00 |
| app_full | meta_read_alarm | 0.43 | 1.00 [0.99-1.00] | 0.80 [0.77-0.83] | 0.60 | para 1.00, refo 1.00, verb 1.00 |
| app_full | provenance | 0.67 | 0.67 [0.62-0.71] | 0.20 [0.17-0.23] | 0.67 | para 0.00, refo 1.00, verb 1.00 |
| app_sinks | reply_dlp | 0.67 | 0.67 [0.62-0.71] | 0.20 [0.17-0.23] | 0.67 | para 0.00, refo 1.00, verb 1.00 |
| app_sinks | meta_read_alarm | 0.43 | 1.00 [0.99-1.00] | 0.80 [0.77-0.83] | 0.60 | para 1.00, refo 1.00, verb 1.00 |
| app_sinks | provenance | 0.00 | 0.00 [0.00-0.01] | 0.00 [0.00-0.01] | 0.00 | para 0.00, refo 0.00, verb 0.00 |
| app_hash | reply_dlp | 0.00 | 0.00 [0.00-0.01] | 0.00 [0.00-0.01] | 0.00 | para 0.00, refo 0.00, verb 0.00 |
| app_hash | meta_read_alarm | 0.43 | 1.00 [0.99-1.00] | 0.80 [0.77-0.83] | 0.60 | para 1.00, refo 1.00, verb 1.00 |
| app_hash | provenance | 0.50 | 1.00 [0.99-1.00] | 0.60 [0.56-0.64] | 0.67 | para 1.00, refo 1.00, verb 1.00 |
| app_meta | reply_dlp | 0.00 | 0.00 [0.00-0.01] | 0.00 [0.00-0.01] | 0.00 | para 0.00, refo 0.00, verb 0.00 |
| app_meta | meta_read_alarm | 0.43 | 1.00 [0.99-1.00] | 0.80 [0.77-0.83] | 0.60 | para 1.00, refo 1.00, verb 1.00 |
| app_meta | provenance | 0.00 | 0.00 [0.00-0.01] | 0.00 [0.00-0.01] | 0.00 | para 0.00, refo 0.00, verb 0.00 |
| service_meta | reply_dlp | 0.00 | 0.00 [0.00-0.01] | 0.00 [0.00-0.01] | 0.00 | para 0.00, refo 0.00, verb 0.00 |
| service_meta | meta_read_alarm | 0.43 | 0.67 [0.62-0.71] | 0.53 [0.49-0.57] | 0.52 | para 0.67, refo 0.67, verb 0.67 |
| service_meta | provenance | 0.00 | 0.00 [0.00-0.01] | 0.00 [0.00-0.01] | 0.00 | para 0.00, refo 0.00, verb 0.00 |
| host_meta | reply_dlp | 0.00 | 0.00 [0.00-0.01] | 0.00 [0.00-0.01] | 0.00 | para 0.00, refo 0.00, verb 0.00 |
| host_meta | meta_read_alarm | 0.39 | 1.00 [0.99-1.00] | 0.93 [0.91-0.95] | 0.56 | para 1.00, refo 1.00, verb 1.00 |
| host_meta | provenance | 0.00 | 0.00 [0.00-0.01] | 0.00 [0.00-0.01] | 0.00 | para 0.00, refo 0.00, verb 0.00 |
| b_only | reply_dlp | 0.67 | 0.67 [0.62-0.71] | 0.20 [0.17-0.23] | 0.67 | para 0.00, refo 1.00, verb 1.00 |
| b_only | meta_read_alarm | 0.43 | 1.00 [0.99-1.00] | 0.80 [0.77-0.83] | 0.60 | para 1.00, refo 1.00, verb 1.00 |
| b_only | provenance | 0.67 | 0.67 [0.62-0.71] | 0.20 [0.17-0.23] | 0.67 | para 0.00, refo 1.00, verb 1.00 |
| reply_only | reply_dlp | 0.67 | 0.33 [0.29-0.38] | 0.10 [0.08-0.13] | 0.44 | para 0.00, refo 0.50, verb 0.50 |
| reply_only | meta_read_alarm | 0.00 | 0.00 [0.00-0.01] | 0.00 [0.00-0.01] | 0.00 | para 0.00, refo 0.00, verb 0.00 |
| reply_only | provenance | 0.00 | 0.00 [0.00-0.01] | 0.00 [0.00-0.01] | 0.00 | para 0.00, refo 0.00, verb 0.00 |
| app_meta_drop50 | reply_dlp | 0.00 | 0.00 [0.00-0.01] | 0.00 [0.00-0.01] | 0.00 | para 0.00, refo 0.00, verb 0.00 |
| app_meta_drop50 | meta_read_alarm | 0.42 | 0.58 [0.53-0.63] | 0.48 [0.45-0.52] | 0.49 | para 0.58, refo 0.59, verb 0.57 |
| app_meta_drop50 | provenance | 0.00 | 0.00 [0.00-0.01] | 0.00 [0.00-0.01] | 0.00 | para 0.00, refo 0.00, verb 0.00 |

## test_ood_channel  (n=960, positives=360)

| profile | detector | precision | recall [95% CI] | FPR [95% CI] | F1 | recall by class |
|---|---|---|---|---|---|---|
| full_ref | reply_dlp | 0.67 | 0.67 [0.62-0.71] | 0.20 [0.17-0.23] | 0.67 | para 0.00, refo 1.00, verb 1.00 |
| full_ref | meta_read_alarm | 0.38 | 1.00 [0.99-1.00] | 1.00 [0.99-1.00] | 0.55 | para 1.00, refo 1.00, verb 1.00 |
| full_ref | provenance | 0.67 | 0.67 [0.62-0.71] | 0.20 [0.17-0.23] | 0.67 | para 0.00, refo 1.00, verb 1.00 |
| app_full | reply_dlp | 0.67 | 0.67 [0.62-0.71] | 0.20 [0.17-0.23] | 0.67 | para 0.00, refo 1.00, verb 1.00 |
| app_full | meta_read_alarm | 0.43 | 1.00 [0.99-1.00] | 0.80 [0.77-0.83] | 0.60 | para 1.00, refo 1.00, verb 1.00 |
| app_full | provenance | 0.67 | 0.67 [0.62-0.71] | 0.20 [0.17-0.23] | 0.67 | para 0.00, refo 1.00, verb 1.00 |
| app_sinks | reply_dlp | 0.67 | 0.67 [0.62-0.71] | 0.20 [0.17-0.23] | 0.67 | para 0.00, refo 1.00, verb 1.00 |
| app_sinks | meta_read_alarm | 0.43 | 1.00 [0.99-1.00] | 0.80 [0.77-0.83] | 0.60 | para 1.00, refo 1.00, verb 1.00 |
| app_sinks | provenance | 0.00 | 0.00 [0.00-0.01] | 0.00 [0.00-0.01] | 0.00 | para 0.00, refo 0.00, verb 0.00 |
| app_hash | reply_dlp | 0.00 | 0.00 [0.00-0.01] | 0.00 [0.00-0.01] | 0.00 | para 0.00, refo 0.00, verb 0.00 |
| app_hash | meta_read_alarm | 0.43 | 1.00 [0.99-1.00] | 0.80 [0.77-0.83] | 0.60 | para 1.00, refo 1.00, verb 1.00 |
| app_hash | provenance | 0.50 | 1.00 [0.99-1.00] | 0.60 [0.56-0.64] | 0.67 | para 1.00, refo 1.00, verb 1.00 |
| app_meta | reply_dlp | 0.00 | 0.00 [0.00-0.01] | 0.00 [0.00-0.01] | 0.00 | para 0.00, refo 0.00, verb 0.00 |
| app_meta | meta_read_alarm | 0.43 | 1.00 [0.99-1.00] | 0.80 [0.77-0.83] | 0.60 | para 1.00, refo 1.00, verb 1.00 |
| app_meta | provenance | 0.00 | 0.00 [0.00-0.01] | 0.00 [0.00-0.01] | 0.00 | para 0.00, refo 0.00, verb 0.00 |
| service_meta | reply_dlp | 0.00 | 0.00 [0.00-0.01] | 0.00 [0.00-0.01] | 0.00 | para 0.00, refo 0.00, verb 0.00 |
| service_meta | meta_read_alarm | 0.43 | 1.00 [0.99-1.00] | 0.80 [0.77-0.83] | 0.60 | para 1.00, refo 1.00, verb 1.00 |
| service_meta | provenance | 0.00 | 0.00 [0.00-0.01] | 0.00 [0.00-0.01] | 0.00 | para 0.00, refo 0.00, verb 0.00 |
| host_meta | reply_dlp | 0.00 | 0.00 [0.00-0.01] | 0.00 [0.00-0.01] | 0.00 | para 0.00, refo 0.00, verb 0.00 |
| host_meta | meta_read_alarm | 0.38 | 1.00 [0.99-1.00] | 1.00 [0.99-1.00] | 0.55 | para 1.00, refo 1.00, verb 1.00 |
| host_meta | provenance | 0.00 | 0.00 [0.00-0.01] | 0.00 [0.00-0.01] | 0.00 | para 0.00, refo 0.00, verb 0.00 |
| b_only | reply_dlp | 0.67 | 0.67 [0.62-0.71] | 0.20 [0.17-0.23] | 0.67 | para 0.00, refo 1.00, verb 1.00 |
| b_only | meta_read_alarm | 0.43 | 1.00 [0.99-1.00] | 0.80 [0.77-0.83] | 0.60 | para 1.00, refo 1.00, verb 1.00 |
| b_only | provenance | 0.67 | 0.67 [0.62-0.71] | 0.20 [0.17-0.23] | 0.67 | para 0.00, refo 1.00, verb 1.00 |
| reply_only | reply_dlp | 0.67 | 0.33 [0.29-0.38] | 0.10 [0.08-0.13] | 0.44 | para 0.00, refo 0.50, verb 0.50 |
| reply_only | meta_read_alarm | 0.00 | 0.00 [0.00-0.01] | 0.00 [0.00-0.01] | 0.00 | para 0.00, refo 0.00, verb 0.00 |
| reply_only | provenance | 0.00 | 0.00 [0.00-0.01] | 0.00 [0.00-0.01] | 0.00 | para 0.00, refo 0.00, verb 0.00 |
| app_meta_drop50 | reply_dlp | 0.00 | 0.00 [0.00-0.01] | 0.00 [0.00-0.01] | 0.00 | para 0.00, refo 0.00, verb 0.00 |
| app_meta_drop50 | meta_read_alarm | 0.39 | 0.53 [0.48-0.58] | 0.49 [0.45-0.53] | 0.45 | para 0.57, refo 0.51, verb 0.51 |
| app_meta_drop50 | provenance | 0.00 | 0.00 [0.00-0.01] | 0.00 [0.00-0.01] | 0.00 | para 0.00, refo 0.00, verb 0.00 |

## test_ood_class  (n=480, positives=240)

| profile | detector | precision | recall [95% CI] | FPR [95% CI] | F1 | recall by class |
|---|---|---|---|---|---|---|
| full_ref | reply_dlp | 0.00 | 0.00 [0.00-0.02] | 0.00 [0.00-0.02] | 0.00 | para 0.00 |
| full_ref | meta_read_alarm | 0.50 | 1.00 [0.98-1.00] | 1.00 [0.98-1.00] | 0.67 | para 1.00 |
| full_ref | provenance | 0.00 | 0.00 [0.00-0.02] | 0.00 [0.00-0.02] | 0.00 | para 0.00 |
| app_full | reply_dlp | 0.00 | 0.00 [0.00-0.02] | 0.00 [0.00-0.02] | 0.00 | para 0.00 |
| app_full | meta_read_alarm | 0.50 | 1.00 [0.98-1.00] | 1.00 [0.98-1.00] | 0.67 | para 1.00 |
| app_full | provenance | 0.00 | 0.00 [0.00-0.02] | 0.00 [0.00-0.02] | 0.00 | para 0.00 |
| app_sinks | reply_dlp | 0.00 | 0.00 [0.00-0.02] | 0.00 [0.00-0.02] | 0.00 | para 0.00 |
| app_sinks | meta_read_alarm | 0.50 | 1.00 [0.98-1.00] | 1.00 [0.98-1.00] | 0.67 | para 1.00 |
| app_sinks | provenance | 0.00 | 0.00 [0.00-0.02] | 0.00 [0.00-0.02] | 0.00 | para 0.00 |
| app_hash | reply_dlp | 0.00 | 0.00 [0.00-0.02] | 0.00 [0.00-0.02] | 0.00 | para 0.00 |
| app_hash | meta_read_alarm | 0.50 | 1.00 [0.98-1.00] | 1.00 [0.98-1.00] | 0.67 | para 1.00 |
| app_hash | provenance | 0.50 | 1.00 [0.98-1.00] | 1.00 [0.98-1.00] | 0.67 | para 1.00 |
| app_meta | reply_dlp | 0.00 | 0.00 [0.00-0.02] | 0.00 [0.00-0.02] | 0.00 | para 0.00 |
| app_meta | meta_read_alarm | 0.50 | 1.00 [0.98-1.00] | 1.00 [0.98-1.00] | 0.67 | para 1.00 |
| app_meta | provenance | 0.00 | 0.00 [0.00-0.02] | 0.00 [0.00-0.02] | 0.00 | para 0.00 |
| service_meta | reply_dlp | 0.00 | 0.00 [0.00-0.02] | 0.00 [0.00-0.02] | 0.00 | para 0.00 |
| service_meta | meta_read_alarm | 0.50 | 0.50 [0.44-0.56] | 0.50 [0.44-0.56] | 0.50 | para 0.50 |
| service_meta | provenance | 0.00 | 0.00 [0.00-0.02] | 0.00 [0.00-0.02] | 0.00 | para 0.00 |
| host_meta | reply_dlp | 0.00 | 0.00 [0.00-0.02] | 0.00 [0.00-0.02] | 0.00 | para 0.00 |
| host_meta | meta_read_alarm | 0.50 | 1.00 [0.98-1.00] | 1.00 [0.98-1.00] | 0.67 | para 1.00 |
| host_meta | provenance | 0.00 | 0.00 [0.00-0.02] | 0.00 [0.00-0.02] | 0.00 | para 0.00 |
| b_only | reply_dlp | 0.00 | 0.00 [0.00-0.02] | 0.00 [0.00-0.02] | 0.00 | para 0.00 |
| b_only | meta_read_alarm | 0.50 | 1.00 [0.98-1.00] | 1.00 [0.98-1.00] | 0.67 | para 1.00 |
| b_only | provenance | 0.00 | 0.00 [0.00-0.02] | 0.00 [0.00-0.02] | 0.00 | para 0.00 |
| reply_only | reply_dlp | 0.00 | 0.00 [0.00-0.02] | 0.00 [0.00-0.02] | 0.00 | para 0.00 |
| reply_only | meta_read_alarm | 0.00 | 0.00 [0.00-0.02] | 0.00 [0.00-0.02] | 0.00 | para 0.00 |
| reply_only | provenance | 0.00 | 0.00 [0.00-0.02] | 0.00 [0.00-0.02] | 0.00 | para 0.00 |
| app_meta_drop50 | reply_dlp | 0.00 | 0.00 [0.00-0.02] | 0.00 [0.00-0.02] | 0.00 | para 0.00 |
| app_meta_drop50 | meta_read_alarm | 0.49 | 0.54 [0.48-0.60] | 0.57 [0.51-0.63] | 0.51 | para 0.54 |
| app_meta_drop50 | provenance | 0.00 | 0.00 [0.00-0.02] | 0.00 [0.00-0.02] | 0.00 | para 0.00 |

## val  (n=288, positives=96)

| profile | detector | precision | recall [95% CI] | FPR [95% CI] | F1 | recall by class |
|---|---|---|---|---|---|---|
| full_ref | reply_dlp | 0.67 | 1.00 [0.96-1.00] | 0.25 [0.19-0.32] | 0.80 | refo 1.00, verb 1.00 |
| full_ref | meta_read_alarm | 0.36 | 1.00 [0.96-1.00] | 0.88 [0.82-0.91] | 0.53 | refo 1.00, verb 1.00 |
| full_ref | provenance | 0.67 | 1.00 [0.96-1.00] | 0.25 [0.19-0.32] | 0.80 | refo 1.00, verb 1.00 |
| app_full | reply_dlp | 0.67 | 1.00 [0.96-1.00] | 0.25 [0.19-0.32] | 0.80 | refo 1.00, verb 1.00 |
| app_full | meta_read_alarm | 0.40 | 1.00 [0.96-1.00] | 0.75 [0.68-0.81] | 0.57 | refo 1.00, verb 1.00 |
| app_full | provenance | 0.67 | 1.00 [0.96-1.00] | 0.25 [0.19-0.32] | 0.80 | refo 1.00, verb 1.00 |
| app_sinks | reply_dlp | 0.67 | 1.00 [0.96-1.00] | 0.25 [0.19-0.32] | 0.80 | refo 1.00, verb 1.00 |
| app_sinks | meta_read_alarm | 0.40 | 1.00 [0.96-1.00] | 0.75 [0.68-0.81] | 0.57 | refo 1.00, verb 1.00 |
| app_sinks | provenance | 0.00 | 0.00 [0.00-0.04] | 0.00 [0.00-0.02] | 0.00 | refo 0.00, verb 0.00 |
| app_hash | reply_dlp | 0.00 | 0.00 [0.00-0.04] | 0.00 [0.00-0.02] | 0.00 | refo 0.00, verb 0.00 |
| app_hash | meta_read_alarm | 0.40 | 1.00 [0.96-1.00] | 0.75 [0.68-0.81] | 0.57 | refo 1.00, verb 1.00 |
| app_hash | provenance | 0.50 | 1.00 [0.96-1.00] | 0.50 [0.43-0.57] | 0.67 | refo 1.00, verb 1.00 |
| app_meta | reply_dlp | 0.00 | 0.00 [0.00-0.04] | 0.00 [0.00-0.02] | 0.00 | refo 0.00, verb 0.00 |
| app_meta | meta_read_alarm | 0.40 | 1.00 [0.96-1.00] | 0.75 [0.68-0.81] | 0.57 | refo 1.00, verb 1.00 |
| app_meta | provenance | 0.00 | 0.00 [0.00-0.04] | 0.00 [0.00-0.02] | 0.00 | refo 0.00, verb 0.00 |
| service_meta | reply_dlp | 0.00 | 0.00 [0.00-0.04] | 0.00 [0.00-0.02] | 0.00 | refo 0.00, verb 0.00 |
| service_meta | meta_read_alarm | 0.40 | 0.50 [0.40-0.60] | 0.38 [0.31-0.45] | 0.44 | refo 0.50, verb 0.50 |
| service_meta | provenance | 0.00 | 0.00 [0.00-0.04] | 0.00 [0.00-0.02] | 0.00 | refo 0.00, verb 0.00 |
| host_meta | reply_dlp | 0.00 | 0.00 [0.00-0.04] | 0.00 [0.00-0.02] | 0.00 | refo 0.00, verb 0.00 |
| host_meta | meta_read_alarm | 0.36 | 1.00 [0.96-1.00] | 0.88 [0.82-0.91] | 0.53 | refo 1.00, verb 1.00 |
| host_meta | provenance | 0.00 | 0.00 [0.00-0.04] | 0.00 [0.00-0.02] | 0.00 | refo 0.00, verb 0.00 |
| b_only | reply_dlp | 0.67 | 1.00 [0.96-1.00] | 0.25 [0.19-0.32] | 0.80 | refo 1.00, verb 1.00 |
| b_only | meta_read_alarm | 0.40 | 1.00 [0.96-1.00] | 0.75 [0.68-0.81] | 0.57 | refo 1.00, verb 1.00 |
| b_only | provenance | 0.67 | 1.00 [0.96-1.00] | 0.25 [0.19-0.32] | 0.80 | refo 1.00, verb 1.00 |
| reply_only | reply_dlp | 0.67 | 0.50 [0.40-0.60] | 0.12 [0.09-0.18] | 0.57 | refo 0.50, verb 0.50 |
| reply_only | meta_read_alarm | 0.00 | 0.00 [0.00-0.04] | 0.00 [0.00-0.02] | 0.00 | refo 0.00, verb 0.00 |
| reply_only | provenance | 0.00 | 0.00 [0.00-0.04] | 0.00 [0.00-0.02] | 0.00 | refo 0.00, verb 0.00 |
| app_meta_drop50 | reply_dlp | 0.00 | 0.00 [0.00-0.04] | 0.00 [0.00-0.02] | 0.00 | refo 0.00, verb 0.00 |
| app_meta_drop50 | meta_read_alarm | 0.41 | 0.65 [0.55-0.73] | 0.46 [0.39-0.53] | 0.50 | refo 0.67, verb 0.62 |
| app_meta_drop50 | provenance | 0.00 | 0.00 [0.00-0.04] | 0.00 [0.00-0.02] | 0.00 | refo 0.00, verb 0.00 |
