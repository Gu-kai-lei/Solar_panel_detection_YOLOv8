# Badcase Analysis

## Common Error Types

### False Negative

The model misses a real solar panel.

Common causes:

- Target is too small.
- Target is blurred or heavily compressed.
- Strong sunlight reflection changes panel texture.
- Panel is partly occluded.
- Annotation box is much tighter or looser than training data.

### False Positive

The model detects a non-panel object as a solar panel.

Common causes:

- Similar rectangular roof texture.
- Dark roof tiles.
- Shadows with panel-like shape.
- Grass or ground texture with repetitive patterns.
- Cars, awnings, or blue/black roofs.

### Duplicate Boxes

The same panel is detected by several overlapping boxes.

Common causes:

- NMS threshold too high.
- Large panel area is visually split into repeated modules.
- Annotation uses one large box but model predicts several smaller boxes.

## Review Template

| Image | Error Type | Description | Possible Cause | Action |
| --- | --- | --- | --- | --- |
| image_name.jpg | FN / FP / Duplicate | What happened | Why it may happen | Relabel / add negative sample / tune threshold |

## Practical Actions

- If false positives dominate, collect hard negative samples.
- If small targets are missed, add more small target samples and test higher input resolution.
- If boxes are not aligned, check whether annotation policy is consistent.
- If one dataset performs far worse than another, inspect whether its images are screenshots, stretched, or non-aerial.
