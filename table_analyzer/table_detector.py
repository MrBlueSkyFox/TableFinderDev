import os.path

import torch
from transformers import AutoImageProcessor, TableTransformerForObjectDetection


class TableDetector:
    def __init__(self, path_to_transformers: str):
        # default_transformer_cache = r'C:\Users\t.abraamyan\Documents\PythonPRJ\TableFinderDev\models'
        if len(path_to_transformers) > 0:
            default_transformer_cache = path_to_transformers
        else:
            default_transformer_cache = r'C:\Users\t.abraamyan\Documents\PythonPRJ\TableFinderDev\models'

        model_detection_name = 'microsoft/table-transformer-detection'
        model_layout_detection_name = 'microsoft/table-transformer-detection'
        # model_detection_name = os.path.join(default_transformer_cache, model_detection_name)
        # model_layout_detection_name = os.path.join(default_transformer_cache, model_layout_detection_name)
        self.image_processor = AutoImageProcessor.from_pretrained(model_detection_name,
                                                                  cache_dir=default_transformer_cache,
                                                                  force_download=False,
                                                                  local_files_only=True,
                                                                  token=False)
        self.model = TableTransformerForObjectDetection.from_pretrained(model_layout_detection_name,
                                                                        cache_dir=default_transformer_cache,
                                                                        force_download=False,
                                                                        local_files_only=True,
                                                                        token=False)
        self.table_minimum_detection_value = 0.8  # from 0 to 1

    def use_table_detection(self, image):
        inputs = self.image_processor(images=image, return_tensors="pt")
        outputs = self.model(**inputs)
        target_sizes = torch.tensor([image.size[::-1]])
        results = self.image_processor.post_process_object_detection(outputs,
                                                                     threshold=self.table_minimum_detection_value,
                                                                     target_sizes=target_sizes)[0]
        return results

    def get_table_boxes(self, results):
        return results["boxes"].tolist()
