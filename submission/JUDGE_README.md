# Hackathon Submission - Evaluation Guide for Judges

## Quick Start

### 1. Extract and Setup
```bash
unzip submission.zip
cd submission
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
```

### 2. Evaluate Model
```bash
# Run inference on test images
python scripts/test_segmentation.py \
  --model checkpoint_final.pt \
  --test-dir /path/to/test/images \
  --output results/predictions
```

### 3. Review Results
- Open `RESULTS.md` for detailed technical report
- View `results/training_curves.png` for training progression
- Check `results/evaluation_metrics.txt` for final scores
- Review `results/failure_analysis.json` for per-class breakdown

## Submission Contents

```
submission/
--- checkpoint_final.pt          # Trained model (10 MB)
--- scripts/
|   --- train_segmentation.py    # Training script (provided)
|   --- test_segmentation.py     # Test/inference script
|   --- evaluation.py            # Evaluation framework
--- results/
|   --- training_curves.png      # Loss & IoU progression
|   --- evaluation_metrics.txt   # Final metrics
|   --- failure_analysis.json    # Per-class analysis
--- README.md                    # Full documentation
--- RESULTS.md                   # 8-page technical report
--- TRAINING_GUIDE.md            # Training process details
--- requirements.txt             # Dependencies
--- config.json                  # Model configuration

```

## Key Metrics

| Metric | Value | Status |
|--------|-------|--------|
| Validation IoU | 0.27 | [WARN] Low baseline |
| Dice Score | 0.4272 | [WARN] Low baseline |
| Pixel Accuracy | 0.6901 | [WARN] Low baseline |
| Inference Speed (CPU) | 1204.7450200007006 ms | [FAIL] FAIL (<50ms req) |
| Classes Segmented | 11/11 | [OK] All classes |
| Model Size | ~10 MB | [OK] Lightweight |

## Architecture Overview

```
Input Image (476x938)
         v
[DINOv2-ViT-S/14] <- Pre-trained backbone (frozen)
    384-dim embeddings
         v
[ConvNeXt Lightweight Head] <- Trained head (~10M params)
  - Conv Stem (384->128)
  - Depthwise-separable blocks
  - Classifier (128->11 classes)
         v
Output Mask (476x938, 11 classes)
```

**Why DINOv2?**
- Pre-trained on 1M+ images -> strong generic features
- Self-supervised learning -> robust to domain shift
- Fast inference (frozen backbone, no fine-tuning)
- Good performance on downstream tasks

## Performance Analysis

### Strengths
[OK] **Fast Training**: 4-5 hours on CPU (10 epochs)  
[WARN] **Inference Speed**: CPU benchmark is ~1205 ms/image (does NOT meet <50 ms requirement)  
[OK] **Reproducible**: Fixed seed, documented config, environment locked  
[OK] **Generalizable**: Frozen backbone adapts to new biomes  

### Known Limitations
[WARN] **Thin Objects**: Flowers & Logs have lower IoU (sparse pixels)  
[WARN] **Class Confusion**: Dry/Lush bushes sometimes confused (color-based)  
[WARN] **Baseline Approach**: No fine-tuning or heavy augmentation (v2 opportunities)  

### Recommended Improvements
1. **Class Weighting** -> +0.05 IoU (easy, <1 hour)
2. **Backbone Fine-tuning** -> +0.07 IoU (moderate, 2-4 hours)
3. **CRF Post-processing** -> +0.02 IoU (easy, <30 min)
4. **Ensembling** -> +0.03 IoU (moderate, 3-5 hours)
5. **Domain Adaptation** -> +0.10 IoU (hard, 1-2 days)

See `RESULTS.md` section 6 for detailed improvement strategies.

## Reproducibility

To reproduce this exact model:

```bash
# Setup environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Download DINOv2 (auto-downloads on first run)
python scripts/train_segmentation.py

# Or manually download:
# wget https://dl.fbaipublicfiles.com/dinov2/dinov2_vits14/dinov2_vits14_pretrain.pth

# Training will take ~5 hours on CPU
# GPU training would take ~30 minutes
```

**Environment Locked**:
- PyTorch 2.1.0 (CPU build)
- Fixed random seed: 42
- Deterministic operations enabled
- No stochastic augmentations (v1)

## Questions?

See documentation:
- **Technical Details**: RESULTS.md (sections 1-2)
- **Training Process**: TRAINING_GUIDE.md
- **Architecture**: config.json
- **Failure Analysis**: RESULTS.md (section 5)

---

**Submission Date**: 2026-02-07 06:29:55  
**Framework**: PyTorch 2.1.0  
**Model**: DINOv2-ViT-S/14 + ConvNeXt Head  
**Status**: [OK] Ready for Evaluation (metrics disclosed)
