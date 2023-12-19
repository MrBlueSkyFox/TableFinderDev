import torch
from transformers import AutoFeatureExtractor, AutoModelForObjectDetection

from cell_types import FoundedTableObjects


class TableLayoutAnalyzer:
    def __init__(self,path_to_transformers: str):
        # default_transformer_cache = r'C:\Users\t.abraamyan\Documents\PythonPRJ\TableFinderDev\models'
        if len(path_to_transformers) > 0:
            default_transformer_cache = path_to_transformers
        else:
            default_transformer_cache = r'C:\Users\t.abraamyan\Documents\PythonPRJ\TableFinderDev\models'

        self.extractor = AutoFeatureExtractor.from_pretrained("microsoft/table-transformer-structure-recognition",
                                                              cache_dir=default_transformer_cache,
                                                              force_download=False,
                                                              local_files_only=True,
                                                              token=False)
        self.model = AutoModelForObjectDetection.from_pretrained("microsoft/table-transformer-structure-recognition",
                                                                 cache_dir=default_transformer_cache,
                                                                 force_download=False,
                                                                 local_files_only=True,
                                                                 token=False)

    def use_table_layout_detection(self, img_with_table):
        encoding = self.extractor(img_with_table, return_tensors="pt")
        encoding.keys()
        print(f"Encoding ke {encoding['pixel_values'].shape}")
        with torch.no_grad():
            outputs = self.model(**encoding)

        # keep only predictions of queries with 0.9+ confidence (excluding no-object class)
        probas = outputs.logits.softmax(-1)[0, :, :-1]
        keep = probas.max(-1).values > 0.6

        # rescale bounding boxes
        target_sizes = torch.tensor(img_with_table.size[::-1]).unsqueeze(0)
        postprocessor_outputs = self.extractor.post_process(outputs, target_sizes)
        bboxes_scaled_lay = postprocessor_outputs[0]['boxes'][keep]

        probs_keeping = probas[keep]
        boxes = bboxes_scaled_lay
        return probs_keeping, boxes

    @staticmethod
    def find_layout_data(probs_keeping, boxes) -> tuple[
        list[FoundedTableObjects], list[FoundedTableObjects], list[FoundedTableObjects]
    ]:
        rows_data: list[FoundedTableObjects] = []
        cols_data: list[FoundedTableObjects] = []
        header_data: list[FoundedTableObjects] = []
        for p, (xmin, ymin, xmax, ymax) in zip(probs_keeping, boxes.tolist()):
            cl = p.argmax()
            pos = cl.item()

            cropped_img_inst = FoundedTableObjects(xmin, ymin, xmax, ymax, pos)
            if pos == 1:  # col
                cols_data.append(cropped_img_inst)
            elif pos == 2:  # rows
                rows_data.append(cropped_img_inst)
            elif pos == 0:
                header_data.append(cropped_img_inst)
            else:
                print(pos)
        print(f"Found rows  len {len(rows_data)}:{rows_data}")
        print(f"Found cols len  {len(cols_data)} :{cols_data}")
        # print(f"Found rows :{header_data}")
        return cols_data, rows_data, header_data
