# Training Monitoring & Progress Report (Final)

**Training completed on**: Feb 6, 2026  
**Source of truth**: `train_logs/run.log` and `dataset/train_stats/evaluation_metrics.txt`

## Final Metrics (Validation)
```
Mean IoU:        0.2700
Dice Score:      0.4272
Pixel Accuracy:  0.6901
```

## Artifacts Created
- `dataset/segmentation_head.pth`
- `dataset/train_stats/training_curves.png`
- `dataset/train_stats/iou_curves.png`
- `dataset/train_stats/dice_curves.png`
- `dataset/train_stats/all_metrics_curves.png`
- `dataset/train_stats/evaluation_metrics.txt`

## Notes
- The inference benchmark (CPU) is **~1204.7 ms/image** from `results/inference_benchmark.json`.
- Failure analysis in `results/failure_analysis.json` is a **placeholder** unless regenerated.

