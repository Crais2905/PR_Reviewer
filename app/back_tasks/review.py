from asgiref.sync import async_to_sync

from app.celery_app import celery
from app.db.session import get_session
from app.repositories.review import ReviewRepo
from app.services.bg_review import BGReviewService


@celery.task(name="app.back_tasks.review.create_review_task")
def create_review_task(
    review_id: int
):
        service = BGReviewService(ReviewRepo())
        async_to_sync(service.review_process)(review_id)

