import os
import argparse

from settings import SettingsCLI

os.environ['MAGICK_HOME'] = './wand'
os.environ["CURL_CA_BUNDLE"] = ""
default_transformer_cache = 'models/'
default_easy_ocr_models = "models/easy_ocr"


def get_basename(path: str) -> str:
    base_file_name = os.path.basename(path)
    base_file_name = os.path.splitext(base_file_name)[0]
    return base_file_name


def create_output_json(path: str, file_name: str) -> str:
    return os.path.join(path, file_name + ".json")


def args_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument("-p", "--path_to_image", type=str, required=True, help="Path to the image to be processed")
    parser.add_argument("-o", "--output_dir", type=str, required=True,
                        help="Path to the directory where to store the JSON result")
    parser.add_argument("-t", "--tesseract_path", type=str, required=False, help="Path to the Tesseract executable")
    parser.add_argument("-t_cache", "--transformer_cache", type=str, required=False,
                        help="Path to the Transformers cache")
    parser.add_argument("-ocr_cache", "--easy_ocr_cache", type=str, required=False,
                        help="Path to the Easy ocr cache models")
    parser.add_argument("-d", "--use_deskew", type=bool, required=False, default=False,
                        help="use deskew")
    arguments = parser.parse_args()
    return arguments


if __name__ == "__main__":
    args = args_parser()
    settings = SettingsCLI(**vars(args))
    os.environ['CURL_CA_BUNDLE'] = ''
    os.environ['REQUESTS_CA_BUNDLE'] = ''
    if settings.easy_ocr_cache:
        default_easy_ocr_models = settings.easy_ocr_cache
        os.environ['EASYOCR_MODULE_PATH'] = default_easy_ocr_models
    import torch.jit
    import warnings

    warnings.simplefilter(action='ignore', category=FutureWarning)

    torch.jit.script = torch.jit._script_if_tracing
    torch.jit.interface = torch.jit._script_if_tracing
    from transformers import logging

    logging.set_verbosity_error()
    path_to_image = args.path_to_image
    output_dir = args.output_dir
    # tesseract_path = args.tesseract_path

    import PIL.Image

    from service_layer.table_detection.table_model import TableDetector
    from service_layer.table_layout_detection.table_layout_model import TableLayoutDetector

    from service_layer import handlers
    from service_layer.table_detection.table_detection_processing import NotFoundTable

    try:
        img = PIL.Image.open(settings.path_to_image)
        img_name = get_basename(settings.path_to_image)
        output_json_name = create_output_json(settings.output_dir, img_name)
        table_detector = TableDetector(
            settings.transformer_cache,
            settings.table_detection_model_name
        )
        table_layout_detector = TableLayoutDetector(
            settings.transformer_cache,
            settings.table_layout_model_name
        )
        table_ordered = handlers.retrieve_table_layout_with_ordering(
            img,
            table_detector,
            table_layout_detector
        )
        from dataclasses import asdict
        import json

        with open(output_json_name, "w", encoding="utf8") as file:
            json.dump(asdict(table_ordered), file, indent=4)
    except NotFoundTable:
        print(f"No table for {img_name}")
    print(table_ordered)
    # Process the image using Tesseract and store the results in a JSON file in the output directory
    # from table_extractor import TableExtractor
    #
    # table_finder = TableExtractor(tesseract_path, dir_to_trans_cache=default_transformer_cache,
    #                               use_deskew=args.use_deskew)
    # table_finder.read_image_and_write_table_in_json(
    #     path_to_image,
    #     output_dir)
