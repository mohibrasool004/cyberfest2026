# Hackathon Segmentation Baseline Setup Guide

## Folder Structure & Files

```
Hackathon/
├── dataset/
│   ├── Offroad_Segmentation_Training_Dataset/
│   │   ├── train/
│   │   │   ├── Color_Images/
│   │   │   └── Segmentation/
│   │   └── val/
│   │       ├── Color_Images/
│   │       └── Segmentation/
│   ├── Offroad_Segmentation_testImages/
│   │   ├── Color_Images/
│   │   └── Segmentation/
│   ├── train_segmentation.py
│   ├── test_segmentation.py
│   └── visualize.py
├── runs/ (generated after training)
│   ├── train_stats/
│   │   ├── training_curves.png
│   │   ├── iou_curves.png
│   │   ├── dice_curves.png
│   │   ├── all_metrics_curves.png
│   │   └── evaluation_metrics.txt
└── ...
```

## Training Process

### Step 1: Environment Setup
- Python 3.13 venv in `.venv`
- Dependencies: torch, torchvision, torchaudio (CPU), opencv-python, matplotlib, tqdm, scipy, scikit-learn

### Step 2: Data Preparation
- **Training Data**: Located in `dataset/Offroad_Segmentation_Training_Dataset/train/`
  - Color_Images: RGB images (480x960px approx)
  - Segmentation: Mask images with class IDs (100, 200, 300, 500, 550, 600, 700, 800, 7100, 10000)
- **Validation Data**: Located in `dataset/Offroad_Segmentation_Training_Dataset/val/`
  - Same structure as training

### Step 3: Model Architecture
- **Backbone**: DINOv2 (small vits14 variant)
  - Pre-trained on large-scale unlabeled image data
  - Frozen features (no gradient updates)
  - Outputs patch tokens (336 dimensions)
  
- **Segmentation Head**: ConvNeXt-style lightweight head
  - Conv stem (in_channels → 128)
  - Depthwise separable convolutions (128 → 128)
  - Final classifier (128 → 11 classes)
  - Upsamples predictions to original image size

### Step 4: Training Configuration
- **Batch Size**: 2 (CPU-friendly)
- **Input Resolution**: 476x938 (multiple of 14 for DINOv2 patches)
- **Learning Rate**: 1e-4 (SGD with momentum 0.9)
- **Loss Function**: CrossEntropyLoss
- **Epochs**: 10 (baseline; can increase)
- **Device**: CPU (GPU available but AMD lacks CUDA/ROCm support on Windows)

### Step 5: Evaluation Metrics
For each epoch, the script computes:
- **IoU (Intersection over Union)**: Per-class & mean
- **Dice Score**: Per-class & mean
- **Pixel Accuracy**: Percentage of correctly classified pixels

### Step 6: Outputs
After training completes:
- Model weights & checkpoints
- Training plots (loss, IoU, Dice, accuracy curves)
- Evaluation metrics summary (text file)

## Class Mapping
```
ID    Class Name
0     Background
100   Trees
200   Lush Bushes
300   Dry Grass
500   Dry Bushes
550   Ground Clutter
600   Flowers
700   Logs
800   Rocks
7100  Landscape
10000 Sky
```

## Running Training

```bash
# Activate environment
conda activate EDU
# or
source .venv/Scripts/activate

# Run training
python dataset/train_segmentation.py
```

**Expected Output**:
- Real-time epoch progress with loss, IoU, accuracy
- Training curves saved to `dataset/train_stats/`
- Metrics summary in text file

## Next Steps
1. Monitor training progress (check terminal output)
2. Evaluate on test images using `test_segmentation.py`
3. Analyze failure cases & improve (augmentation, hyperparams)
4. Generate final report & submission package
