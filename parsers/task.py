from dmfd import main as dmfd
from avi import main as avi
from data_load import main as data_load

celery_app = Celery('task', brocker='redis://localhost:6379/0')


@celery_app.task
def add():
    dmfd()
    avi()
    data_load()
