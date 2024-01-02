import numpy as np
import pytest
from PIL import Image
from domain.model import TableBox, Cell, TableStructure

from service_layer.table_layout_model import TableLayoutDetector
from service_layer.handlers.handlers import crop_image_by_coord
from service_layer.handlers.table_layout_detection import \
    process_output_from_table_layout_detector, process_to_ordered_table_structure

path_to_model = r"D:\PycharmMainProjects\TableFinderDev\models"
model_name = "microsoft/table-transformer-structure-recognition"
path_to_image = r"D:\PycharmMainProjects\TableFinderDev\tests\FIO_1_0.jpg"


# TODO
# 1) change duplicate code to fixture

def test_found_table_layout():
    img = Image.open(path_to_image)
    table_box = TableBox(
        Cell(
            150.7137908935547,
            615.0811767578125,
            1472.652099609375,
            1805.0367431640625
        ),
        0.95
    )
    img = crop_image_by_coord(
        img,
        [table_box.box.x_min, table_box.box.y_min,
         table_box.box.x_max, table_box.box.y_max]
    )
    width, height = img.size
    img.resize((int(width * 0.5), int(height * 0.5)))
    table_detector = TableLayoutDetector(path_to_model, model_name)
    probs, boxes = table_detector.use_detection(img)

    table_layout = process_output_from_table_layout_detector(
        probs, boxes
    )
    assert len(table_layout.rows) == 9
    assert len(table_layout.columns) == 3
    assert len(table_layout.header) == 1


def test_found_table_layout_with_cells_in_order():
    img = Image.open(path_to_image)
    table_box = TableBox(
        Cell(
            150.7137908935547,
            615.0811767578125,
            1472.652099609375,
            1805.0367431640625
        ),
        0.95
    )
    img = crop_image_by_coord(
        img,
        [table_box.box.x_min, table_box.box.y_min,
         table_box.box.x_max, table_box.box.y_max]
    )
    width, height = img.size
    img.resize((int(width * 0.5), int(height * 0.5)))
    table_detector = TableLayoutDetector(path_to_model, model_name)
    probs, boxes = table_detector.use_detection(img)

    table_layout = process_output_from_table_layout_detector(
        probs, boxes
    )
    table_layout_ordered = process_to_ordered_table_structure(table_layout)

    assert len(table_layout.rows) == len(table_layout_ordered.cells)
    assert len(table_layout.columns) == len(table_layout_ordered.cells[0])