# Model Evaluation Summary

## Task

Detect solar panels in RGB aerial or inspection images using YOLOv8-s based on MMYOLO.

## Main Model Choice

The recommended model for deployment or DJI quantization workflow validation is the main solar-panel model checkpoint, not the later small-dataset fine-tuned checkpoint.

Reason:

- The main checkpoint is more stable on the fixed evaluation split.
- The fine-tuned checkpoint improved on one small dataset, but failed to generalize to another external split.
- The external tests show that dataset style and annotation policy strongly affect measured mAP.

## Key Results

| Model / Split | mAP | mAP50 | mAP75 | Notes |
| --- | ---: | ---: | ---: | --- |
| Main model on fixed test split | about 0.977 | 1.000 | about 0.989 | Best overall model |
| Fine-tuned model on small Roboflow test split | 0.285 | 0.663 | 0.229 | Improved over main model on that small split |
| Fine-tuned model on another external test split | 0.011 | 0.092 | 0.000 | Poor generalization |
| Fine-tuned model on another external valid split | 0.039 | 0.065 | 0.051 | Poor generalization |

## Interpretation

The project shows that a good mAP on one dataset is not enough. Solar-panel detection is sensitive to:

- Aerial angle and altitude
- Image source, such as drone video, web image, screenshot, or inspection capture
- Annotation policy, such as full panel area versus panel component
- Resize and stretch preprocessing
- Small objects and strong reflection
- Roof, grass, and shadow textures

## Recommendation

Use the main checkpoint as the stable baseline. Before formal deployment:

1. Build a unified validation set with consistent annotation policy.
2. Review false positives and false negatives visually.
3. Avoid mixing datasets with incompatible labels.
4. Compare FP32 and quantized model outputs after DJI platform quantization.
