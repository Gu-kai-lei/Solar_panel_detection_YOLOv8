# Workflow

## 1. Prepare MMYOLO

```powershell
git clone https://github.com/open-mmlab/mmyolo.git D:\mmyolo_dji
cd D:\mmyolo_dji
git checkout v0.6.0
```

Install the matching PyTorch, MMCV, MMEngine, MMDetection, and MMYOLO environment according to your machine.

## 2. Convert Dataset

```powershell
python scripts\yolo_to_coco.py --root D:\dataset\solar_panel
```

Copy the generated config files to:

```text
D:\mmyolo_dji\configs\yolov8\
```

## 3. Train

```powershell
cd D:\mmyolo_dji
conda run --live-stream -n dji-mmyolo python tools\train.py ^
  configs\yolov8\dji_yolov8_s_solar_panel_finetune.py ^
  --work-dir work_dirs\dji_yolov8_s_solar_panel_finetune
```

## 4. Test and Visualize

```powershell
conda run --live-stream -n dji-mmyolo python tools\test.py ^
  configs\yolov8\dji_yolov8_s_solar_panel_test.py ^
  checkpoints\solar_colleague.pth ^
  --work-dir work_dirs\test_solar_panel ^
  --show-dir work_dirs\test_solar_panel\pred_vis
```

## 5. Badcase Notes

```powershell
python scripts\make_badcase_notes_from_pkl.py ^
  --pkl work_dirs\test_solar_panel\pred_test.pkl ^
  --vis-dir work_dirs\test_solar_panel\pred_vis ^
  --out reports\badcase_notes.csv ^
  --score-thr 0.25 ^
  --iou-thr 0.5 ^
  --only-badcase
```

## 6. DJI Quantization Handoff

Prepare a private package outside the GitHub repository:

```text
dji_quant_export/
├── model.pth
├── calibration_images/
├── class_names.txt
├── algorithm_params.json
├── configs/
└── README.md
```
