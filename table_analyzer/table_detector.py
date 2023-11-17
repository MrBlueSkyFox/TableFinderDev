import torch
from transformers import AutoImageProcessor, TableTransformerForObjectDetection


class TableDetector:
    def __init__(self):
        self.image_processor = AutoImageProcessor.from_pretrained("microsoft/table-transformer-detection")
        self.model = TableTransformerForObjectDetection.from_pretrained("microsoft/table-transformer-detection")
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
