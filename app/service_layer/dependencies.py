from service_layer.table_detection import table_model
from service_layer.table_layout_detection import table_layout_model
from service_layer import ocr_interface
from service_layer.ocr import tesseract_ocr, easy_ocr


def get_table_detector(
        path_to_model: str = "path/to/model",
        model_name: str = "model_name"
) -> table_model.TableDetector:
    # Ensure singleton behavior using a module-level variable
    if not hasattr(get_table_detector, "instance"):
        get_table_detector.instance = table_model.TableDetector(
            path_to_model,
            model_name
        )
    return get_table_detector.instance


def get_table_layout_detection_model(
        path_to_model: str = "path/to/model",
        model_name: str = "model_name"
) -> table_layout_model.TableLayoutDetector:
    if not hasattr(get_table_layout_detection_model, "instance"):
        get_table_layout_detection_model.instance = table_layout_model.TableLayoutDetector(
            path_to_model,
            model_name
        )
    return get_table_layout_detection_model.instance


def get_tesseract_ocr(
        path_to_model: str = "path/to/model",
) -> tesseract_ocr.TesseractOCR:
    if not hasattr(get_tesseract_ocr, "instance"):
        get_tesseract_ocr.instance = tesseract_ocr.TesseractOCR(
            path_to_model
        )
    return get_tesseract_ocr.instance


def get_easy_ocr(
        path_to_model: str = "path/to/model"
) -> easy_ocr.EasyOcr:
    if not hasattr(get_easy_ocr, "instance"):
        get_easy_ocr.instance = easy_ocr.EasyOcr(
            path_to_model
        )
    return get_easy_ocr.instance


def get_ocr_modules() -> list[ocr_interface.OcrInterface]:
    if not hasattr(get_ocr_modules, "instances"):
        get_ocr_modules.instances = []
        get_ocr_modules.instances.append(get_tesseract_ocr())
        get_ocr_modules.instances.append(get_easy_ocr())
    return get_ocr_modules.instances


def setup(settings):
    table_detection_model = get_table_detector(
        settings.transformer_cache,
        settings.table_detection_model_name
    )
    table_layout_detection_model = get_table_layout_detection_model(
        settings.transformer_cache,
        settings.table_layout_model_name
    )
    tesseract_ocr_model = get_tesseract_ocr(
        settings.tesseract_path
    )
    easy_ocr_model = get_easy_ocr(
        settings.easy_ocr_cache
    )
    ocr_modules_available = get_ocr_modules()
    return (
        table_detection_model,
        table_layout_detection_model,
        ocr_modules_available,
        tesseract_ocr_model,
        easy_ocr_model
    )
