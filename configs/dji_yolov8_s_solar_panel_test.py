"""MMYOLO YOLOv8-s test config for solar-panel detection."""

_base_ = "./dji_yolov8_s_solar_panel_finetune.py"

data_root = "D:/path/to/solar_panel_dataset/"
test_ann_file = "annotations/test_coco.json"
test_data_prefix = "test/images/"

class_name = ("solar-panel",)
metainfo = dict(classes=class_name)

test_dataloader = dict(
    batch_size=4,
    num_workers=0,
    persistent_workers=False,
    dataset=dict(
        metainfo=metainfo,
        data_root=data_root,
        ann_file=test_ann_file,
        data_prefix=dict(img=test_data_prefix),
    ),
)

test_evaluator = dict(ann_file=data_root + test_ann_file)
