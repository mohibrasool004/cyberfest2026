# Submission Package README (Accurate as of Feb 7, 2026)

This README is intended for the `submission/` folder and `submission.zip`.

## Contents
```
submission/
  checkpoint_final.pt
  scripts/
    train_segmentation.py
    test_segmentation.py
    evaluation.py
    run_post_training_eval.py
  results/
    training_curves.png
    iou_curves.png
    dice_curves.png
    all_metrics_curves.png
    evaluation_metrics.txt
    inference_benchmark.json
    failure_analysis.json
  README.md
  RESULTS.md
  TRAINING_GUIDE.md
  JUDGE_README.md
  requirements.txt
  config.json
```

## Quick Start
```bash
python -m venv venv
source venv/bin/activate  # or venv\\Scripts\\activate on Windows
pip install -r requirements.txt
```

## Metrics (Validation)
- Mean IoU: **0.2700**
- Dice: **0.4272**
- Pixel Accuracy: **0.6901**

## Inference Speed
CPU benchmark from `results/inference_benchmark.json`:
- **~1204.7 ms/image** (fails <50 ms requirement on CPU)

## Notes
- `results/failure_analysis.json` is a placeholder unless regenerated from real model outputs.
- For full details, see `RESULTS.md` and `JUDGE_README.md`.

