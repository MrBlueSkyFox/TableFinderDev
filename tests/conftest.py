import numpy as np
import pytest
import os

from PIL import Image

from domain.model import TableBox, Cell
from service_layer.util import crop_image_by_coord

PROJECT_DIR = r"D:\PycharmMainProjects\TableFinderDev"
MODEL_DIR = "models"
TABLE_DETECTOR_MODEL_NAME = "microsoft/table-transformer-detection"
TABLE_LAYOUT_DETECTOR_MODEL_NAME = "microsoft/table-transformer-structure-recognition"
PATH_TO_EASY_OCR = os.path.join(MODEL_DIR, "easy_ocr")

PATH_TO_TESSERACT_EXE = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

path_to_image = os.path.join(PROJECT_DIR, "tests\\FIO_1_0.jpg")


@pytest.fixture
def img():
    img = Image.open(path_to_image)
    return img


@pytest.fixture
def img_empty():
    arr = np.zeros([1653, 2337, 3], dtype=np.uint8)
    img = Image.fromarray(arr)
    return img


@pytest.fixture
def path_to_detection_models():
    return os.path.join(PROJECT_DIR, MODEL_DIR)


@pytest.fixture
def table_detection_model_name():
    return TABLE_DETECTOR_MODEL_NAME


@pytest.fixture
def table_detection_layout_model_name():
    return TABLE_LAYOUT_DETECTOR_MODEL_NAME


@pytest.fixture
def tesseract_path() -> str:
    # TODO
    # ADD LOGIC TO SET PATH DEPENDING ON OS
    return PATH_TO_TESSERACT_EXE


@pytest.fixture
def easy_ocr_path() -> str:
    return PATH_TO_EASY_OCR


@pytest.fixture
def table_box():
    table_box = TableBox(
        Cell(
            150.7137908935547,
            615.0811767578125,
            1472.652099609375,
            1805.0367431640625
        ),
        0.95
    )
    return table_box


@pytest.fixture
def img_with_table(img, table_box):
    img = crop_image_by_coord(
        img,
        [table_box.box.x_min, table_box.box.y_min,
         table_box.box.x_max, table_box.box.y_max]
    )
    return img
