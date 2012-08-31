from celery import Celery

celery = Celery('proj.celery',
                broker='amqp://',
                backend='amqp://',
                include=['celery.tasks'])

# Optional configuration, see the application user guide.
# celery.conf.update(
#     CELERY_TASK_RESULT_EXPIRES=3600,
# )
# We should probably create a celeryconfig.py file
# and use that.

if __name__ == '__main__':
    celery.start()
