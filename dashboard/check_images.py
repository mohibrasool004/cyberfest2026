from pathlib import Path
from PIL import Image

root = Path(__file__).resolve().parents[1]
imgs_dir = root / 'dataset' / 'train_stats' / 'failure_examples'

print('Checking images in:', imgs_dir)
if not imgs_dir.exists():
    print('Directory does not exist')
    raise SystemExit(1)

files = sorted(imgs_dir.glob('*'))
if not files:
    print('No files found')

for p in files:
    try:
        print(f'[{p.name}] size={p.stat().st_size} bytes - exists: {p.exists()}')
        with Image.open(p) as im:
            im.verify()  # verify does not load full image but checks integrity
        print(f'  OK: {p.name}')
    except Exception as e:
        print(f'  FAILED: {p.name} -> {e}')
