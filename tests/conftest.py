import numpy as np
import pytest
import os

from PIL import Image

PROJECT_DIR = r"D:\PycharmMainProjects\TableFinderDev"
MODEL_DIR = "models"
TABLE_DETECTOR_MODEL_NAME = "microsoft/table-transformer-detection"
TABLE_LAYOUT_DETECTOR_MODEL_NAME = "microsoft/table-transformer-structure-recognition"

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


