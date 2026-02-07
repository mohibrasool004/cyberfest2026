# START HERE (Accurate as of Feb 7, 2026)

## Current Status
Training is **complete**. Final validation metrics:
- Mean IoU: **0.2700**
- Dice: **0.4272**
- Pixel Accuracy: **0.6901**

Inference benchmark (CPU): **~1204.7 ms/image** (fails <50 ms requirement).

## Key Files
- `RESULTS.md` – concise, accurate results summary.
- `STATUS_DASHBOARD.md` – current status.
- `TRAINING_GUIDE.md` – how training was done.
- `create_submission_package.py` – rebuild `submission/` and `submission.zip`.

## If You Need to Improve Performance
1. Fine‑tune DINOv2 last blocks.
2. Add class weighting/focal loss.
3. Use stronger augmentations.
4. Re‑benchmark on GPU if available.

