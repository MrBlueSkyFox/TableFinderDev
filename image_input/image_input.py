from PIL import Image
from typing import Optional


class ImageInput:
    def __init__(self, path_to_image: str):
        self.path = path_to_image
        self.image_orig = self.read_image(self.path)
        self.image = self.resize_image(self.image_orig)
        self.image_crop: Optional[Image.Image]

    @staticmethod
    def read_image(path: str):
        image = Image.open(path).convert("RGB")
        return image

    @staticmethod
    def resize_image(image):
        width, height = image.size
        image.resize((int(width * 0.5), int(height * 0.5)))
        return image

    def get_image(self):
        if not self.image:
            print("Image empty")
        return self.image

    def get_image_crop(self):
        if not self.img_crop:
            print("Img crop empty")
        return self.img_crop

    def crop_detected_table(self, result):
        padding = 50
        xmin, ymin, xmax, ymax = result
        xmax += padding
        ymax += padding
        xmin -= padding
        ymin -= padding
        crop_img = self.image.crop((xmin, ymin, xmax, ymax))
        width, height = crop_img.size
        crop_img.resize((int(width * 0.5), int(height * 0.5)))
        self.img_crop = crop_img
