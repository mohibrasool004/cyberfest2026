# Complete Project Summary (Accurate as of Feb 7, 2026)

## Status
- Training complete (10 epochs).
- Val IoU: 0.2700
- Dice: 0.4272
- Pixel Accuracy: 0.6901
- CPU Inference Benchmark: ~3188.7 ms/image (FAIL vs <50 ms)
- Test Mean IoU (local masks): 0.1996

## Key Artifacts
- Weights: `dataset/segmentation_head.pth`
- Training stats: `dataset/train_stats/evaluation_metrics.txt`
- Training curves: `dataset/train_stats/*.png`
- Test metrics: `results/test_evaluation_metrics.txt`
- Test per-class chart: `results/test_per_class_metrics.png`
- Benchmark: `results/inference_benchmark.json`
- Submission package: `submission.zip`

## Known Gaps
- Low baseline accuracy (Val IoU 0.2700).
- CPU inference speed fails requirement.
- Failure analysis JSON is placeholder unless regenerated.

## Next Steps (If Improving)
1. Fine-tune backbone + class weighting.
2. Add augmentations and more epochs.
3. Measure GPU inference.

