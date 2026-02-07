import os
import re
import json
from pathlib import Path

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import shutil


def find_project_root():
    p = Path(__file__).resolve().parent
    # walk upward looking for common repo markers
    for _ in range(6):
        if (p / 'dataset').exists() or (p / 'submission.zip').exists() or (p / '.git').exists():
            return p
        p = p.parent
    # fallback to two levels up
    return Path(__file__).resolve().parent.parent


ROOT = find_project_root()
STATS_DIR = ROOT / 'dataset' / 'train_stats'


def read_key_values_txt(path):
    data = {}
    if not path.exists():
        return data
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # try key: value or key = value or CSV-like
            m = re.match(r"^([^:=]+)[:=]\s*(.+)$", line)
            if m:
                k = m.group(1).strip()
                v = m.group(2).strip()
                try:
                    data[k] = float(v)
                except Exception:
                    data[k] = v
            else:
                parts = [p.strip() for p in line.split(',') if p.strip()]
                if len(parts) == 2:
                    k, v = parts
                    try:
                        data[k] = float(v)
                    except Exception:
                        data[k] = v
    return data


def load_benchmark():
    # look in project root, then results/
    candidates = [ROOT / 'benchmark_results.json', ROOT / 'results' / 'inference_benchmark.json', ROOT / 'results' / 'inference_benchmark.json']
    for p in candidates:
        if p.exists():
            try:
                return json.loads(p.read_text(encoding='utf-8'))
            except Exception:
                return None
    return None


def list_failure_images():
    # Search both train_stats/failure_examples and results/ for images
    imgs = []
    # 1) explicit list file (registered sample paths)
    list_file = STATS_DIR / 'failure_examples_paths.json'
    if list_file.exists():
        try:
            data = json.loads(list_file.read_text(encoding='utf-8'))
            for p in data:
                pp = Path(p)
                if not pp.is_absolute():
                    pp = ROOT / p
                if pp.exists():
                    imgs.append(pp)
        except Exception:
            pass

    # 2) copied images folder
    folder1 = STATS_DIR / 'failure_examples'
    if folder1.exists():
        imgs.extend(sorted(folder1.glob('*')))

    # 3) results/ (any images)
    folder2 = ROOT / 'results'
    if folder2.exists():
        imgs.extend(sorted([p for p in folder2.glob('**/*') if p.suffix.lower() in ['.png', '.jpg', '.jpeg']]))

    return imgs


def main():
    st.set_page_config(page_title='Training Dashboard', layout='wide')
    st.title('Model Training Dashboard')

    # Left: controls
    with st.sidebar:
        st.header('Controls')
        show_training = st.checkbox('Show training curves', value=True)
        show_perclass = st.checkbox('Show per-class metrics', value=True)
        show_failures = st.checkbox('Show failure examples', value=True)
        show_benchmark = st.checkbox('Show benchmark', value=True)
        show_submission = st.checkbox('Submission checklist', value=True)

    # Top row: key metrics
    col1, col2, col3 = st.columns([1, 1, 1])
    metrics = read_key_values_txt(STATS_DIR / 'evaluation_metrics.txt')
    with col1:
        st.subheader('Final Metrics')
        if metrics:
            for k in ['Val IoU', 'Val Loss', 'Dice', 'Accuracy']:
                # try flexible key matches
                found = None
                for key in metrics:
                    if k.lower() in key.lower():
                        found = key
                        break
                if found:
                    st.metric(label=found, value=metrics[found])
        else:
            st.write('No `evaluation_metrics.txt` found or could not parse.')

    with col2:
        st.subheader('Training Artifacts')
        if (STATS_DIR / 'training_curves.png').exists():
            st.image(str(STATS_DIR / 'training_curves.png'), use_column_width=True)
        else:
            st.write('No training curves image found at dataset/train_stats/training_curves.png')

    with col3:
        st.subheader('Submission')
        submission_exists = (ROOT / 'submission.zip').exists()
        ckpt_exists = (ROOT / 'dataset' / 'segmentation_head.pth').exists()
        st.write('submission.zip: %s' % ('[OK]' if submission_exists else '[FAIL]'))
        st.write('checkpoint: %s' % ('[OK]' if ckpt_exists else '[FAIL]'))
        if submission_exists:
            with open(ROOT / 'submission.zip', 'rb') as f:
                st.download_button('Download submission.zip', f, file_name='submission.zip')

    # Per-class metrics
    if show_perclass:
        st.header('Per-class Metrics')
        # Look for per-class JSON in both train_stats and results
        perclass_paths = [STATS_DIR / 'per_class_iou.json', ROOT / 'results' / 'per_class_iou.json']
        perclass_data = None
        for p in perclass_paths:
            if p.exists():
                try:
                    perclass_data = json.loads(p.read_text(encoding='utf-8'))
                    break
                except Exception:
                    perclass_data = None

        # Fallback: synthesize from results/failure_analysis.json
        if perclass_data is None:
            fa = ROOT / 'results' / 'failure_analysis.json'
            if fa.exists():
                try:
                    raw = json.loads(fa.read_text(encoding='utf-8'))
                    perclass_data = {}
                    for case in raw.get('worst_cases', []):
                        for item in case.get('worst_3_classes', []):
                            perclass_data[item['class_name']] = item.get('iou', None)
                except Exception:
                    perclass_data = None

        if perclass_data:
            # Normalize to a DataFrame: keys may be class names or ids
            df = pd.DataFrame.from_dict(perclass_data, orient='index', columns=['IoU'])
            df = df.sort_values(by='IoU', ascending=True)
            st.bar_chart(df['IoU'])
            st.dataframe(df)
        else:
            st.write('`per_class_iou.json` not found in `dataset/train_stats/` or `results/` and could not synthesize from failure analysis.')

            # Provide quick action to regenerate per_class_iou.json from results/failure_analysis.json
            fa_btn = st.button('Regenerate per_class_iou.json from results/failure_analysis.json')
            if fa_btn:
                fa_path = ROOT / 'results' / 'failure_analysis.json'
                out_dir = STATS_DIR
                out_dir.mkdir(parents=True, exist_ok=True)
                out_path = out_dir / 'per_class_iou.json'
                if fa_path.exists():
                    try:
                        raw = json.loads(fa_path.read_text(encoding='utf-8'))
                        perclass = {}
                        for case in raw.get('worst_cases', []):
                            for item in case.get('worst_3_classes', []):
                                perclass[item['class_name']] = item.get('iou', None)
                        with open(out_path, 'w', encoding='utf-8') as f:
                            json.dump(perclass, f, indent=2)
                        st.success(f'Wrote {out_path}')
                    except Exception as e:
                        st.error(f'Failed to synthesize per_class_iou.json: {e}')
                else:
                    st.error('results/failure_analysis.json not found')

            # Provide quick action to copy failure images from results/ to dataset/train_stats/failure_examples
            copy_btn = st.button('Copy failure images from results/ to dataset/train_stats/failure_examples')
            if copy_btn:
                src = ROOT / 'results'
                dst = STATS_DIR / 'failure_examples'
                dst.mkdir(parents=True, exist_ok=True)
                copied = 0
                if src.exists():
                    for p in src.glob('**/*'):
                        if p.suffix.lower() in ['.png', '.jpg', '.jpeg']:
                            try:
                                shutil.copy2(p, dst / p.name)
                                copied += 1
                            except Exception as e:
                                st.warning(f'Failed to copy {p.name}: {e}')
                    st.success(f'Copied {copied} images to {dst}')
                else:
                    st.error('results/ folder not found')

            # Provide quick action to register sample test images as failure examples (no copy)
            register_btn = st.button('Register sample test images as failure examples')
            if register_btn:
                # find sample images under dataset/Offroad_Segmentation_testImages/Segmentation
                sample_dir = ROOT / 'dataset' / 'Offroad_Segmentation_testImages' / 'Segmentation'
                list_file = STATS_DIR / 'failure_examples_paths.json'
                STATS_DIR.mkdir(parents=True, exist_ok=True)
                if sample_dir.exists():
                    imgs = sorted([p for p in sample_dir.glob('*.png')])[:12]
                    rel_paths = [str(p.relative_to(ROOT)) for p in imgs]
                    try:
                        with open(list_file, 'w', encoding='utf-8') as f:
                            json.dump(rel_paths, f, indent=2)
                        st.success(f'Registered {len(rel_paths)} sample images to {list_file}')
                    except Exception as e:
                        st.error(f'Failed to write {list_file}: {e}')
                else:
                    st.error(f'Sample directory not found: {sample_dir}')

    # Failure examples
    if show_failures:
        st.header('Failure Examples')
        imgs = list_failure_images()
        if imgs:
            cols = st.columns(3)
            for i, p in enumerate(imgs[:12]):
                with cols[i % 3]:
                    try:
                        img = Image.open(p)
                        st.image(img, caption=p.name)
                    except Exception:
                        st.write('Failed to open %s' % p.name)
        else:
            st.write('No failure example images found. Showing textual failure analysis instead.')
            fa_path = ROOT / 'results' / 'failure_analysis.json'
            if fa_path.exists():
                try:
                    fa = json.loads(fa_path.read_text(encoding='utf-8'))
                    st.subheader('Summary')
                    st.write(fa.get('status', 'No status'))

                    st.subheader('Worst Cases')
                    for case in fa.get('worst_cases', []):
                        st.markdown(f"**Rank {case.get('rank','[OK]')}  mean IoU: {case.get('mean_iou', '[OK]')}**")
                        # show worst classes table
                        worst = case.get('worst_3_classes', [])
                        if worst:
                            df = pd.DataFrame(worst)
                            st.table(df)
                        # show likely causes and recommendations
                        if case.get('likely_causes'):
                            st.write('Likely causes:')
                            for item in case.get('likely_causes'):
                                st.write('-', item)
                        if case.get('recommendations'):
                            st.write('Recommendations:')
                            for r in case.get('recommendations'):
                                st.write('-', r)
                        st.markdown('---')

                    # Provide raw JSON and download
                    st.subheader('Raw failure_analysis.json')
                    st.json(fa)
                    with open(fa_path, 'rb') as f:
                        st.download_button('Download failure_analysis.json', f, file_name='failure_analysis.json')
                except Exception as e:
                    st.error(f'Failed to read failure_analysis.json: {e}')
            else:
                st.write('No textual failure analysis found in `results/failure_analysis.json`.')

    # Benchmark
    if show_benchmark:
        st.header('Inference Benchmark')
        bench = load_benchmark()
        if bench:
            st.json(bench)
            if 'mean_ms' in bench:
                st.write('Mean per-image (ms):', bench['mean_ms'])
        else:
            st.write('No `benchmark_results.json` found at project root.')

    # Misc: raw logs preview
    st.header('Logs & Raw Files')
    logs = ROOT / 'train_logs' / 'run.log'
    if logs.exists():
        with open(logs, 'r', encoding='utf-8', errors='ignore') as f:
            data = f.read()
            st.text_area('run.log (tail)', value='\n'.join(data.splitlines()[-200:]), height=300)
    else:
        st.write('No `train_logs/run.log` found')

    st.sidebar.markdown('---')
    st.sidebar.write('Paths read:')
    st.sidebar.write(str(STATS_DIR))


if __name__ == '__main__':
    main()


