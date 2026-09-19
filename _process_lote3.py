import os
from PIL import Image

SRC = "/tmp/work/site/acropole-capital/_novas_fotos_raw_lote3"
DST = "/tmp/work/site/acropole-capital/src/static/assets/img"
TARGET_W, TARGET_H = 1400, 875  # 16:10

jobs = [
    ("programa-bndes.webp", "programa-bndes.jpg", None),
    ("programa-bndes-2.webp", "programa-bndes-2.jpg", None),
    ("programa-peac-fgi.webp", "programa-peac-fgi.jpg", None),
    ("programa-peac-fgi-2.jpg", "programa-peac-fgi-2.jpg", None),
    ("programa-pronampe.png", "programa-pronampe.jpg", None),
    ("programa-pronampe-2.png", "programa-pronampe-2.jpg", None),
    ("programa-procred-360.png", "programa-procred-360.jpg", None),
    ("programa-procred-360-2.png", "programa-procred-360-2.jpg", None),
]

for src_name, dst_name, extra_crop in jobs:
    src_path = os.path.join(SRC, src_name)
    dst_path = os.path.join(DST, dst_name)
    im = Image.open(src_path).convert("RGB")
    w, h = im.size
    if extra_crop:
        lf, tf, rf, bf = extra_crop
        im = im.crop((round(w*lf), round(h*tf), round(w*(1-rf)), round(h*(1-bf))))
        w, h = im.size
    target_ratio = TARGET_W / TARGET_H
    cur_ratio = w / h
    if cur_ratio > target_ratio:
        new_w = round(h * target_ratio)
        left = (w - new_w) // 2
        im = im.crop((left, 0, left + new_w, h))
    else:
        new_h = round(w / target_ratio)
        top = (h - new_h) // 2
        im = im.crop((0, top, w, top + new_h))
    im = im.resize((TARGET_W, TARGET_H), Image.LANCZOS)
    im.save(dst_path, "JPEG", quality=85, optimize=True)
    print(dst_name, os.path.getsize(dst_path), "bytes")
