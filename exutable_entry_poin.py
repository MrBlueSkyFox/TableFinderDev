import os
import argparse

default_transformer_cache = 'models/'
default_easy_ocr_models = "models/easy_ocr"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-p", "--path_to_image", type=str, required=True, help="Path to the image to be processed")
    parser.add_argument("-o", "--output_dir", type=str, required=True,
                        help="Path to the directory where to store the JSON result")
    parser.add_argument("-t", "--tesseract_path", type=str, required=False, help="Path to the Tesseract executable")
    parser.add_argument("-t_cache", "--transformer_cache", type=str, required=False,
                        help="Path to the Transformers cache")
    parser.add_argument("-ocr_cache", "--easy_ocr_cache", type=str, required=False,
                        help="Path to the Easy ocr cache models")
    args = parser.parse_args()
    path_to_transformers_cache = args.transformer_cache
    path_to_easy_ocr_models = args.easy_ocr_cache
    if path_to_transformers_cache:
        default_transformer_cache = path_to_transformers_cache
    os.environ['TRANSFORMERS_CACHE'] = default_transformer_cache
    os.environ['HF_HOME'] = default_transformer_cache
    os.environ['XDG_CACHE_HOME'] = default_transformer_cache

    if path_to_easy_ocr_models:
        default_easy_ocr_models = path_to_easy_ocr_models
    os.environ['EASYOCR_MODULE_PATH'] = default_easy_ocr_models
    import torch.jit

    torch.jit.script = torch.jit._script_if_tracing
    torch.jit.interface = torch.jit._script_if_tracing
    import warnings

    warnings.simplefilter(action='ignore', category=FutureWarning)
    from transformers import logging

    logging.set_verbosity_error()
    path_to_image = args.path_to_image
    output_dir = args.output_dir
    tesseract_path = args.tesseract_path

    # Process the image using Tesseract and store the results in a JSON file in the output directory
    from table_finder import TableFinder

    table_finder = TableFinder(tesseract_path)
    table_finder.read_image_and_write_table_in_json(
        path_to_image,
        output_dir)
