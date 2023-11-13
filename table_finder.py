import os
from image_input import ImageInput
from table_detection import TableDetection
from table_layout_detection import TableLayoutDetection
from ocr_resolver import OCRResolver
from cell_structure_resolver import CellStructureResolver
from output_resolver import OutputResolver


class TableFinder:
    def __init__(self, path_to_tesseract: str = ""):
        self.table_detection_model = TableDetection()
        self.table_layout_detection_model = TableLayoutDetection()
        self.ocr = OCRResolver()

    def read_image_and_write_table_in_json(self, path_to_img: str,
                                           path_to_save: str):
        img_input = ImageInput(path_to_img)
        table_detection_results_raw = self.table_detection_model.use_table_detection(img_input.get_image())
        table_boxes = self.table_detection_model.get_table_boxes(table_detection_results_raw)
        print(f"Detected tables : {len(table_boxes)}")
        try:
            img_input.crop_detected_table(table_boxes[0])
            table_layout_probs, table_layout_boxes = self.table_layout_detection_model.use_table_layout_detection(
                img_input.get_image_crop())
            columns_data, rows_data, header_data = self.table_layout_detection_model.find_layout_data(
                table_layout_probs,
                table_layout_boxes)
            cell_structure = CellStructureResolver(self.ocr)
            col_row_data, header_texts = cell_structure.get_table_structure(img_input.get_image_crop(),
                                                                            columns_data, rows_data, header_data)
            basename = get_basename(path_to_img)
            path_to_store = os.path.join(path_to_save, basename + ".json")
            output_formatter = OutputResolver(path_to_store)
            json_str_result = output_formatter.create_json_result(col_row_data, header_texts)
            output_formatter.write_result(json_str_result)
        except IndexError as e:
            print(f"No table for {path_to_img}")
        except Exception as e:
            print(f"Strange excpetion {path_to_img}")
            print(e)


def get_basename(path: str) -> str:
    base_file_name = os.path.basename(path)
    base_file_name = os.path.splitext(base_file_name)[0]
    return base_file_name
