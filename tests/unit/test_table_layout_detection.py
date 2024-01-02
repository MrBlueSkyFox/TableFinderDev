from domain.model import TableBox, Cell

from service_layer import handlers
from service_layer.table_detection import table_model
from service_layer.table_layout_detection import table_layout_model, table_layout_detection_processing
from service_layer.util import crop_image_by_coord

path_to_model = r"D:\PycharmMainProjects\TableFinderDev\models"
model_name = "microsoft/table-transformer-structure-recognition"
path_to_image = r"D:\PycharmMainProjects\TableFinderDev\tests\FIO_1_0.jpg"


# TODO
# 1) change duplicate code to fixture

def test_found_table_layout(img):
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
    table_detector = table_layout_model.TableLayoutDetector(path_to_model, model_name)
    probs, boxes = table_detector.use_detection(img)

    table_layout = table_layout_detection_processing. \
        process_output_from_table_layout_detector(probs, boxes)
    assert len(table_layout.rows) == 9
    assert len(table_layout.columns) == 3
    assert len(table_layout.header) == 1


def test_found_table_layout_with_cells_in_order(img):
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
    table_detector = table_layout_model.TableLayoutDetector(path_to_model, model_name)
    probs, boxes = table_detector.use_detection(img)

    table_layout = table_layout_detection_processing. \
        process_output_from_table_layout_detector(probs, boxes)
    table_layout_ordered = table_layout_detection_processing. \
        process_to_ordered_table_structure(table_layout)

    assert len(table_layout.rows) == len(table_layout_ordered.cells)
    assert len(table_layout.columns) == len(table_layout_ordered.cells[0])


def test_retrieve_table_layout_without_ordering_success(img):
    table_detector = table_model.TableDetector(path_to_model, "microsoft/table-transformer-detection")
    table_layout_detector = table_layout_model.TableLayoutDetector(path_to_model, model_name)
    table_without_order = handlers. \
        retrieve_table_layout_without_ordering(img, table_detector, table_layout_detector)
    assert len(table_without_order.rows) == 9
    assert len(table_without_order.columns) == 3
    assert len(table_without_order.header) == 1


def test_retrieve_table_layout_with_ordering(img):
    table_detector = table_model.TableDetector(path_to_model, "microsoft/table-transformer-detection")
    table_layout_detector = table_layout_model.TableLayoutDetector(path_to_model, model_name)
    table_with_order = handlers. \
        retrieve_table_layout_with_ordering(img, table_detector, table_layout_detector)
    assert len(table_with_order.cells) == 9
    assert len(table_with_order.cells[0]) == 3
