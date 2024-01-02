import PIL.Image


def crop_image_by_coord(
        image: PIL.Image.Image,
        box: list[float, float, float, float]
) -> PIL.Image.Image:
    padding = 50
    xmin, ymin, xmax, ymax = box
    xmax += padding
    ymax += padding
    xmin -= padding
    ymin -= padding
    crop_img = image.crop((xmin, ymin, xmax, ymax))
    width, height = crop_img.size
    crop_img.resize((int(width * 0.5), int(height * 0.5)))
    return crop_img



