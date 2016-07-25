# -*- coding: utf-8 -*-

from flask import Flask
from celery import Celery

celery = Celery('bp_vchat', broker='redis://localhost:6379/11')
celery.conf.update(
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_RESULT_SERIALIZER='json',
    CELERY_TIMEZONE='Europe/Oslo',
    CELERYD_CONCURRENCY=1,
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/11',
    )


def make_celery(app):
    """
    You can use current_app in this celery task.
    which is different from individual celery task.
    param app: flask app instance
    """
    celery = Celery(app.import_name, backend=app.config['CELERY_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery


@celery.task
def send_virtual_msg(virtualId, userId, msg, host):
    path = host
    path += "/im/send_message?"
    path += 'from_id=' + str(virtualId) + '&to_id=' + str(userId) \
            + '&msg_type=TIMTextElem&message='
    path += msg
    ret = requests.get(path).json()
    return json.dumps(ret)


app = Flask(__name__)
celery2 = make_celery(app)
@celery2.task
def celery2_task(arg1, arg2):
    pass


if __name__ == '__main__':
    send_virtual_msg.apply_async(args=[1, 2, 'msg', 'host'], countdown=60)
    celery2_task.apply_async(args=[arg1, arg2], countdown=2)
    print('Done')

