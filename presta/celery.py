from __future__ import absolute_import

from celery import Celery

celery = Celery('presta.celery',
                broker='amqp://',
                backend='amqp://',
                include=['presta.tasks'])

# Optional configuration, see the application user guide.
# celery.conf.update(
#     CELERY_TASK_RESULT_EXPIRES=3600,
# )
# We should probably create a celeryconfig.py file
# and use that.

if __name__ == '__main__':
    celery.start()
