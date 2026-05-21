"""MMYOLO YOLOv8-s fine-tuning config for solar-panel detection.

Copy this file into `mmyolo/configs/yolov8/` before running training.
Set `data_root` and `load_from` to local paths in your environment.
"""

_base_ = "./yolov8_s_syncbn_fast_8xb16-500e_coco.py"

data_root = "D:/path/to/solar_panel_dataset/"
train_ann_file = "annotations/train_coco.json"
train_data_prefix = "train/images/"
val_ann_file = "annotations/valid_coco.json"
val_data_prefix = "valid/images/"
test_ann_file = "annotations/test_coco.json"
test_data_prefix = "test/images/"

num_classes = 1
class_name = ("solar-panel",)
metainfo = dict(classes=class_name)

train_batch_size_per_gpu = 4
train_num_workers = 0
val_batch_size_per_gpu = 4
val_num_workers = 0
persistent_workers = False

img_scale = (640, 640)
affine_scale = 0.20
max_aspect_ratio = 100

max_epochs = 30
val_interval = 1
base_lr = 0.0002

load_from = "checkpoints/solar_colleague.pth"
work_dir = "./work_dirs/dji_yolov8_s_solar_panel_finetune"

model = dict(
    bbox_head=dict(head_module=dict(num_classes=num_classes)),
    train_cfg=dict(assigner=dict(num_classes=num_classes)),
)

pre_transform = [
    dict(type="LoadImageFromFile", backend_args=None),
    dict(type="LoadAnnotations", with_bbox=True),
]

train_pipeline = [
    *pre_transform,
    dict(type="YOLOv5KeepRatioResize", scale=img_scale),
    dict(type="LetterResize", scale=img_scale, allow_scale_up=True, pad_val=dict(img=114.0)),
    dict(
        type="YOLOv5RandomAffine",
        max_rotate_degree=0.0,
        max_shear_degree=0.0,
        scaling_ratio_range=(1 - affine_scale, 1 + affine_scale),
        max_aspect_ratio=max_aspect_ratio,
        border_val=(114, 114, 114),
    ),
    dict(type="YOLOv5HSVRandomAug"),
    dict(type="mmdet.RandomFlip", prob=0.5),
    dict(
        type="mmdet.PackDetInputs",
        meta_keys=("img_id", "img_path", "ori_shape", "img_shape", "flip", "flip_direction"),
    ),
]

train_dataloader = dict(
    batch_size=train_batch_size_per_gpu,
    num_workers=train_num_workers,
    persistent_workers=persistent_workers,
    dataset=dict(
        metainfo=metainfo,
        data_root=data_root,
        ann_file=train_ann_file,
        data_prefix=dict(img=train_data_prefix),
        filter_cfg=dict(filter_empty_gt=False, min_size=16),
        pipeline=train_pipeline,
    ),
)

val_dataloader = dict(
    batch_size=val_batch_size_per_gpu,
    num_workers=val_num_workers,
    persistent_workers=persistent_workers,
    dataset=dict(
        metainfo=metainfo,
        data_root=data_root,
        ann_file=val_ann_file,
        data_prefix=dict(img=val_data_prefix),
    ),
)

test_dataloader = dict(
    batch_size=val_batch_size_per_gpu,
    num_workers=val_num_workers,
    persistent_workers=persistent_workers,
    dataset=dict(
        metainfo=metainfo,
        data_root=data_root,
        ann_file=test_ann_file,
        data_prefix=dict(img=test_data_prefix),
    ),
)

val_evaluator = dict(ann_file=data_root + val_ann_file)
test_evaluator = dict(ann_file=data_root + test_ann_file)

train_cfg = dict(max_epochs=max_epochs, val_interval=val_interval)

optim_wrapper = dict(optimizer=dict(lr=base_lr, batch_size_per_gpu=train_batch_size_per_gpu))

default_hooks = dict(
    checkpoint=dict(interval=1, max_keep_ckpts=3, save_best="auto", type="CheckpointHook"),
    logger=dict(interval=20, type="LoggerHook"),
    param_scheduler=dict(
        lr_factor=0.01,
        max_epochs=max_epochs,
        scheduler_type="linear",
        type="YOLOv5ParamSchedulerHook",
    ),
    sampler_seed=dict(type="DistSamplerSeedHook"),
    timer=dict(type="IterTimerHook"),
    visualization=dict(type="mmdet.DetVisualizationHook"),
)

custom_hooks = [
    dict(
        type="EMAHook",
        ema_type="ExpMomentumEMA",
        momentum=0.0001,
        update_buffers=True,
        strict_load=False,
        priority=49,
    )
]
