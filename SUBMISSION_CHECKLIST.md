# Submission Checklist (Accurate as of Feb 7, 2026)

## Artifacts
- [x] `dataset/segmentation_head.pth` exists
- [x] `dataset/train_stats/evaluation_metrics.txt` exists
- [x] `dataset/train_stats/*.png` curves exist
- [x] `results/inference_benchmark.json` exists (CPU ~1204.7 ms)
- [x] `submission.zip` exists

## Metrics (Validation)
- Mean IoU: **0.2700**
- Dice: **0.4272**
- Pixel Accuracy: **0.6901**

## Known Limitations to Disclose
- CPU inference benchmark fails <50 ms requirement.
- Failure analysis JSON is a placeholder unless regenerated.

## Packaging
```bash
python create_submission_package.py
```

