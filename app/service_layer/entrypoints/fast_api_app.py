import io
from dataclasses import asdict

from PIL import Image
from fastapi import FastAPI, UploadFile, File

from domain.pydantic.model import TableBox, TableStructureOrderedWithText
from service_layer import handlers, tasks

from settings import SettingsWeb
from .. import dependencies

settings = SettingsWeb()
app = FastAPI()

dependencies.setup(settings)


@app.post("/box")
async def find_table(
        my_file: UploadFile = File(...),
) -> TableBox:
    img_content = await my_file.read()
    img = Image.open(io.BytesIO(img_content))
    table_box = handlers.retrieve_table_box_and_confidence(
        img,
        dependencies.get_table_detector()
    )
    table_box = TableBox(**asdict(table_box))
    return table_box


@app.post("/text")
async def find_text_in_table_image(
        my_file: UploadFile = File(...),

) -> TableStructureOrderedWithText:
    img_content = await my_file.read()
    img = Image.open(io.BytesIO(img_content))
    table_with_text = handlers.retrieve_text_in_table(
        img,
        dependencies.get_table_detector(),
        dependencies.get_table_layout_detection_model(),
        dependencies.get_ocr_modules()
    )
    table_with_text = TableStructureOrderedWithText(**asdict(table_with_text))
    return table_with_text


@app.post("/box_task")
async def find_table_task(
        my_file: UploadFile = File(...),
):
    img_content = await my_file.read()
    img = Image.open(io.BytesIO(img_content))
    task = tasks.task_retrieve_table_box_and_confidence.apply_async(args=[img])
    return task.id


@app.post("/text_task")
async def find_text_in_table_image(
        my_file: UploadFile = File(...)
):
    img_content = await my_file.read()
    img = Image.open(io.BytesIO(img_content))
    task = tasks.task_retrieve_text_in_table.apply_async(args=[img])
    return task.id


@app.get("/task/{job_id}")
async def get_add_dev_info(job_id: str) -> dict:
    return tasks.get_job_info(job_id)
