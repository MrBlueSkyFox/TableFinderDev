from domain.model import TableBox, TableStructure, TableStructureOrdered
from .table_detection import table_model, table_detection_processing
from .table_layout_detection import table_layout_model, table_layout_detection_processing
from . import util


def retrieve_table_box_and_confidence(
        img,
        model_detection: table_model.TableDetector
) -> TableBox:
    raw_result = model_detection.use_detection(img)
    all_detected_tables = table_detection_processing. \
        process_output_from_table_detector(raw_result)
    if len(all_detected_tables) == 0:
        raise table_detection_processing.NotFoundTable("Not Found any table")
    fist_detected_table = all_detected_tables[0]
    return fist_detected_table


def retrieve_table_layout_without_ordering(
        img,
        model_detection: table_model.TableDetector,
        model_detection_layout: table_layout_model.TableLayoutDetector
) -> TableStructure:
    table_box = retrieve_table_box_and_confidence(img, model_detection)
    img_with_only_table = util.crop_image_by_coord(img,
                                                   list(vars(table_box.box).values())
                                                   )

    probes, boxes = model_detection_layout.use_detection(img_with_only_table)
    table_structured = table_layout_detection_processing. \
        process_output_from_table_layout_detector(probes, boxes)
    return table_structured


def retrieve_table_layout_with_ordering(
        img,
        model_detection: table_model.TableDetector,
        model_detection_layout: table_layout_model.TableLayoutDetector
) -> TableStructureOrdered:
    table_structured = retrieve_table_layout_without_ordering(
        img,
        model_detection,
        model_detection_layout
    )
    table_structured_with_order = table_layout_detection_processing. \
        process_to_ordered_table_structure(table_structured)
    return table_structured_with_order


from .ocr_interface import OcrInterface
from domain.model import TableStructureOrderedWithText, CellWithText
from . import util
from dataclasses import astuple


def retrieve_text_in_table(
        img,
        model_detection: table_model.TableDetector,
        model_detection_layout: table_layout_model.TableLayoutDetector,
        ocr_modules: list[OcrInterface]
) -> TableStructureOrderedWithText:
    table_structured_with_order = retrieve_table_layout_with_ordering(
        img,
        model_detection,
        model_detection_layout
    )
    table_box = retrieve_table_box_and_confidence(
        img,
        model_detection,
    )
    img_with_only_table = util.crop_image_by_coord(img,
                                                   list(vars(table_box.box).values())
                                                   )
    columns_with_text: list[list[CellWithText]] = []
    for column in table_structured_with_order.cells:
        column_with_text: list[CellWithText] = []
        for cell in column:
            img_cell = util.crop_image_by_coord(
                img_with_only_table,
                list(astuple(cell)),
                0
            )
            text = ""
            for ocr in ocr_modules:
                text = ocr.use_ocr(img_cell)
                if is_text_empty(text):
                    continue
                else:
                    break
            cell_with_text = CellWithText(*astuple(cell), text=text)
            column_with_text.append(cell_with_text)
        columns_with_text.append(column_with_text)
    table_ordered_with_text = TableStructureOrderedWithText(columns_with_text)
    return table_ordered_with_text


def is_text_empty(text):
    return len(text) == 0
