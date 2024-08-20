from celery.app import Celery


celery = Celery(
    "smart-u",
    broker="redis://localhost:6379/2",
    backend="redis://localhost:6379/3",
    include=["app.services.tasks.pair_tasks"],
)

celery.conf.update(
    result_expires=3600,  # Время хранения результатов
)
