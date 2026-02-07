# Post-Training Workflow (Accurate as of Feb 7, 2026)

Training is already complete. Use the steps below if you want to rebuild artifacts.

## 1. Verify Training Artifacts
```bash
ls dataset/train_stats
ls dataset/segmentation_head.pth
```

## 2. Evaluate (Optional)
```bash
python dataset/test_segmentation.py --data_dir dataset/Offroad_Segmentation_testImages --output_dir predictions
```

## 3. Benchmark Inference
```bash
python benchmark_inference.py
```

## 4. Build Submission Package
```bash
python create_submission_package.py
```

## 5. Push Updates
```bash
git add -A
git commit -m "Update docs and metrics for accuracy"
git push
```

