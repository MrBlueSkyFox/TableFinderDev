# import warnings
#
# warnings.simplefilter(action='ignore', category=FutureWarning)
# from transformers import logging
#
# logging.set_verbosity_error()
import argparse

import torch.jit

# torch.jit.script_method = script_method
torch.jit.script = torch.jit._script_if_tracing
torch.jit.interface = torch.jit._script_if_tracing
from table_finder import TableFinder

if __name__ == "__main__":
    # import torch
    # import numpy
    def script_method(fn, _rcb=None):
        return fn


    def script(obj, optimize=True, _frames_up=0, _rcb=None):
        return obj


    parser = argparse.ArgumentParser()

    parser.add_argument("-p", "--path_to_image", type=str, required=True, help="Path to the image to be processed")
    parser.add_argument("-o", "--output_dir", type=str, required=True,
                        help="Path to the directory where to store the JSON result")
    parser.add_argument("-t", "--tesseract_path", type=str, required=True, help="Path to the Tesseract executable")

    args = parser.parse_args()

    path_to_image = args.path_to_image
    output_dir = args.output_dir
    tesseract_path = args.tesseract_path

    # Process the image using Tesseract and store the results in a JSON file in the output directory

    table_finder = TableFinder()
    table_finder.read_image_and_write_table_in_json(
        path_to_image,
        output_dir)
