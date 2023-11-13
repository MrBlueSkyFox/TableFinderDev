import torch
from transformers import AutoImageProcessor, TableTransformerForObjectDetection


class TableDetection:
    def __init__(self):
        self.image_processor = AutoImageProcessor.from_pretrained("microsoft/table-transformer-detection")
        self.model = TableTransformerForObjectDetection.from_pretrained("microsoft/table-transformer-detection")

    def use_table_detection(self, image):
        inputs = self.image_processor(images=image, return_tensors="pt")
        outputs = self.model(**inputs)
        target_sizes = torch.tensor([image.size[::-1]])
        results = self.image_processor.post_process_object_detection(outputs,
                                                                threshold=0.9,
                                                                target_sizes=target_sizes)[0]
        return results

    def get_table_boxes(self, results):
        return results["boxes"].tolist()
