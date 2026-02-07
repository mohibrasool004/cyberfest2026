# Hackathon Submission - Status Dashboard (Accurate as of Feb 7, 2026)

## Current Status
- Training: Complete (10/10 epochs)
- Final Validation Metrics:
  - Mean IoU: 0.2700
  - Dice: 0.4272
  - Pixel Accuracy: 0.6901
- Inference Benchmark (CPU): ~3188.7 ms/image (FAIL vs <50 ms)
- Test Mean IoU (local masks): 0.1996 (from `results/test_evaluation_metrics.txt`)
- Submission Package: `submission.zip` exists

## Key Artifacts
- Model weights: `dataset/segmentation_head.pth` (copied to `submission/checkpoint_final.pt`)
- Training metrics: `dataset/train_stats/evaluation_metrics.txt`
- Training curves: `dataset/train_stats/*.png`
- Benchmark: `results/inference_benchmark.json`
- Test metrics: `results/test_evaluation_metrics.txt`
- Test per-class chart: `results/test_per_class_metrics.png`
- Failure analysis: `results/failure_analysis.json` (placeholder unless regenerated)

## Data Summary
- Train: 2,857 images
- Val: 317 images
- Test: 1,002 images (masks present in local copy)

## What Still Needs Work (If Improving)
1. Improve accuracy (current Val IoU 0.2700 is low baseline).
2. Optimize inference speed (CPU benchmark fails <50 ms).
3. Generate real failure analysis if required by judges.

## Pointers
- Full report: `RESULTS.md`
- Training details: `TRAINING_GUIDE.md`
- Packaging: `create_submission_package.py`

