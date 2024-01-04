import io
from typing import Union
from PIL import Image
from fastapi import FastAPI, UploadFile, File
from settings import SettingsWeb
from service_layer import handlers
from service_layer.table_detection import table_model
from service_layer.table_layout_detection import table_layout_model
from service_layer.ocr import tesseract_ocr, easy_ocr
from domain.pydantic.model import TableBox, TableStructureOrderedWithText
from dataclasses import asdict

settings = SettingsWeb()
app = FastAPI()


@app.post("/box")
async def find_table(
        my_file: UploadFile = File(...),
) -> TableBox:
    img_content = await my_file.read()
    img = Image.open(io.BytesIO(img_content))
    table_detection_model = table_model.TableDetector(
        settings.transformer_cache,
        settings.table_detection_model_name,

    )
    table_box = handlers.retrieve_table_box_and_confidence(
        img,
        table_detection_model
    )
    table_box = TableBox(**asdict(table_box))
    return table_box


@app.post("/text")
async def find_text_in_table_image(
        my_file: UploadFile = File(...),

) -> TableStructureOrderedWithText:
    img_content = await my_file.read()
    img = Image.open(io.BytesIO(img_content))
    table_detection_model = table_model.TableDetector(
        settings.transformer_cache,
        settings.table_detection_model_name,

    )
    table_layout_detection_model = table_layout_model.TableLayoutDetector(
        settings.transformer_cache,
        settings.table_layout_model_name
    )
    ocr_tesseract = tesseract_ocr.TesseractOCR(settings.tesseract_path)
    ocr_easy_ocr = easy_ocr.EasyOcr(settings.easy_ocr_cache)
    table_with_text = handlers.retrieve_text_in_table(
        img,
        table_detection_model,
        table_layout_detection_model,
        [ocr_tesseract, ocr_easy_ocr]
    )
    table_with_text = TableStructureOrderedWithText(**asdict(table_with_text))
    return table_with_text
