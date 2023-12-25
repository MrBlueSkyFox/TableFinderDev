import os.path

import pytest
import numpy as np
from PIL import Image

from domain.model import TableBox, Cell
from service_layer.table_model import TableDetector
from service_layer.handlers.table_detection import process_output_from_table_detector

PROJECT_DIR = r"D:\PycharmMainProjects\TableFinderDev"
path_to_model = os.path.join(PROJECT_DIR, "models")

model_name = "microsoft/table-transformer-detection"
path_to_image = os.path.join(PROJECT_DIR, "tests\\FIO_1_0.jpg")


def test_find_table():
    excepted_table_box = TableBox(
        Cell(
            150.7137908935547,
            615.0811767578125,
            1472.652099609375,
            1805.0367431640625
        ),
        0.95
    )
    img = Image.open(path_to_image)
    width, height = img.size
    img.resize((int(width * 0.5), int(height * 0.5)))
    table_detector = TableDetector(path_to_model, model_name)
    res = table_detector.use_detection(img)
    founded_table_boxes = process_output_from_table_detector(res)
    first_table_box = founded_table_boxes[0]
    assert first_table_box.confidence > 0.95
    assert first_table_box.box == excepted_table_box.box


def test_not_found_table():
    arr = np.zeros([1653, 2337, 3], dtype=np.uint8)
    img = Image.fromarray(arr)
    table_detector = TableDetector(path_to_model, model_name, threshold=1)
    with pytest.raises(ValueError):
        res = table_detector.use_detection(img)
        table_confidence = float(res["scores"])
