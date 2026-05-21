# DJI Quantization Package Notes

This project prepared a DJI quantization handoff package for a YOLOv8-s solar-panel detector.

## Recommended Form Settings

For the current RGB solar-panel model:

```text
Applicable model: Matrice 4 Series
Camera: Visible light
Resolution: 2K
Class enum value: 0
User-side class name: solar-panel
```

Do not select 4K for the current configuration. The current model uses `widen_factor = 0.5`. The DJI adaptation document notes that 4K quantization requires changing `widen_factor` to `0.25`.

## Files to Provide

The DJI handoff package should include:

- `*.pth` checkpoint
- 500-1000 representative calibration images
- Class name file
- Detection output parameters
- Training or evaluation config snapshot
- File manifest

## Detection Parameters

```json
{
  "num_classes": 1,
  "classes": ["solar-panel"],
  "input_size": [640, 640],
  "model_test_cfg": {
    "multi_label": true,
    "nms_pre": 30000,
    "score_thr": 0.001,
    "nms": {
      "type": "nms",
      "iou_threshold": 0.7
    },
    "max_per_img": 300
  }
}
```

## Important Constraints

Keep these model structure parameters consistent with DJI's adapted YOLOv8-s structure:

- `deepen_factor = 0.33`
- `widen_factor = 0.5` for 2K
- `strides = [8, 16, 32]`
- `last_stage_out_channels = 1024`
- `num_det_layers = 3`
- `norm_cfg = dict(type='BN', momentum=0.03, eps=0.001)`

## Safety

Do not publish model weights, calibration images, private datasets, or DJI internal documents in a public GitHub repository.
