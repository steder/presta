from presta.celery import celery

@celery.task
def add(x, y):
    """sanity check task"""
    return x + y
