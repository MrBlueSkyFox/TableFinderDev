import easyocr
import numpy as np
import pytesseract

from .use_methods import UseMethods


class OCRResolver:
    def __init__(self, path_to_tesseract: str = r"C:\Program Files\Tesseract-OCR\tesseract.exe",
                 use_only: str = UseMethods.use_all):
        self.path_to_tesseract = path_to_tesseract
        self.reader = easyocr.Reader(['ru', 'en'],
                                     gpu=False)  # this needs to run only once to load the model into memory
        pytesseract.pytesseract.tesseract_cmd = self.path_to_tesseract
        self.use_method = use_only

    def get_text_from_img(self, image):
        image = self.convert_pil2numpy(image)
        if self.use_method == UseMethods.use_tesseract:
            text = self.use_pytesseract(image)
        elif self.use_method == UseMethods.use_easy_ocr:
            text = self.use_easyocr(image)
        else:
            text = self.use_pytesseract(image)
            if not text:
                # image = self.convert_pil2numpy(image)
                text = self.use_easyocr(image)

        return text

    def use_pytesseract(self, image) -> str:
        text = pytesseract.image_to_string(image, lang='rus')
        return text

    def use_easyocr(self, image) -> str:
        result = self.reader.readtext(image)
        text = [data_found[1] for data_found in result]
        text = "".join(text)
        return text

    @staticmethod
    def convert_pil2numpy(pil_img) -> np.array:
        image_numpy = np.array(pil_img)
        return image_numpy
