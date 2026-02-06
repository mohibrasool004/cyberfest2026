# Dashboard

This Streamlit dashboard visualizes training progress, per-class metrics, failure examples, benchmark results, and submission checklist.

Run locally (activate your virtualenv first):

```bash
pip install -r dashboard/requirements.txt
streamlit run dashboard/app.py
```

Notes:
- The app reads artifacts from `dataset/train_stats/`, `train_logs/run.log`, `benchmark_results.json`, and `submission.zip` at the repository root.
- If any files are missing the app will show helpful messages and continue.
