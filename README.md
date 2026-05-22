# Solar Panel Detection with YOLOv8 and MMYOLO

[中文](#中文版本) | [English](#english-version)

---

## 中文版本

本项目是一个面向无人机航拍场景的太阳能板目标检测实习项目。项目基于 MMYOLO / YOLOv8 完成数据集转换、模型训练与微调、验证测试、badcase 分析。

> 说明：本仓库只公开项目代码、配置模板和实验报告，不包含私有数据集、模型权重、量化标定图片或内部文档。

### 项目目标

- 使用 YOLOv8 检测航拍图像中的太阳能板区域。
- 将 Roboflow YOLOv8 格式数据转换为 MMYOLO 可用的 COCO 格式。
- 基于已有 YOLOv8-s 检测模型进行评估和小数据集适配实验。
- 记录 mAP、mAP50、mAP75、误检、漏检和 badcase 原因。
- 整理 DJI 开发者平台量化所需文件清单和参数。

### 仓库结构

```text
.
├── configs/                 # MMYOLO 配置模板
├── scripts/                 # 数据转换与 badcase 分析脚本
├── reports/                 # 实验记录和结果分析
├── docs/                    # DJI 量化交付说明
├── assets/                  # 预留示例图片位置，不存放私有数据
├── requirements.txt
└── README.md
```

### 环境

本项目实验环境：

```text
Windows 10/11
Python 3.8
PyTorch 2.0.0
TorchVision 0.15.0
MMEngine 0.10.7
MMDetection 3.3.0
MMCV 2.0.0
MMYOLO 0.6.0
GPU: NVIDIA RTX 4070 Laptop GPU
```

### 数据格式

原始数据采用 Roboflow 导出的 YOLOv8 格式：

```text
dataset/
├── data.yaml
├── train/
│   ├── images/
│   └── labels/
├── valid/
│   ├── images/
│   └── labels/
└── test/
    ├── images/
    └── labels/
```

通过 `scripts/yolo_to_coco.py` 转换为 COCO：

```powershell
python scripts/yolo_to_coco.py --root D:\path\to\dataset
```

生成：

```text
dataset/annotations/train_coco.json
dataset/annotations/valid_coco.json
dataset/annotations/test_coco.json
```

### 训练示例

在 MMYOLO 根目录中运行：

```powershell
conda run --live-stream -n dji-mmyolo python tools\train.py ^
  configs\yolov8\dji_yolov8_s_solar_panel_finetune.py ^
  --work-dir work_dirs\dji_yolov8_s_solar_panel_finetune
```

### 测试示例

```powershell
conda run --live-stream -n dji-mmyolo python tools\test.py ^
  configs\yolov8\dji_yolov8_s_solar_panel_test.py ^
  checkpoints\solar_colleague.pth ^
  --work-dir work_dirs\test_solar_panel ^
  --show-dir work_dirs\test_solar_panel\pred_vis
```

### 主要实验结论

当前最稳定的主模型是同事提供的太阳能板检测模型，并在固定测试集上取得较高精度。后续小数据集微调能够在对应小数据集上提升指标，但跨新场景泛化能力不足。

简要结果：

| 模型/测试集 | mAP | mAP50 | 结论 |
| --- | ---: | ---: | --- |
| 主模型固定测试集 | 约 0.977 | 1.000 | 当前最稳定 |
| 小数据集微调后 test | 0.285 | 0.663 | 对该小集有提升 |
| 新外部数据集 test | 0.011 | 0.092 | 泛化不足 |

### DJI 量化交付

根据 DJI AI 算力开放平台 YOLOv8 适配说明，量化交付通常需要：

- `.pth` 模型权重
- 500-1000 张量化标定图片
- 类别名称
- 输出框相关参数，如 `score_thr`、`nms_pre`、`iou_threshold`、`max_per_img`
- 训练配置快照

本项目整理的推荐参数见 [docs/dji_quantization_package.md](docs/dji_quantization_package.md)。

### 不公开内容

以下内容不上传 GitHub：

- 模型权重：`*.pth`
- 原始数据集图片和标签
- 量化标定图片
- DJI 内部或老师提供的文档
- 本机绝对路径和私有日志

### 致谢

本项目基于 OpenMMLab 的 MMYOLO / MMDetection / MMEngine 生态完成。项目中的配置和脚本用于太阳能板检测任务适配、实验记录和工程交付整理。

---

## English Version

This project is an internship project for solar panel target detection in UAV aerial photography scenarios. The project is based on MMYOLO / YOLOv8 to complete dataset conversion, model training and fine-tuning, validation testing, and badcase analysis.

> Note: This repository only publishes project code, configuration templates, and experimental reports. It does not include private datasets, model weights, quantization calibration images, or internal documents.

### Project Objectives

- Detect solar panel regions in aerial images using YOLOv8.
- Convert Roboflow YOLOv8 format data to COCO format compatible with MMYOLO.
- Evaluate and conduct small dataset adaptation experiments based on the existing YOLOv8-s detection model.
- Record mAP, mAP50, mAP75, false positives, false negatives, and badcase analysis.
- Organize the file checklist and parameters required for DJI developer platform quantization.

### Repository Structure

```text
.
├── configs/                 # MMYOLO configuration templates
├── scripts/                 # Data conversion and badcase analysis scripts
├── reports/                 # Experimental records and results analysis
├── docs/                    # DJI quantization delivery documentation
├── assets/                  # Reserved location for sample images, no private data stored
├── requirements.txt
└── README.md
```

### Environment

This project experimental environment:

```text
Windows 10/11
Python 3.8
PyTorch 2.0.0
TorchVision 0.15.0
MMEngine 0.10.7
MMDetection 3.3.0
MMCV 2.0.0
MMYOLO 0.6.0
GPU: NVIDIA RTX 4070 Laptop GPU
```

### Data Format

The original data is exported from Roboflow in YOLOv8 format:

```text
dataset/
├── data.yaml
├── train/
│   ├── images/
│   └── labels/
├── valid/
│   ├── images/
│   └── labels/
└── test/
    ├── images/
    └── labels/
```

Convert to COCO format using `scripts/yolo_to_coco.py`:

```powershell
python scripts/yolo_to_coco.py --root D:\path\to\dataset
```

Generated files:

```text
dataset/annotations/train_coco.json
dataset/annotations/valid_coco.json
dataset/annotations/test_coco.json
```

### Training Example

Run in the MMYOLO root directory:

```powershell
conda run --live-stream -n dji-mmyolo python tools\train.py ^
  configs\yolov8\dji_yolov8_s_solar_panel_finetune.py ^
  --work-dir work_dirs\dji_yolov8_s_solar_panel_finetune
```

### Testing Example

```powershell
conda run --live-stream -n dji-mmyolo python tools\test.py ^
  configs\yolov8\dji_yolov8_s_solar_panel_test.py ^
  checkpoints\solar_colleague.pth ^
  --work-dir work_dirs\test_solar_panel ^
  --show-dir work_dirs\test_solar_panel\pred_vis
```

### Main Experimental Conclusions

The current most stable main model is the solar panel detection model provided by colleagues, and achieves high accuracy on the fixed test set. Subsequent fine-tuning on small datasets can improve metrics on the corresponding small dataset, but generalization to new scenes is insufficient.

Brief results:

| Model/Test Set | mAP | mAP50 | Conclusion |
| --- | ---: | ---: | --- |
| Main model on fixed test set | ~0.977 | 1.000 | Currently most stable |
| After fine-tuning on small dataset | 0.285 | 0.663 | Improvement on that small set |
| New external dataset test | 0.011 | 0.092 | Insufficient generalization |

### DJI Quantization Delivery

According to the DJI AI Computing Open Platform YOLOv8 adaptation guide, quantization delivery typically requires:

- `.pth` model weights
- 500-1000 calibration images for quantization
- Class names
- Output box related parameters, such as `score_thr`, `nms_pre`, `iou_threshold`, `max_per_img`
- Training configuration snapshot

The recommended parameters organized in this project can be found in [docs/dji_quantization_package.md](docs/dji_quantization_package.md).

### Non-public Content

The following content is not uploaded to GitHub:

- Model weights: `*.pth`
- Original dataset images and labels
- Quantization calibration images
- DJI internal or instructor-provided documents
- Local absolute paths and private logs

### Acknowledgments

This project is completed based on OpenMMLab's MMYOLO / MMDetection / MMEngine ecosystem. The configurations and scripts in this project are used for solar panel detection task adaptation, experimental record keeping, and engineering delivery organization.
