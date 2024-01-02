from abc import abstractmethod

from transformers import AutoImageProcessor, AutoModelForObjectDetection
import PIL.Image
from . import types

default_transformer_cache = r"models"


class TableInterface:
    def __init__(self, path_to_model: str, model_name: str, detection_threshold: types.probability):
        if len(path_to_model) < 0:
            path = default_transformer_cache
        else:
            path = path_to_model
        self.path = path
        self.model_name = model_name
        self.threshold = detection_threshold

        self.image_processor: AutoImageProcessor
        self.model: AutoModelForObjectDetection

    @abstractmethod
    def use_detection(self, image: PIL.Image.Image):
        pass
