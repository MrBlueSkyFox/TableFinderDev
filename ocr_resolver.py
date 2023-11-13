import easyocr
import numpy as np
import pytesseract


class OCRResolver:
    def __init__(self, path_to_tesseract: str = r"C:\Program Files\Tesseract-OCR\tesseract.exe"):
        self.path_to_tesseract = path_to_tesseract
        self.reader = easyocr.Reader(['ru', 'en'],
                                     gpu=False)  # this needs to run only once to load the model into memory
        pytesseract.pytesseract.tesseract_cmd = self.path_to_tesseract

    def get_text_from_img(self, image):
        text = self.use_pytesseract(image)
        if not text:
            text = self.use_paddle(image)
        return text

    def use_pytesseract(self, image) -> str:
        text = pytesseract.image_to_string(image, lang='rus')
        return text

    def use_paddle(self, image) -> str:
        img = self.convert_pil2numpy(image)
        result = self.reader.readtext(img)
        text = [data_found[1] for data_found in result]
        text = "".join(text)
        return text

    @staticmethod
    def convert_pil2numpy(pil_img) -> np.array:
        image_numpy = np.array(pil_img)
        return image_numpy
