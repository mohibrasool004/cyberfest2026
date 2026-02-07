# Hackathon Segmentation: Project README (Accurate as of Feb 7, 2026)

## Overview
This repository contains a trained semantic segmentation model for Duality AI's Offroad Autonomy Segmentation Hackathon.

**Training status**: Complete (10 epochs).  
**Final validation metrics** (from `dataset/train_stats/evaluation_metrics.txt`):
- Mean IoU: **0.2700**
- Dice Score: **0.4272**
- Pixel Accuracy: **0.6901**

**Inference benchmark** (CPU, from `results/inference_benchmark.json`):
- Mean inference time: **~3188.7 ms/image** (does **not** meet the <50 ms requirement on CPU)

**Test set evaluation** (local masks, from `results/test_evaluation_metrics.txt`):
- Mean IoU: **0.1996**

## Repository Structure
```
Hackathon/
  dataset/
    Offroad_Segmentation_Training_Dataset/
      train/Color_Images (2,857 PNG)
      train/Segmentation (2,857 PNG)
      val/Color_Images (317 PNG)
      val/Segmentation (317 PNG)
    Offroad_Segmentation_testImages/
      Color_Images (1,002 PNG)
      Segmentation (1,002 PNG)
    train_segmentation.py
    test_segmentation.py
    train_stats/ (training curves + metrics)
  results/
    inference_benchmark.json
    test_evaluation_metrics.txt
    test_per_class_metrics.png
  submission/
    checkpoint_final.pt
    scripts/ (train/test/eval)
    results/ (metrics + benchmark JSON)
    docs (README, RESULTS, etc)
  create_submission_package.py
  run_post_training_eval.py
  benchmark_inference.py
  submission.zip
```

## Model Summary
- Backbone: DINOv2 ViT-S/14 (frozen)
- Head: ConvNeXt-style lightweight segmentation head
- Classes: 11 total (includes Flowers)
- Input size: 476 x 938

## Training (Reproducible)
```bash
python dataset/train_segmentation.py
```
Outputs:
- `dataset/segmentation_head.pth`
- `dataset/train_stats/*.png`
- `dataset/train_stats/evaluation_metrics.txt`

## Evaluation
```bash
python dataset/test_segmentation.py --data_dir dataset/Offroad_Segmentation_testImages --output_dir predictions
```
Notes:
- This script expects masks in the test folder (they exist here).
- Latest mean IoU: **0.1996** (see `results/test_evaluation_metrics.txt`).

## Benchmark
```bash
python benchmark_inference.py
```
This produces `results/inference_benchmark.json`. The last run on CPU is **~3188.7 ms/image**, which fails the <50 ms requirement.

## Known Limitations
- CPU inference is **not** real-time (<50 ms). The current benchmark fails the requirement.
- Accuracy is a low baseline (Val IoU 0.2700); improvements are required to be competitive.
- Failure analysis JSON is a placeholder unless regenerated with real outputs.

## Submission Package
To rebuild the submission package with current artifacts:
```bash
python create_submission_package.py
```
This creates/refreshes `submission/` and `submission.zip`.

