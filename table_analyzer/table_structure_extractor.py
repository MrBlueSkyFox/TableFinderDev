from ocr import OCRResolver
from cell_types import FoundedCell


class TableStructureExtractor:
    def __init__(self, ocr_instance: OCRResolver):
        self.ocr = ocr_instance

    def get_table_structure(self, image_with_table, cols_data, rows_data, header_data) \
            -> tuple[list[list[str]], list[str]]:
        len_of_columns = len(cols_data)
        founded_cells = self.find_cells_data(cols_data, rows_data)
        sorted_by_rows = self.sort_by_y(founded_cells)
        self.set_text_to_cell(image_with_table, sorted_by_rows)
        col_row_data = self.restore_table_format(sorted_by_rows, len_of_columns)
        header_texts = []
        # header_cells = self.get_tabl_object_as_cell(header_data)
        # self.set_text_to_cell(image_with_table, header_cells)
        # headers_texts = [cell.text for cell in header_cells]
        return col_row_data, header_texts

    def set_text_to_cell(self, img, cells: list[FoundedCell]):
        for cell in cells:
            img_with_text = cell.get_crop_img(img)
            text = self.ocr.get_text_from_img(img_with_text)
            cell.set_text(text)

    @staticmethod
    def get_tabl_object_as_cell(data) -> list[FoundedCell]:
        res = [FoundedCell(cell.xmin,
                           cell.ymin,
                           cell.xmax,
                           cell.ymax)
               for cell in data
               ]
        return res

    @staticmethod
    def find_cells_data(cols_data, rows_data):
        founded_cells: list[FoundedCell] = []

        for columns in cols_data:
            for rows in rows_data:
                xmin_inter, ymin_inter, xmax_inter, ymax_inter = \
                    TableStructureExtractor.find_intersection(columns.xmin,
                                                              columns.ymin,
                                                              columns.xmax,
                                                              columns.ymax,
                                                              rows.xmin,
                                                              rows.ymin,
                                                              rows.xmax,
                                                              rows.ymax)
                cell = FoundedCell(xmin_inter, ymin_inter, xmax_inter, ymax_inter)
                founded_cells.append(cell)
        return founded_cells

    @staticmethod
    def sort_by_y(cells: list[FoundedCell]):
        return sorted(cells, key=lambda cell: cell.ymin)

    @staticmethod
    def sort_by_x(cells: list[FoundedCell]):
        return sorted(cells, key=lambda cell: cell.xmin)

    @staticmethod
    def find_intersection(x1, y1, x2, y2, x3, y3, x4, y4):
        """Finds the intersection of two rectangles.

        Args:
          x1: The x-coordinate of the first rectangle's top-left corner.
          y1: The y-coordinate of the first rectangle's top-left corner.
          x2: The x-coordinate of the first rectangle's bottom-right corner.
          y2: The y-coordinate of the first rectangle's bottom-right corner.
          x3: The x-coordinate of the second rectangle's top-left corner.
          y3: The y-coordinate of the second rectangle's top-left corner.
          x4: The x-coordinate of the second rectangle's bottom-right corner.
          y4: The y-coordinate of the second rectangle's bottom-right corner.

        Returns:
          A tuple of four coordinates (x1, y1, x2, y2) of the intersecting rectangle,
          or None if the two rectangles do not overlap.
        """

        if x1 > x4 or x2 < x3 or y1 > y4 or y2 < y3:
            return None

        x_min = max(x1, x3)
        x_max = min(x2, x4)
        y_min = max(y1, y3)
        y_max = min(y2, y4)

        return x_min, y_min, x_max, y_max

    @staticmethod
    def restore_table_format(cells: list[FoundedCell], column_len: int) -> list[list[str]]:
        result_data = []
        for i in range(0, len(cells), column_len):
            row = TableStructureExtractor.sort_by_x(cells[i:i + column_len])
            res_row = []
            for r in row:
                res_text = r.text
                if not res_text:
                    res_text = r.text
                res_row.append(res_text)
            result_data.append(res_row)
        return result_data
