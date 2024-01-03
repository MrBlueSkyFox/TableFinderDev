import os

import easyocr

from .. import ocr_interface, util


class EasyOcr(ocr_interface.OcrInterface):
    def __init__(self, path_to_model: str):
        super().__init__(path_to_model)
        os.environ['EASYOCR_MODULE_PATH'] = self.path
        self.reader = easyocr.Reader(['ru', 'en'],
                                     gpu=False)

    def _preprocess_image(self, img):
        img = util.convert_pill2np(img)
        return img

    def _inference(self, img):
        text = self.reader.readtext(img, detail=0)
        if isinstance(text, list):
            text = "\n".join(text)
        return text
