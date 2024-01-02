import pytest
import os

from PIL import Image

PROJECT_DIR = r"D:\PycharmMainProjects\TableFinderDev"

path_to_image = os.path.join(PROJECT_DIR, "tests\\FIO_1_0.jpg")


@pytest.fixture
def img():
    img = Image.open(path_to_image)
    return img
