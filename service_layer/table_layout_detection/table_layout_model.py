import PIL.Image
import torch
from transformers import AutoFeatureExtractor, AutoModelForObjectDetection
from .. import types, table_model_interface


class TableLayoutDetector(table_model_interface.TableInterface):
    def __init__(self,
                 path_to_model: str,
                 model_name: str = "microsoft/table-transformer-structure-recognition",
                 detection_threshold: types.probability = 0.6
                 ):
        super().__init__(path_to_model, model_name, detection_threshold)
        self.image_processor = AutoFeatureExtractor.from_pretrained(self.model_name,
                                                                    cache_dir=self.path,
                                                                    local_files_only=True,
                                                                    force_download=False,
                                                                    token=False)
        self.model = AutoModelForObjectDetection.from_pretrained(self.model_name,
                                                                 cache_dir=self.path,
                                                                 local_files_only=True,
                                                                 force_download=False,
                                                                 token=False)

    def _inference(self, img):
        encoding = self.image_processor(img, return_tensors="pt")
        encoding.keys()
        with torch.no_grad():
            outputs = self.model(**encoding)

        # keep only predictions of queries with 0.6+ confidence (excluding no-object class)
        probas = outputs.logits.softmax(-1)[0, :, :-1]
        keep = probas.max(-1).values > self.threshold

        # rescale bounding boxes
        target_sizes = torch.tensor(img.size[::-1]).unsqueeze(0)
        postprocessor_outputs = self.image_processor.post_process(outputs, target_sizes)
        bboxes_scaled_lay = postprocessor_outputs[0]['boxes'][keep]

        probs_keeping = probas[keep]
        boxes = bboxes_scaled_lay
        return probs_keeping, boxes

    def _preprocess_image(self, img) -> PIL.Image.Image:
        return img
