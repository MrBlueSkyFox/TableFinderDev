import io
from dataclasses import asdict

from PIL import Image
from fastapi import FastAPI, UploadFile, File, Depends

from domain.pydantic.model import TableBox, TableStructureOrderedWithText
from service_layer import handlers
from settings import SettingsWeb
from .. import dependencies

settings = SettingsWeb()
app = FastAPI()


def start_up():
    dependencies.get_table_detector(
        settings.transformer_cache,
        settings.table_detection_model_name
    )
    dependencies.get_table_layout_detection_model(
        settings.transformer_cache,
        settings.table_layout_model_name
    )
    dependencies.get_tesseract_ocr(
        settings.tesseract_path
    )
    dependencies.get_easy_ocr(
        settings.easy_ocr_cache
    )
    dependencies.get_ocr_modules()


start_up()


@app.post("/box")
async def find_table(
        my_file: UploadFile = File(...),
        table_detection_model=Depends(dependencies.get_table_detector),
) -> TableBox:
    img_content = await my_file.read()
    img = Image.open(io.BytesIO(img_content))
    table_box = handlers.retrieve_table_box_and_confidence(
        img,
        table_detection_model
    )
    table_box = TableBox(**asdict(table_box))
    return table_box


@app.post("/text")
async def find_text_in_table_image(
        my_file: UploadFile = File(...),
        table_detection_model=Depends(dependencies.get_table_detector),
        table_layout_detection_model=Depends(dependencies.get_table_layout_detection_model),
        ocr_modules_available=Depends(dependencies.get_ocr_modules),

) -> TableStructureOrderedWithText:
    img_content = await my_file.read()
    img = Image.open(io.BytesIO(img_content))
    table_with_text = handlers.retrieve_text_in_table(
        img,
        table_detection_model,
        table_layout_detection_model,
        ocr_modules_available
    )
    table_with_text = TableStructureOrderedWithText(**asdict(table_with_text))
    return table_with_text
