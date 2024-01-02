import numpy as np
from PIL import Image
from typing import Optional


class ImageInput:
    def __init__(self, path_to_image: str, use_deskew: bool):
        self.path = path_to_image
        self.image_orig = self.read_image(self.path)
        self.image = self.resize_image(self.image_orig)
        self.image_crop: Optional[Image.Image]
        if use_deskew:
            self.deskew_image_wand()

    @staticmethod
    def read_image(path: str):
        image = Image.open(path).convert("RGB")
        return image

    @staticmethod
    def resize_image(image):
        width, height = image.size
        image.resize((int(width * 0.5), int(height * 0.5)))
        return image

    def deskew_image_wand(self):
        from PIL import Image as ImagePIL
        from wand.image import Image
        with Image.from_array(np.array(self.image_orig)) as img:
            img.deskew(0.4 * img.quantum_range)
            deskew_img = img.clone()
            deskew_img = ImagePIL.fromarray(np.array(deskew_img))
            self.image_orig = deskew_img

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
