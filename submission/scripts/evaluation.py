"""
Test and Evaluation Script
Evaluates the trained model on test images and generates predictions + failure case analysis.
"""

import os
import torch
import numpy as np
from PIL import Image
import cv2
import json
from pathlib import Path
import torch.nn.functional as F

# Class mapping
CLASS_MAP = {
    0: 'Background',
    1: 'Trees',
    2: 'Lush Bushes',
    3: 'Dry Grass',
    4: 'Dry Bushes',
    5: 'Ground Clutter',
    6: 'Flowers',
    7: 'Logs',
    8: 'Rocks',
    9: 'Landscape',
    10: 'Sky'
}

# Color map for visualization (high contrast)
COLOR_MAP = {
    0: (0, 0, 0),           # Background - Black
    1: (0, 200, 0),         # Trees - Green
    2: (0, 255, 0),         # Lush Bushes - Lime
    3: (139, 69, 19),       # Dry Grass - Brown
    4: (210, 105, 30),      # Dry Bushes - Chocolate
    5: (128, 128, 128),     # Ground Clutter - Gray
    6: (255, 0, 255),       # Flowers - Magenta
    7: (165, 42, 42),       # Logs - Brown Red
    8: (192, 192, 192),     # Rocks - Silver
    9: (139, 69, 19),       # Landscape - Saddle Brown
    10: (135, 206, 235)     # Sky - Sky Blue
}

def compute_iou_per_class(pred, target, num_classes=11):
    """Compute IoU for each class."""
    pred = torch.argmax(pred, dim=1) if pred.dim() == 4 else pred
    pred, target = pred.view(-1), target.view(-1)
    
    iou_dict = {}
    for class_id in range(num_classes):
        pred_inds = pred == class_id
        target_inds = target == class_id
        
        intersection = (pred_inds & target_inds).sum().float()
        union = (pred_inds | target_inds).sum().float()
        
        if union == 0:
            iou_dict[class_id] = float('nan')
        else:
            iou_dict[class_id] = (intersection / union).item()
    
    return iou_dict

def visualize_prediction(image, pred_mask, target_mask=None, output_path=None):
    """Visualize prediction overlays on image."""
    # Convert image to uint8 RGB
    if isinstance(image, torch.Tensor):
        image = image.cpu().numpy()
        image = np.moveaxis(image, 0, -1)  # CHW -> HWC
        image = (image * np.array([0.229, 0.224, 0.225]).reshape(1, 1, 3) + 
                 np.array([0.485, 0.456, 0.406]).reshape(1, 1, 3)) * 255
        image = np.uint8(image)
    else:
        image = np.uint8(image)
    
    # Create colored predictions
    pred_colored = np.zeros((*pred_mask.shape, 3), dtype=np.uint8)
    for class_id, color in COLOR_MAP.items():
        mask = pred_mask == class_id
        pred_colored[mask] = color
    
    # Blend
    overlay = cv2.addWeighted(image, 0.6, pred_colored, 0.4, 0)
    
    if target_mask is not None:
        # Create ground truth visualization
        target_colored = np.zeros((*target_mask.shape, 3), dtype=np.uint8)
        for class_id, color in COLOR_MAP.items():
            mask = target_mask == class_id
            target_colored[mask] = color
        
        target_overlay = cv2.addWeighted(image, 0.6, target_colored, 0.4, 0)
        combined = np.hstack([target_overlay, overlay])
        title = "Ground Truth (left) | Prediction (right)"
    else:
        combined = overlay
        title = "Prediction"
    
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        cv2.imwrite(output_path, combined[:, :, ::-1])  # BGR for cv2.imwrite
    
    return combined, title

def test_model(model_path, test_images_dir, output_dir='test_results'):
    """Evaluate model on test images."""
    os.makedirs(output_dir, exist_ok=True)
    
    # Load model (simplified - assumes saved PyTorch model)
    print(f"Loading model from {model_path}...")
    # Note: Real implementation would load the trained model
    print("Model loaded (placeholder)")
    
    # Get test image paths
    test_color_dir = os.path.join(test_images_dir, 'Color_Images')
    test_seg_dir = os.path.join(test_images_dir, 'Segmentation')
    
    if not os.path.exists(test_color_dir):
        print(f"Test color images not found at {test_color_dir}")
        return {}
    
    image_files = sorted(os.listdir(test_color_dir))
    print(f"Found {len(image_files)} test images")
    
    results = {
        'test_images': len(image_files),
        'mean_iou': 0.0,
        'per_class_iou': {},
        'predictions': []
    }
    
    return results

def generate_failure_analysis(results, output_file='failure_analysis.json'):
    """Analyze and report failure cases."""
    analysis = {
        'worst_classes': {},
        'observations': [],
        'recommendations': []
    }
    
    per_class = results.get('per_class_iou', {})
    if per_class:
        sorted_classes = sorted(per_class.items(), key=lambda x: x[1] if not np.isnan(x[1]) else float('-inf'))
        worst = sorted_classes[:3]
        for class_id, iou in worst:
            analysis['worst_classes'][CLASS_MAP.get(class_id, 'Unknown')] = iou
    
    analysis['observations'] = [
        "Small/thin objects (logs, flowers) harder to segment",
        "Background/landscape classes may have overlap",
        "Lighting variations affect dry/lush distinction"
    ]
    
    analysis['recommendations'] = [
        "Apply data augmentation (rotation, brightness, contrast)",
        "Use focal loss or class weights for imbalanced classes",
        "Increase training epochs or model capacity",
        "Post-processing: CRF or morphological operations"
    ]
    
    return analysis

if __name__ == '__main__':
    # Placeholder: Would integrate with actual trained model
    print("Evaluation script ready. To be integrated with trained DINOv2 model.")



