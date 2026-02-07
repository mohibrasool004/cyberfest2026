# Quick Reference (Accurate as of Feb 7, 2026)

## Current Metrics
- Val IoU: 0.2700
- Dice: 0.4272
- Pixel Accuracy: 0.6901
- Test Mean IoU: 0.1996
- CPU inference: ~3188.7 ms/image (FAIL vs <50 ms)

## Key Commands
```bash
# Train (re-run)
python dataset/train_segmentation.py

# Evaluate (requires masks)
python dataset/test_segmentation.py --data_dir dataset/Offroad_Segmentation_testImages --output_dir predictions

# Benchmark inference
python benchmark_inference.py

# Build submission package
python create_submission_package.py
```

## Key Files
- `dataset/train_stats/evaluation_metrics.txt`
- `results/test_evaluation_metrics.txt`
- `results/test_per_class_metrics.png`
- `results/inference_benchmark.json`
- `submission.zip`

