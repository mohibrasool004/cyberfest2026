# Commands (Accurate as of Feb 7, 2026)

```bash
# Train (re-run)
python dataset/train_segmentation.py

# Evaluate (requires masks)
python dataset/test_segmentation.py --data_dir dataset/Offroad_Segmentation_testImages --output_dir predictions

# Benchmark
python benchmark_inference.py

# Build submission package
python create_submission_package.py
```

