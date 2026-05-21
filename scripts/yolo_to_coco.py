"""Convert a Roboflow YOLOv8 detection dataset to COCO JSON.

Expected layout:

    dataset/
      data.yaml
      train/images, train/labels
      valid/images, valid/labels
      test/images, test/labels
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image


IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def read_names(data_yaml: Path) -> list[str]:
    text = data_yaml.read_text(encoding="utf-8")
    for line in text.splitlines():
        if line.strip().startswith("names:"):
            raw = line.split(":", 1)[1].strip()
            return [x.strip().strip("'\"") for x in raw.strip("[]").split(",") if x.strip()]
    return ["solar-panel"]


def convert_split(root: Path, split: str, names: list[str]) -> dict:
    img_dir = root / split / "images"
    label_dir = root / split / "labels"
    images = []
    annotations = []
    ann_id = 1

    image_paths = sorted(p for p in img_dir.iterdir() if p.suffix.lower() in IMAGE_SUFFIXES)
    for img_id, img_path in enumerate(image_paths, start=1):
        with Image.open(img_path) as img:
            width, height = img.size

        images.append(
            {
                "id": img_id,
                "file_name": img_path.name,
                "width": width,
                "height": height,
            }
        )

        label_path = label_dir / f"{img_path.stem}.txt"
        if not label_path.exists():
            continue

        for raw in label_path.read_text(encoding="utf-8").splitlines():
            parts = raw.strip().split()
            if len(parts) < 5:
                continue
            cls, xc, yc, bw, bh = int(float(parts[0])), *map(float, parts[1:5])
            x = (xc - bw / 2) * width
            y = (yc - bh / 2) * height
            w = bw * width
            h = bh * height
            x = max(0.0, min(x, width - 1))
            y = max(0.0, min(y, height - 1))
            w = max(0.0, min(w, width - x))
            h = max(0.0, min(h, height - y))
            if w <= 0 or h <= 0:
                continue
            annotations.append(
                {
                    "id": ann_id,
                    "image_id": img_id,
                    "category_id": cls + 1,
                    "bbox": [round(x, 3), round(y, 3), round(w, 3), round(h, 3)],
                    "area": round(w * h, 3),
                    "iscrowd": 0,
                }
            )
            ann_id += 1

    return {
        "images": images,
        "annotations": annotations,
        "categories": [{"id": idx + 1, "name": name} for idx, name in enumerate(names)],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--out-dir", default="annotations", type=Path)
    args = parser.parse_args()

    root = args.root.resolve()
    names = read_names(root / "data.yaml")
    out_dir = root / args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    for split in ("train", "valid", "test"):
        data = convert_split(root, split, names)
        out_file = out_dir / f"{split}_coco.json"
        out_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(
            f"{split}: images={len(data['images'])} "
            f"annotations={len(data['annotations'])} -> {out_file}"
        )


if __name__ == "__main__":
    main()
