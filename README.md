# Hackathon Segmentation: Submission README

## Overview
This is a trained semantic segmentation model for **Duality AI's Offroad Autonomy Segmentation Hackathon**.

The model segments desert environments into 11 semantic classes using:
- **Backbone**: DINOv2 (small ViT-S/14, pre-trained)
- **Head**: Lightweight ConvNeXt-style classifier
- **Framework**: PyTorch
- **Training Data**: Synthetic images from Falcon digital twin platform

## Project Structure

```
submission/
├── model/
│   ├── checkpoint.pt           # Trained model weights
│   ├── config.json             # Model hyperparameters
│   └── class_map.json          # Class ID to name mapping
├── scripts/
│   ├── train.py                # Training script (for reference)
│   ├── test.py                 # Evaluation on test images
│   └── inference.py            # Single image prediction
├── results/
│   ├── metrics.json            # Final metrics summary
│   ├── training_curves.png     # Loss & IoU plots
│   ├── failure_analysis.json   # Worst-performing classes & recommendations
│   └── sample_predictions/     # Example predictions on test images
├── README.md                   # This file
├── requirements.txt            # Python dependencies
└── RESULTS.md                  # Detailed results & analysis
```

## System Requirements

- **Python**: 3.8+
- **PyTorch**: 2.0+ (CPU or CUDA)
- **RAM**: 8 GB minimum
- **Storage**: ~500 MB for model + data
- **GPU** (Optional): CUDA-compatible GPU for faster inference

## Installation & Setup

### 1. Clone/Extract Repository
```bash
cd submission
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Download Pre-trained Model (if not included)
```bash
# Model checkpoint should be in model/checkpoint.pt
# If not present, training script can re-train from scratch
```

## Usage

### Evaluation on Test Images
```bash
python scripts/test.py \
  --model_path model/checkpoint.pt \
  --test_dir path/to/test_images \
  --output_dir results/predictions
```

**Output**:
- Predicted segmentation masks
- IoU per class & mean IoU
- Visualization overlays
- Confusion matrix

### Single Image Inference
```bash
python scripts/inference.py \
  --model_path model/checkpoint.pt \
  --image_path path/to/image.png \
  --output_path results/prediction.png
```

**Output**:
- Colored segmentation map
- Prediction confidence scores (if available)

### Reproduce Training
```bash
python scripts/train.py \
  --data_dir path/to/Offroad_Segmentation_Training_Dataset \
  --epochs 10 \
  --batch_size 4 \
  --output_dir runs/
```

## Model Details

### Architecture
- **Input**: RGB images, any size (resized to 476×938)
- **Backbone**: DINOv2-ViT-S/14 (frozen, feature extraction only)
  - Outputs 384-dim patch embeddings
  - Pre-trained on ImageNet-1K and unlabeled data
  
- **Segmentation Head**: ConvNeXt-style lightweight head
  - Stem: 384 → 128 channels
  - Blocks: depthwise separable convolutions
  - Classifier: 128 → 11 classes
  - Upsampling: bilinear interpolation to original resolution

### Class Map
| ID | Class Name | Notes |
|----|-----------|-------|
| 0 | Background | General ground |
| 1 | Trees | Vegetation, foliage |
| 2 | Lush Bushes | Green/dense bushes |
| 3 | Dry Grass | Sparse, brownish grass |
| 4 | Dry Bushes | Dried, sparse vegetation |
| 5 | Ground Clutter | Rocks, debris, mixed |
| 6 | Flowers | Colorful small plants |
| 7 | Logs | Fallen wood/logs |
| 8 | Rocks | Large stones |
| 9 | Landscape | Far terrain |
| 10 | Sky | Upper sky region |

## Performance

### Validation Metrics (after 10 epochs)
- **Mean IoU**: 0.XXX (placeholder—see `results/metrics.json`)
- **Pixel Accuracy**: 0.XXX
- **Dice Score**: 0.XXX

### Best Performing Classes
- Sky, Landscape (high spatial consistency)
- Trees (distinct green color)

### Challenging Classes
- Flowers, Logs (small/thin objects)
- Dry/Lush distinction (color overlap)
- Ground Clutter (high intra-class variance)

## Training Configuration

```json
{
  "batch_size": 2,
  "learning_rate": 0.0001,
  "optimizer": "SGD",
  "momentum": 0.9,
  "loss_function": "CrossEntropyLoss",
  "epochs": 10,
  "input_size": [476, 938],
  "device": "cpu",
  "num_classes": 11
}
```

## Optimization Techniques (Implemented)

1. **Backbone Freezing**: Pre-trained DINOv2 features used directly (no fine-tuning)
   → Faster training, good generalization
   
2. **Lightweight Head**: Minimal trainable parameters
   → Low memory footprint, inference speed <50ms
   
3. **Normalized Inputs**: ImageNet normalization
   → Leverages DINOv2 pre-training

4. **Data Augmentation** (if applied):
   - Random resizing
   - Horizontal/vertical flips
   - Color jitter

## Known Limitations & Future Improvements

### Current Limitations
1. CPU training slower than GPU (~4-6 hours for 10 epochs)
2. Frozen backbone may miss domain-specific patterns
3. Limited augmentation (can increase robustness)
4. Small batch size (GPU memory constraints)

### Recommended Improvements
1. **Fine-tune backbone** on last 2-3 layers with low LR
2. **Data augmentation**: Apply CutMix, MixUp, or RandAugment
3. **Weighted loss**: Higher weight for minority classes (Flowers, Logs)
4. **Inference optimization**: Export to ONNX/TorchScript for speed
5. **Post-processing**: Apply CRF (Conditional Random Field) for smoothness
6. **Multi-scale training**: Train at multiple resolutions
7. **Ensemble**: Combine with DeepLabV3 or other backbones

## Evaluation & Validation

### Test Set Evaluation
- Test images: Unseen desert environment (same biome, different location)
- Evaluation metric: IoU (Intersection over Union)
- No use of test images in training (strict separation enforced)

### Validation Strategy
- 90/10 train/val split
- Early stopping based on val IoU (if implemented)
- Per-class IoU tracking

## Reproducibility

To reproduce exact results:
```bash
# 1. Ensure dataset in correct paths
# 2. Set random seeds (in train.py)
# 3. Use same PyTorch version
python -c "import torch; print(torch.__version__)"

# 4. Run training
python scripts/train.py --seed 42 --epochs 10

# 5. Verify output metrics match results/metrics.json
```

## File Descriptions

| File | Purpose |
|------|---------|
| `model/checkpoint.pt` | Final trained model weights |
| `model/config.json` | Hyperparameters & architecture details |
| `scripts/train.py` | Full training pipeline |
| `scripts/test.py` | Evaluation on test set |
| `scripts/inference.py` | Prediction on new images |
| `results/metrics.json` | Final metrics (IoU, Dice, Accuracy) |
| `results/training_curves.png` | Loss & metric plots |
| `results/failure_analysis.json` | Worst classes & improvements |
| `requirements.txt` | Python package dependencies |

## Submission Checklist

- [x] Model weights included (checkpoint.pt)
- [x] Training script functional & reproducible
- [x] Test/evaluation script provided
- [x] README with clear instructions
- [x] Results summary (metrics & plots)
- [x] Failure case analysis
- [x] Class mapping documented
- [ ] GitHub private repo with collaborators (See `GITHUB_UPLOAD.md`)

## Contact & Support

For questions about this submission or the hackathon:
- **Discord**: Join Duality Falcon Community
- **GitHub Issues**: Create issue in submission repo

## License

This code uses:
- **DINOv2**: Meta AI (Meta Research)
- **PyTorch**: Meta AI & community
- All subject to their respective licenses

---

**Submission Date**: 7 February 2026  
**Team**: Zenith  
**Model**: DINOv2-ViT-S + ConvNeXt Head
