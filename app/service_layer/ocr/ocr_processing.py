from dataclasses import astuple

from domain.model import CellWithText, TableStructureOrderedWithText
from service_layer import util


def ocr_table_cells(img_with_only_table, ocr_modules, table_structured_with_order):
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
