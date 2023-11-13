import os
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

from founded_table_objects import FoundedTableObjects


def view_pyplot_dev(coord: FoundedTableObjects, img):
    xmin = coord.xmin
    ymin = coord.ymin
    xmax = coord.xmax
    ymax = coord.ymax
    plt.figure(figsize=(32, 20))
    plt.imshow(img)
    ax = plt.gca()
    ax.add_patch(plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin,
                               fill=False, color='red', linewidth=3))  # plot row
    plt.axis('off')
    plt.show()


from util import get_all_jpg_images_in_directory

if __name__ == "__main__":
    import warnings

    warnings.simplefilter(action='ignore', category=FutureWarning)
    from transformers import logging

    logging.set_verbosity_error()

    path_to_image = r"C:\Users\tigra\PycharmProjects\OcrResearch\data\fifo_normalize\FIO_1_page-0001.jpg"
    path_to_image = r"C:\Users\tigra\PycharmProjects\OcrResearch\data\fifo_normalize\FIO_1_page-0001.jpg"
    path_to_img_dir = r"C:\Users\tigra\PycharmProjects\OcrResearch\data\fifo_normalize"

    path_to_store_base = r"C:\Users\tigra\PycharmProjects\OcrResearch\data\res"
    from table_finder import TableFinder

    table_finder = TableFinder()

    path_to_jpg_im = get_all_jpg_images_in_directory(path_to_img_dir)
    for path_to_jpg in path_to_jpg_im:
        table_finder.read_image_and_write_table_in_json(
            path_to_jpg,
            path_to_store_base)
