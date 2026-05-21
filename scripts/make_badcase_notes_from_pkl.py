"""Create a CSV template for visual badcase review from an MMYOLO pkl file."""

from __future__ import annotations

import argparse
import csv
import pickle
from pathlib import Path
from typing import Any


def to_list(value: Any) -> list:
    if hasattr(value, "detach"):
        value = value.detach().cpu()
    if hasattr(value, "numpy"):
        value = value.numpy()
    if hasattr(value, "tolist"):
        return value.tolist()
    return list(value)


def iou(a: list[float], b: list[float]) -> float:
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b
    ix1, iy1 = max(ax1, bx1), max(ay1, by1)
    ix2, iy2 = min(ax2, bx2), min(ay2, by2)
    inter = max(0.0, ix2 - ix1) * max(0.0, iy2 - iy1)
    area_a = max(0.0, ax2 - ax1) * max(0.0, ay2 - ay1)
    area_b = max(0.0, bx2 - bx1) * max(0.0, by2 - by1)
    union = area_a + area_b - inter
    return inter / union if union > 0 else 0.0


def analyze(sample: dict[str, Any], score_thr: float, iou_thr: float) -> dict[str, Any]:
    preds = sample["pred_instances"]
    gts = sample["gt_instances"]
    pred_boxes = to_list(preds["bboxes"])
    scores = to_list(preds["scores"])
    gt_boxes = to_list(gts["bboxes"])
    pred_indices = sorted(
        [i for i, score in enumerate(scores) if score >= score_thr],
        key=lambda i: scores[i],
        reverse=True,
    )
    matched_gt: set[int] = set()
    fp_boxes = []
    for pred_idx in pred_indices:
        best_gt, best_iou = -1, 0.0
        for gt_idx, gt_box in enumerate(gt_boxes):
            if gt_idx in matched_gt:
                continue
            cur = iou(pred_boxes[pred_idx], gt_box)
            if cur > best_iou:
                best_iou = cur
                best_gt = gt_idx
        if best_gt >= 0 and best_iou >= iou_thr:
            matched_gt.add(best_gt)
        else:
            fp_boxes.append((pred_boxes[pred_idx], scores[pred_idx], best_iou))
    fn = len(gt_boxes) - len(matched_gt)
    return {
        "img_id": sample.get("img_id"),
        "img_path": sample.get("img_path", ""),
        "gt_count": len(gt_boxes),
        "pred_count": len(pred_indices),
        "fp_count": len(fp_boxes),
        "fn_count": fn,
        "max_fp_score": max([x[1] for x in fp_boxes], default=""),
        "max_fp_iou": max([x[2] for x in fp_boxes], default=""),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pkl", required=True, type=Path)
    parser.add_argument("--vis-dir", required=True)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--score-thr", type=float, default=0.0)
    parser.add_argument("--iou-thr", type=float, default=0.5)
    parser.add_argument("--only-badcase", action="store_true")
    args = parser.parse_args()

    with args.pkl.open("rb") as f:
        data = pickle.load(f)

    rows = []
    for sample in data:
        row = analyze(sample, args.score_thr, args.iou_thr)
        filename = Path(row["img_path"]).name
        row["vis_path"] = str(Path(args.vis_dir) / filename)
        if args.only_badcase and row["fp_count"] == 0 and row["fn_count"] == 0:
            continue
        rows.append(row)

    rows.sort(key=lambda r: (r["fp_count"] + r["fn_count"], r["fp_count"]), reverse=True)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", newline="", encoding="utf-8-sig") as f:
        fieldnames = [
            "img_id",
            "vis_path",
            "img_path",
            "gt_count",
            "pred_count",
            "fp_count",
            "fn_count",
            "max_fp_score",
            "max_fp_iou",
            "badcase_type",
            "negative_sample_description",
            "cause",
            "action",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    **row,
                    "badcase_type": "",
                    "negative_sample_description": "",
                    "cause": "",
                    "action": "",
                }
            )
    print(f"rows={len(rows)}")
    print(args.out)


if __name__ == "__main__":
    main()
