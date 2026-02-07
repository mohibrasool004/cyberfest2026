# Hackathon Segmentation Results (Accurate as of Feb 7, 2026)

## Executive Summary
- **Model**: DINOv2-ViT-S/14 (frozen) + ConvNeXt-style head
- **Framework**: PyTorch
- **Final Validation IoU**: **0.2700**
- **Final Dice Score**: **0.4272**
- **Final Pixel Accuracy**: **0.6901**

Metrics source: `dataset/train_stats/evaluation_metrics.txt` (generated Feb 6, 2026).

## Dataset Overview
- Train: 2,857 images
- Val: 317 images
- Test: 1,002 images (includes masks in this local dataset)

## Model Architecture
- Backbone: DINOv2 ViT-S/14 (frozen features)
- Head: lightweight ConvNeXt-style segmentation head
- Classes: 11 semantic categories (including Flowers)

## Training Configuration
- Batch size: 2
- Epochs: 10
- Optimizer: SGD (lr=1e-4, momentum=0.9)
- Loss: CrossEntropyLoss
- Device: CPU

## Final Metrics (Validation Set)
```
Final Validation Metrics (Epoch 10):
  Mean IoU:        0.2700
  Dice Score:      0.4272
  Pixel Accuracy:  0.6901

Best Epoch Metrics:
  Best Val IoU:    0.2700 (Epoch 10)
  Best Val Dice:   0.4272 (Epoch 10)
  Best Val Accuracy: 0.6901 (Epoch 10)
```

## Per-Class Performance
Per-class IoU/Dice values are **not computed** in this report. Use:
```bash
python dataset/test_segmentation.py --data_dir dataset/Offroad_Segmentation_testImages --output_dir predictions
```
This script produces a per-class IoU chart in `predictions/per_class_metrics.png`.

## Training Curves
Training curves are stored in:
- `dataset/train_stats/training_curves.png`
- `dataset/train_stats/iou_curves.png`
- `dataset/train_stats/dice_curves.png`
- `dataset/train_stats/all_metrics_curves.png`

## Inference Speed
Benchmark result from `results/inference_benchmark.json`:
- CPU mean inference time: **~1204.7 ms/image**
- Status: **FAIL** vs <50 ms requirement

## Failure Analysis
`results/failure_analysis.json` is currently a **placeholder** unless regenerated from actual model outputs.

## Recommendations (If improving)
1. Fine-tune last blocks of DINOv2 with low LR.
2. Use class weighting or focal loss for small classes (Flowers, Logs).
3. Add stronger data augmentation.
4. Re-run inference benchmark on GPU if available.

