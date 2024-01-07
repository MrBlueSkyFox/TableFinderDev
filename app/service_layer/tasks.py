from celery import Celery, shared_task
from celery.result import AsyncResult
from celery.utils.log import get_task_logger

from service_layer import handlers
from settings import SettingsWeb
from . import dependencies

settings = SettingsWeb()

app_celery = Celery('tasks',
                    broker=settings.CELERY_BROKER_URL,
                    backend=settings.CELERY_RESULT_BACKEND
                    )

app_celery.conf.update(
    accept_content=settings.CELERY_ACCEPT_CONTENT,
    task_serializer='pickle',
    result_serializer='pickle',
    worker_send_task_events=True,
    worker_prefetch_multiplier=1
)

LOGGER = get_task_logger(__name__)

(
    table_detection_model,
    table_layout_detection_model,
    ocr_modules_available,
    *_
) = dependencies.setup(settings)


def get_job_info(job_id):
    task_result = AsyncResult(job_id)
    result = {
        "id": job_id,
        "status": task_result.status,
        "result": task_result.result
    }
    return result


@shared_task(bind=True, max_retries=5)
def task_retrieve_table_box_and_confidence(self, img):
    table_box = handlers.retrieve_table_box_and_confidence(
        img,
        table_detection_model
    )
    return table_box


@shared_task(bind=True, max_retries=5)
def task_retrieve_text_in_table(self, img):
    table_with_text = handlers.retrieve_text_in_table(
        img,
        table_detection_model,
        table_layout_detection_model,
        ocr_modules_available
    )
    return table_with_text
