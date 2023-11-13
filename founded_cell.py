from dataclasses import dataclass


@dataclass
class FoundedCell:
    xmin: int
    ymin: int
    xmax: int
    ymax: int
    # pos: int
    text: str = None

    def set_text(self, text):
        self.text = text

    def get_crop_img(self, img_orig):
        img_crop = img_orig.crop((self.xmin, self.ymin, self.xmax, self.ymax))
        return img_crop
