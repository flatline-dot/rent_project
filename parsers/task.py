from celery import Celery
from dmfd import main as dmfd
from avi import main as avi
from data_load import main as data_load

celery_app = Celery('task', broker='redis://localhost:6379/0')


@celery_app.task
def add(num_pages):
    dmfd(num_pages)
    avi(num_pages)
    data_load()
