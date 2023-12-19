# import matplotlib
#
# matplotlib.use('TkAgg')
# import matplotlib.pyplot as plt
# from cell_types import FoundedTableObjects
#
#
# def view_pyplot_dev(coord: FoundedTableObjects, img):
#     xmin = coord.xmin
#     ymin = coord.ymin
#     xmax = coord.xmax
#     ymax = coord.ymax
#     plt.figure(figsize=(32, 20))
#     plt.imshow(img)
#     ax = plt.gca()
#     ax.add_patch(plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin,
#                                fill=False, color='red', linewidth=3))  # plot row
#     plt.axis('off')
# #     plt.show()


import os
import pathlib

from util import get_all_jpg_images_in_directory


def get_data_using_tes_ocr():
    from table_extractor import TableExtractor
    use_method = "tes"
    table_finder = TableExtractor(path_to_pytes, use_method)
    path_to_img_dir = r"C:\Users\t.abraamyan\Documents\PythonPRJ\TableFinderDev\data\normalize\fio"
    path_to_store_base = r"C:\Users\t.abraamyan\Documents\PythonPRJ\TableFinderDev\res\normalize\tes"
    path_to_jpg_im = get_all_jpg_images_in_directory(path_to_img_dir)
    for path_to_jpg in path_to_jpg_im:
        table_finder.read_image_and_write_table_in_json(
            path_to_jpg,
            path_to_store_base)


def get_data_using_easy_ocr():
    from table_extractor import TableExtractor
    use_method = "easy"
    table_finder = TableExtractor(path_to_pytes, use_method)
    path_to_img_dir = r"C:\Users\t.abraamyan\Documents\PythonPRJ\TableFinderDev\data\normalize\fio"
    path_to_store_base = r"C:\Users\t.abraamyan\Documents\PythonPRJ\TableFinderDev\res\normalize\easy_ocr"
    path_to_jpg_im = get_all_jpg_images_in_directory(path_to_img_dir)
    for path_to_jpg in path_to_jpg_im:
        table_finder.read_image_and_write_table_in_json(
            path_to_jpg,
            path_to_store_base)


def get_data_using_all_ocr(path_to_dir: str, path_to_save: str):
    from table_extractor import TableExtractor
    use_method = "all"
    table_finder = TableExtractor(path_to_pytes, use_method)
    # path_to_img_dir = r"C:\Users\t.abraamyan\Documents\PythonPRJ\TableFinderDev\data\normalize\fio"
    # path_to_store_base = r"C:\Users\t.abraamyan\Documents\PythonPRJ\TableFinderDev\res\normalize\all"
    pathlib.Path(path_to_save).mkdir(exist_ok=True, parents=True)
    path_to_jpg_im = get_all_jpg_images_in_directory(path_to_dir)
    for path_to_jpg in path_to_jpg_im[:2]:
        table_finder.read_image_and_write_table_in_json(
            path_to_jpg,
            path_to_save)


if __name__ == "__main__":
    default_transformer_cache = r'C:\Users\t.abraamyan\Documents\PythonPRJ\TableFinderDev\models'
    os.environ['CURL_CA_BUNDLE'] = ''
    os.environ['REQUESTS_CA_BUNDLE'] = ''
    os.environ['TRANSFORMERS_CACHE'] = default_transformer_cache
    os.environ['EASYOCR_MODULE_PATH'] = os.path.join(default_transformer_cache, "easy_ocr")
    os.environ['TRANSFORMERS_CACHE'] = default_transformer_cache
    os.environ['HF_HOME'] = default_transformer_cache
    os.environ['XDG_CACHE_HOME'] = default_transformer_cache
    import warnings

    warnings.simplefilter(action='ignore', category=FutureWarning)
    from transformers import logging

    logging.set_verbosity_error()

    # path_to_image = r"C:\Users\tigra\PycharmProjects\OcrResearch\data\fifo_normalize\FIO_1_page-0001.jpg"
    # path_to_image = r"C:\Users\t.abraamyan\Documents\PythonPRJ\TableFinderDev\tmp4AF4.jpg"
    path_to_image = r"C:\Users\t.abraamyan\Documents\PythonPRJ\TableFinderDev\data\default\pos_credit_1_page-0001.jpg"

    # path_to_store_base = r"C:\Users\tigra\PycharmProjects\OcrResearch\data\res"
    path_to_pytes = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    # get_data_using_tes_ocr()
    # get_data_using_easy_ocr()
    path_to_dir_deskew_common = r"C:\Users\t.abraamyan\Documents\PythonPRJ\TableFinderDev\res\deskew\deskew_common_lib"
    path_to_dir_deskew_opencv = r"C:\Users\t.abraamyan\Documents\PythonPRJ\TableFinderDev\res\deskew\deskew_opencv"
    path_to_dir_deskew_image_magic = r"C:\Users\t.abraamyan\Documents\PythonPRJ\TableFinderDev\res\deskew\deskew_image_magic"

    path_to_save_deskew_common_table = r"C:\Users\t.abraamyan\Documents\PythonPRJ\TableFinderDev\res\normalize_deskew\deskew_common_lib"
    path_to_save_deskew_opencv_table = r"C:\Users\t.abraamyan\Documents\PythonPRJ\TableFinderDev\res\normalize_deskew\deskew_opencv"
    path_to_save_deskew_image_magic_table = r"C:\Users\t.abraamyan\Documents\PythonPRJ\TableFinderDev\res\normalize_deskew\deskew_image_magic"

    get_data_using_all_ocr(path_to_dir_deskew_common, path_to_save_deskew_common_table)
    # get_data_using_all_ocr(path_to_dir_deskew_opencv, path_to_save_deskew_opencv_table)
    # get_data_using_all_ocr(path_to_dir_deskew_image_magic, path_to_save_deskew_image_magic_table)
