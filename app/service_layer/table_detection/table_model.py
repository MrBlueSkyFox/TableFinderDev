import PIL.Image
import torch
from transformers import AutoImageProcessor, TableTransformerForObjectDetection
from .. import types, table_model_interface


class TableDetector(table_model_interface.TableInterface):
    def __init__(self,
                 path_to_model: str,
                 model_name: str,
                 threshold: types.probability = 0.8
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

    def _inference(self, img):
        inputs = self.image_processor(images=img, return_tensors="pt")
        outputs = self.model(**inputs)
        target_sizes = torch.tensor([img.size[::-1]])
        results = self.image_processor.post_process_object_detection(outputs,
                                                                     threshold=self.threshold,
                                                                     target_sizes=target_sizes)[0]
        return results

    def _preprocess_image(self, img) -> PIL.Image.Image:
        return img
