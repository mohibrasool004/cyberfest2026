# Submission Checklist (Accurate as of Feb 7, 2026)

## Artifacts
- [x] `dataset/segmentation_head.pth`
- [x] `dataset/train_stats/evaluation_metrics.txt`
- [x] `dataset/train_stats/*.png`
- [x] `results/inference_benchmark.json`
- [x] `results/test_evaluation_metrics.txt`
- [x] `results/test_per_class_metrics.png`
- [x] `submission.zip`

## Metrics
- Validation Mean IoU: 0.2700
- Validation Dice: 0.4272
- Validation Pixel Accuracy: 0.6901
- Test Mean IoU: 0.1996
- CPU Inference: ~3188.7 ms/image (FAIL vs <50 ms)

## Packaging
```bash
python create_submission_package.py
```

