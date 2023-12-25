import torch
from transformers import AutoImageProcessor, TableTransformerForObjectDetection

from .table_model_interface import TableInterface
from .types import probability


class TableDetector(TableInterface):
    def __init__(self,
                 path_to_model: str,
                 model_name: str,
                 threshold: probability = 0.8
                 ):
        super().__init__(path_to_model, model_name, threshold)
        self.image_processor = AutoImageProcessor.from_pretrained(self.model_name,
                                                                  cache_dir=self.path,
                                                                  local_files_only=True,
                                                                  force_download=False,
                                                                  token=False)
        self.model = TableTransformerForObjectDetection.from_pretrained(self.model_name,
                                                                        cache_dir=self.path,
                                                                        local_files_only=True,
                                                                        force_download=False,
                                                                        token=False)

    def use_detection(self, image):
        inputs = self.image_processor(images=image, return_tensors="pt")
        outputs = self.model(**inputs)
        target_sizes = torch.tensor([image.size[::-1]])
        results = self.image_processor.post_process_object_detection(outputs,
                                                                     threshold=self.threshold,
                                                                     target_sizes=target_sizes)[0]
        return results
