import pytest

from domain.model import TableBox, Cell
from service_layer import handlers
from service_layer.table_detection import table_model, table_detection_processing


def test_find_table(
        img,
        path_to_detection_models,
        table_detection_model_name
):
    excepted_table_box = TableBox(
        Cell(
            150.7137908935547,
            615.0811767578125,
            1472.652099609375,
            1805.0367431640625
        ),
        0.95
    )
    width, height = img.size
    img.resize((int(width * 0.5), int(height * 0.5)))
    table_detector = table_model.TableDetector(
        path_to_detection_models,
        table_detection_model_name
    )
    res = table_detector.use_detection(img)
    founded_table_boxes = table_detection_processing. \
        process_output_from_table_detector(res)
    first_table_box = founded_table_boxes[0]
    assert first_table_box.confidence > 0.95
    assert first_table_box.box == excepted_table_box.box


def test_not_found_table(
        img_empty,
        path_to_detection_models,
        table_detection_model_name
):
    table_detector = table_model.TableDetector(
        path_to_detection_models,
        table_detection_model_name,
        threshold=1
    )
    with pytest.raises(ValueError):
        res = table_detector.use_detection(img_empty)
        table_confidence = float(res["scores"])


def test_retrieve_table_box_and_confidence_success(
        img,
        path_to_detection_models,
        table_detection_model_name
):
    excepted_table_box = TableBox(
        Cell(
            150.7137908935547,
            615.0811767578125,
            1472.652099609375,
            1805.0367431640625
        ),
        0.95
    )
    width, height = img.size
    img.resize((int(width * 0.5), int(height * 0.5)))
    table_detector = table_model.TableDetector(
        path_to_detection_models,
        table_detection_model_name
    )
    table_in_image = handlers. \
        retrieve_table_box_and_confidence(img, table_detector)
    assert table_in_image.confidence > 0.95
    assert table_in_image.box == excepted_table_box.box


def test_retrieve_table_box_and_confidence_failure(
        img_empty,
        path_to_detection_models,
        table_detection_model_name
):
    table_detector = table_model.TableDetector(
        path_to_detection_models,
        table_detection_model_name,
        threshold=1
    )
    with pytest.raises(table_detection_processing.NotFoundTable):
        table_not_found = handlers. \
            retrieve_table_box_and_confidence(img_empty, table_detector)
