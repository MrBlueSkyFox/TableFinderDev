from service_layer import handlers
from service_layer.table_detection import table_model
from service_layer.table_layout_detection import table_layout_model, table_layout_detection_processing


# TODO
# add failure tests
def test_found_table_layout(
        img_with_table,
        path_to_detection_models,
        table_detection_layout_model_name
):
    table_detector = table_layout_model.TableLayoutDetector(
        path_to_detection_models,
        table_detection_layout_model_name
    )
    probs, boxes = table_detector.use_detection(img_with_table)

    table_layout = table_layout_detection_processing. \
        process_output_from_table_layout_detector(probs, boxes)
    assert len(table_layout.rows) == 9
    assert len(table_layout.columns) == 3
    assert len(table_layout.header) == 1


def test_found_table_layout_with_cells_in_order(
        img_with_table,
        path_to_detection_models,
        table_detection_layout_model_name
):
    table_detector = table_layout_model.TableLayoutDetector(
        path_to_detection_models,
        table_detection_layout_model_name
    )
    probs, boxes = table_detector.use_detection(img_with_table)

    table_layout = table_layout_detection_processing. \
        process_output_from_table_layout_detector(probs, boxes)
    table_layout_ordered = table_layout_detection_processing. \
        process_to_ordered_table_structure(table_layout)

    assert len(table_layout.rows) == len(table_layout_ordered.cells)
    assert len(table_layout.columns) == len(table_layout_ordered.cells[0])


def test_retrieve_table_layout_without_ordering_success(
        img,
        path_to_detection_models,
        table_detection_model_name,
        table_detection_layout_model_name
):
    table_detector = table_model.TableDetector(
        path_to_detection_models,
        table_detection_model_name
    )
    table_layout_detector = table_layout_model.TableLayoutDetector(
        path_to_detection_models,
        table_detection_layout_model_name
    )
    table_without_order = handlers. \
        retrieve_table_layout_without_ordering(img, table_detector, table_layout_detector)
    assert len(table_without_order.rows) == 9
    assert len(table_without_order.columns) == 3
    assert len(table_without_order.header) == 1


def test_retrieve_table_layout_with_ordering(
        img,
        path_to_detection_models,
        table_detection_model_name,
        table_detection_layout_model_name
):
    table_detector = table_model.TableDetector(
        path_to_detection_models,
        table_detection_model_name
    )
    table_layout_detector = table_layout_model.TableLayoutDetector(
        path_to_detection_models,
        table_detection_layout_model_name
    )
    table_with_order = handlers. \
        retrieve_table_layout_with_ordering(img, table_detector, table_layout_detector)
    assert len(table_with_order.cells) == 9
    assert len(table_with_order.cells[0]) == 3
