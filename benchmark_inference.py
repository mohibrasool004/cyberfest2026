#!/usr/bin/env python3
"""
Inference Speed Benchmark Script
Measures inference time for the segmentation model
Ensures < 50ms requirement is met
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import time
from PIL import Image
import cv2
import os
from pathlib import Path
import json

# Set random seed for reproducibility
torch.manual_seed(42)
np.random.seed(42)


class SegmentationHeadConvNeXt(nn.Module):
    """Lightweight ConvNeXt-style head for segmentation."""
    def __init__(self, in_channels=384, hidden_channels=128, num_classes=11):
        super().__init__()
        self.norm = nn.LayerNorm(in_channels)
        self.conv_stem = nn.Conv2d(in_channels, hidden_channels, kernel_size=7, padding=3)
        self.gelu = nn.GELU()
        
        # ConvNeXt blocks
        self.block1 = nn.Sequential(
            nn.Conv2d(hidden_channels, hidden_channels, kernel_size=7, padding=3, groups=hidden_channels),
            nn.GELU(),
            nn.Conv2d(hidden_channels, hidden_channels, kernel_size=1)
        )
        
        self.classifier = nn.Conv2d(hidden_channels, num_classes, kernel_size=1)
    
    def forward(self, x):
        """
        x: [B, N, 384] patch tokens from DINOv2
        Returns: [B, num_classes, H, W] logits
        """
        # Reshape to 2D
        B, N, C = x.shape
        # For DINOv2 ViT-S/14 with 476x938 input:
        # patch_h = ceil(476 / 14) = 35, patch_w = ceil(938 / 14) = 68
        # N = 35 * 68 = 2380, but actual may vary with padding
        # Infer H, W more carefully: assume approximately rectangular
        H = int(np.sqrt(N * 0.5))  # start with aspect ~2:1
        W = (N + H - 1) // H  # ensure coverage
        # Pad if necessary
        padded_size = H * W
        if padded_size > N:
            x_padded = torch.zeros(B, padded_size, C, dtype=x.dtype, device=x.device)
            x_padded[:, :N, :] = x
            x = x_padded
        x = x.reshape(B, H, W, C).permute(0, 3, 1, 2)  # [B, C, H, W]
        
        # Normalize
        x = self.norm(x.permute(0, 2, 3, 1)).permute(0, 3, 1, 2)
        
        # Stem
        x = self.conv_stem(x)
        x = self.gelu(x)
        
        # ConvNeXt blocks
        x = x + self.block1(x)
        
        # Classifier
        x = self.classifier(x)
        return x


def load_test_image(image_path, size=(476, 938)):
    """Load and preprocess a test image."""
    image = Image.open(image_path).convert("RGB")
    image = image.resize(size)
    
    # Normalize using ImageNet stats
    img_array = np.array(image).astype(np.float32) / 255.0
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])
    img_array = (img_array - mean) / std
    
    # Convert to tensor
    img_tensor = torch.from_numpy(img_array).permute(2, 0, 1).unsqueeze(0)
    return img_tensor


def benchmark_inference(model, backbone, test_image_dir=None, num_iterations=10):
    """
    Benchmark inference speed on CPU and GPU.
    
    Args:
        model: Segmentation head
        backbone: DINOv2 backbone
        test_image_dir: Directory with test images
        num_iterations: Number of iterations for averaging
    
    Returns:
        dict with timing statistics
    """
    
    print("\n" + "="*80)
    print("INFERENCE SPEED BENCHMARK")
    print("="*80)
    
    results = {
        'cpu': {'times': [], 'mean': 0, 'std': 0, 'min': 0, 'max': 0},
        'gpu': {'times': [], 'mean': 0, 'std': 0, 'min': 0, 'max': 0} if torch.cuda.is_available() else None,
        'requirement': '<50ms',
        'status': 'UNKNOWN'
    }
    
    # Create dummy input (476x938 image)
    dummy_input = torch.randn(1, 3, 476, 938)
    
    # ============================================================================
    # CPU Benchmark
    # ============================================================================
    print("\n[1/2] Benchmarking on CPU...")
    model.to('cpu')
    backbone.to('cpu')
    model.eval()
    backbone.eval()
    
    cpu_times = []
    
    with torch.no_grad():
        # Warm up
        for _ in range(3):
            _ = backbone.forward_features(dummy_input.to('cpu'))
        
        # Actual benchmark
        for i in range(num_iterations):
            input_batch = dummy_input.to('cpu')
            
            # Total time: backbone + head + upsampling
            start = time.perf_counter()
            
            # Backbone forward pass
            features = backbone.forward_features(input_batch)["x_norm_patchtokens"]  # [B, N, 384]
            
            # Head forward pass
            logits = model(features)  # [B, 11, H, W]
            
            # Upsample to original size
            output = F.interpolate(logits, size=(476, 938), mode='bilinear', align_corners=False)
            
            end = time.perf_counter()
            elapsed_ms = (end - start) * 1000
            cpu_times.append(elapsed_ms)
            
            print(f"  Iteration {i+1}/{num_iterations}: {elapsed_ms:.2f} ms")
    
    results['cpu']['times'] = cpu_times
    results['cpu']['mean'] = np.mean(cpu_times)
    results['cpu']['std'] = np.std(cpu_times)
    results['cpu']['min'] = np.min(cpu_times)
    results['cpu']['max'] = np.max(cpu_times)
    
    print(f"\n[OK] CPU Results:")
    print(f"  Mean:   {results['cpu']['mean']:.2f} ms")
    print(f"  Std:    {results['cpu']['std']:.2f} ms")
    print(f"  Min:    {results['cpu']['min']:.2f} ms")
    print(f"  Max:    {results['cpu']['max']:.2f} ms")
    
    # ============================================================================
    # GPU Benchmark (if available)
    # ============================================================================
    if torch.cuda.is_available():
        print("\n[2/2] Benchmarking on GPU...")
        model.to('cuda')
        backbone.to('cuda')
        
        gpu_times = []
        
        with torch.no_grad():
            # Warm up
            for _ in range(3):
                _ = backbone.forward_features(dummy_input.to('cuda'))
            
            # Synchronize
            if torch.cuda.is_available():
                torch.cuda.synchronize()
            
            # Actual benchmark
            for i in range(num_iterations):
                input_batch = dummy_input.to('cuda')
                
                if torch.cuda.is_available():
                    torch.cuda.synchronize()
                start = time.perf_counter()
                
                # Backbone forward pass
                features = backbone.forward_features(input_batch)["x_norm_patchtokens"]
                
                # Head forward pass
                logits = model(features)
                
                # Upsample to original size
                output = F.interpolate(logits, size=(476, 938), mode='bilinear', align_corners=False)
                
                if torch.cuda.is_available():
                    torch.cuda.synchronize()
                end = time.perf_counter()
                elapsed_ms = (end - start) * 1000
                gpu_times.append(elapsed_ms)
                
                print(f"  Iteration {i+1}/{num_iterations}: {elapsed_ms:.2f} ms")
        
        results['gpu']['times'] = gpu_times
        results['gpu']['mean'] = np.mean(gpu_times)
        results['gpu']['std'] = np.std(gpu_times)
        results['gpu']['min'] = np.min(gpu_times)
        results['gpu']['max'] = np.max(gpu_times)
        
        print(f"\n[OK] GPU Results:")
        print(f"  Mean:   {results['gpu']['mean']:.2f} ms")
        print(f"  Std:    {results['gpu']['std']:.2f} ms")
        print(f"  Min:    {results['gpu']['min']:.2f} ms")
        print(f"  Max:    {results['gpu']['max']:.2f} ms")
    
    # ============================================================================
    # Verification
    # ============================================================================
    print("\n" + "="*80)
    print("VERIFICATION")
    print("="*80)
    
    cpu_pass = results['cpu']['mean'] < 50
    print(f"\n[OK] CPU Mean: {results['cpu']['mean']:.2f} ms")
    print(f"  Requirement: < 50 ms")
    print(f"  Status: {'PASS' if cpu_pass else 'FAIL'}")
    
    if results['gpu'] is not None:
        gpu_pass = results['gpu']['mean'] < 50
        print(f"\n[OK] GPU Mean: {results['gpu']['mean']:.2f} ms")
        print(f"  Requirement: < 50 ms")
        print(f"  Status: {'PASS' if gpu_pass else 'FAIL'}")
    
    # Overall status
    overall_pass = cpu_pass and (results['gpu'] is None or results['gpu']['mean'] < 50)
    results['status'] = 'PASS' if overall_pass else 'FAIL'
    
    print("\n" + "="*80)
    print(f"OVERALL STATUS: {'PASS' if overall_pass else 'FAIL'}")
    print("="*80)
    
    return results


def main():
    """Main benchmark function."""
    
    print("\nLoading model components...")
    
    # Load backbone
    print("  Loading DINOv2 backbone...")
    BACKBONE_SIZE = "small"
    backbone_arch = "vits14"
    backbone_name = f"dinov2_{backbone_arch}"
    backbone = torch.hub.load(repo_or_dir="facebookresearch/dinov2", model=backbone_name)
    print(f"  [OK] Backbone loaded: {backbone_name}")
    
    # Load head
    print("  Loading segmentation head...")
    head = SegmentationHeadConvNeXt(in_channels=384, hidden_channels=128, num_classes=11)
    print("  [OK] Head loaded")
    
    # Run benchmark
    results = benchmark_inference(
        model=head,
        backbone=backbone,
        num_iterations=10
    )
    
    # Save results
    print("\n" + "="*80)
    print("SAVING RESULTS")
    print("="*80)
    
    results_file = Path('results/inference_benchmark.json')
    results_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Convert numpy types to Python types for JSON serialization
    results_json = {
        'cpu': {
            'mean': float(results['cpu']['mean']),
            'std': float(results['cpu']['std']),
            'min': float(results['cpu']['min']),
            'max': float(results['cpu']['max']),
        },
        'requirement': '<50ms',
        'status': results['status'],
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    if results['gpu'] is not None:
        results_json['gpu'] = {
            'mean': float(results['gpu']['mean']),
            'std': float(results['gpu']['std']),
            'min': float(results['gpu']['min']),
            'max': float(results['gpu']['max']),
        }
    
    with open(results_file, 'w') as f:
        json.dump(results_json, f, indent=2)
    
    print(f"\n[OK] Results saved to: {results_file}")
    print(f"\n Summary:")
    print(f"  CPU Mean:     {results['cpu']['mean']:.2f} ms PASS" if results['cpu']['mean'] < 50 else f"  CPU Mean:     {results['cpu']['mean']:.2f} ms FAIL")
    print(f"  Requirement:  < 50 ms")
    print(f"  Status:       {'PASS' if results['status'] == 'PASS' else 'FAIL'}")


if __name__ == '__main__':
    main()



