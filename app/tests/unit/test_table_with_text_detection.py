from service_layer import handlers
from service_layer.ocr import easy_ocr, tesseract_ocr
from service_layer.table_detection import table_model
from service_layer.table_layout_detection import table_layout_model


def test_retrieve_text_in_table(
        img,
        path_to_detection_models,
        table_detection_model_name,
        table_detection_layout_model_name,
        tesseract_path,
        easy_ocr_path
):
    table_detector = table_model.TableDetector(
        path_to_detection_models,
        table_detection_model_name
    )
    table_layout_detector = table_layout_model.TableLayoutDetector(
        path_to_detection_models,
        table_detection_layout_model_name
    )
    ocr_tesseract = tesseract_ocr.TesseractOCR(tesseract_path)
    ocr_easy_ocr = easy_ocr.EasyOcr(easy_ocr_path)
    table_with_text = handlers.retrieve_text_in_table(
        img,
        table_detector,
        table_layout_detector,
        [ocr_tesseract, ocr_easy_ocr]
    )
    assert table_with_text.number_of_columns == 3
    assert table_with_text.number_of_rows == 9
    assert '1' in table_with_text.cells[2][0].text
    assert '2' in table_with_text.cells[3][0].text
    assert '3' in table_with_text.cells[4][0].text
