import pytesseract

from .. import ocr_interface, util


class TesseractOCR(ocr_interface.OcrInterface):
    def __init__(self, path_to_model: str):
        super().__init__(path_to_model)
        pytesseract.pytesseract.tesseract_cmd = self.path

    def _preprocess_image(self, img):
        img = util.convert_pill2np(img)
        return img

    def _inference(self, img):
        text = pytesseract.image_to_string(img, lang='rus')
        return text
