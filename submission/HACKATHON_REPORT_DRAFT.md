# Hackathon Segmentation Report

## 1. Title & Summary

**Team Name:** [Your Team Name]  
**Project Name:** Offroad Semantic Segmentation  
**Tagline:** Fast, Accurate, and Judge-Friendly Segmentation with Interactive Dashboard  

## 2. Methodology

### Dataset
- **Source:** Falcon synthetic desert dataset (Duality AI)
- **Classes:** 11 semantic categories
- **Splits:** Train (2,857), Val (317), Test (1,002, masks present in local copy)
- **Preprocessing:** Resize to 476x938, normalization (ImageNet stats)

### Model Architecture
- **Backbone:** DINOv2-ViT-S/14 (frozen, pre-trained)
- **Head:** Lightweight ConvNeXt-style segmentation head
- **Framework:** PyTorch
- **Parameters:** <10M (compact, CPU-friendly)

### Training
- **Batch Size:** 2 (CPU)
- **Epochs:** 10
- **Optimizer:** SGD (lr=1e-4, momentum=0.9)
- **Loss:** CrossEntropyLoss (no class weighting in v1)
- **Augmentation:** Resize, normalization (recommend: flip, color jitter for v2)

### Metrics
- **IoU (Intersection over Union)**
- **Dice Score (F1)**
- **Pixel Accuracy**

## 3. Results & Performance

### Final Validation Metrics
- **Mean IoU:** 0.2700 (from `dataset/train_stats/evaluation_metrics.txt`)
- **Dice Score:** 0.4272
- **Pixel Accuracy:** 0.6901

### Per-Class Performance
Per-class IoU values are **not computed** in this report.  
Use `python dataset/test_segmentation.py --data_dir dataset/Offroad_Segmentation_testImages` to generate per-class metrics.

### Training Curves
- See `dataset/train_stats/training_curves.png` for loss, accuracy, IoU progression.

### Inference Speed
- **CPU:** ~1204.7 ms/image (fails <50 ms requirement on CPU, from `results/inference_benchmark.json`)

### Dashboard Innovation
- **Streamlit dashboard** for judges: shows metrics, per-class results, failure analysis (text fallback if images unavailable)
- **Value-add:** Enables rapid, visual review and transparent failure analysis

## 4. Challenges & Solutions

### CPU Training Speed
- **Problem:** Slow training on CPU
- **Solution:** Frozen backbone, lightweight head, batch size 2

### Small/Thin Objects
- **Problem:** Low IoU for Flowers, Logs
- **Solution:** Recommend class weighting, focal loss, stronger augmentation

### Class Confusion
- **Problem:** Dry vs. Lush bushes
- **Solution:** DINOv2 features, recommend fine-tuning last 2 blocks, stronger augmentation

### Inference Speed vs. Accuracy
- **Problem:** Need <50ms/image
- **Solution:** Current CPU benchmark fails requirement; consider GPU or model optimization

## 5. Optimizations
- **Transfer learning** (DINOv2 backbone)
- **Lightweight segmentation head**
- **Frozen backbone**
- **Input normalization**

## 6. Failure Case Analysis

Failure analysis is **not computed** in this report. The current `results/failure_analysis.json`
is a placeholder unless regenerated from model outputs.

### Recommendations
- **Short term:** Class weighting, more epochs, data augmentation
- **Medium term:** Fine-tune backbone, ensembling, post-processing
- **Long term:** Domain adaptation, multi-task learning

## 7. Conclusion & Future Work
- **Achievements:**
  - Reproducible segmentation baseline
  - Clear documentation and packaging
- **Next Steps:**
  - Improve accuracy (IoU 0.2700 is low baseline)
  - Optimize inference speed for <50 ms requirement

## 8. Appendix
- See `README.md` for setup and reproduction
- See `JUDGE_README.md` for evaluation instructions
- All scripts, configs, and results included in submission.zip

---

*This report was generated on February 7, 2026. For any queries, refer to the included documentation or contact the team.*
