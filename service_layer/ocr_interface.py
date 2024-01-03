from abc import abstractmethod

import PIL.Image


class OcrInterface:
    def __init__(self, path_to_model: str):
        self.path = path_to_model

    def use_ocr(self, image: PIL.Image.Image):
        image = self._preprocess_image(image)
        res = self._inference(image)
        return res

    @abstractmethod
    def _inference(self, img):
        pass

    @abstractmethod
    def _preprocess_image(self, img):
        pass
