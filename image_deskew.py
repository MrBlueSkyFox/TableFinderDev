import os.path

from PIL import Image


def deskew_library(image: Image.Image) -> Image.Image:
    from deskew import determine_skew
    import numpy as np
    from skimage.color import rgb2gray
    from skimage.transform import rotate
    image_array = np.array(image)
    grayscale = rgb2gray(image_array)
    angle = determine_skew(grayscale)
    rotated = rotate(image_array, angle, resize=True) * 255
    pil_res = Image.fromarray(rotated.astype(np.uint8))
    return pil_res


def deskew_opencv(image: Image.Image) -> Image.Image:
    import numpy as np
    import cv2
    img = np.array(image)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    gray = cv2.GaussianBlur(gray, (9, 9), 0)
    resized_height = 480
    percent = resized_height / len(img)
    resized_width = int(percent * len(img[0]))
    gray = cv2.resize(gray, (resized_width, resized_height))
    start_point = (0, 0)
    end_point = (gray.shape[0], gray.shape[1])
    color = (255, 255, 255)
    thickness = 10
    gray = cv2.rectangle(gray, start_point, end_point, color, thickness)
    gray = cv2.bitwise_not(gray)
    thresh = cv2.threshold(gray, 0, 255,
                           cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 5))
    dilate = cv2.dilate(thresh, kernel)

    contours, hierarchy = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    angles = []
    for contour in contours:
        minAreaRect = cv2.minAreaRect(contour)
        angle = minAreaRect[-1]
        if angle != 90.0 and angle != -0.0:  # filter out 0 and 90
            angles.append(angle)

    angles.sort()
    mid_angle = angles[int(len(angles) / 2)]

    if angle > 45:  # anti-clockwise
        angle = -(90 - angle)
    height = img.shape[0]
    width = img.shape[1]
    m = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)
    deskewed = cv2.warpAffine(img, m, (width, height), borderValue=(255, 255, 255))
    deskewed_img = Image.fromarray(deskewed.astype(np.uint8))
    return deskewed_img


def deskew_image_magic(image: Image.Image) -> Image.Image:
    # use image magic open source library
    from wand.image import Image
    from PIL import Image as Image_pil
    import numpy as np
    with Image.from_array(np.array(image)) as img:
        img.deskew(0.4 * img.quantum_range)
        deskew_img = img.clone()
        deskew_img = Image_pil.fromarray(np.array(deskew_img))
    return deskew_img


if __name__ == "__main__":
    from util import get_all_jpg_images_in_directory
    import pathlib
    from PIL import Image
    import time

    path_to_dir = r"C:\Users\t.abraamyan\Documents\PythonPRJ\TableFinderDev\data\default"
    path_to_save = r"C:\Users\t.abraamyan\Documents\PythonPRJ\TableFinderDev\res\deskew"
    method_and_save_path = [
        (deskew_library, "deskew_common_lib"),
        (deskew_opencv, "deskew_opencv"),
        (deskew_image_magic, "deskew_image_magic")
    ]
    timing = {

    }
    for file_path in get_all_jpg_images_in_directory(path_to_dir):
        print(f"Working on file path {file_path}")
        img = Image.open(file_path)
        file_name_with_ext = os.path.basename(file_path)

        for deskew_function, dir_name in method_and_save_path:
            start = time.perf_counter()
            try:
                img_res = deskew_function(img.copy())
            except IndexError as e:
                print(f"Error index method {dir_name}")
                continue
            except Exception as e:
                print(f"Exception error method {dir_name}")
                continue
            end = time.perf_counter()

            array_with_timings = timing.get(dir_name, [])
            array_with_timings.append(
                end - start
            )
            timing[dir_name] = array_with_timings
            dir_path_to_save = os.path.join(
                path_to_save, dir_name
            )
            pathlib.Path(dir_path_to_save).mkdir(exist_ok=True, parents=True)
            file_save = os.path.join(
                dir_path_to_save, file_name_with_ext
            )

            img_res.save(file_save)
