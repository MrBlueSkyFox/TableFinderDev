import numpy as np
import pytest
import os

from PIL import Image

PROJECT_DIR = r"D:\PycharmMainProjects\TableFinderDev"

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
