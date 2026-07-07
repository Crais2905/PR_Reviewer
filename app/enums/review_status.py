from enum import Enum


class ReviewStatus(Enum):
    pending = "pending"
    processing = "processing"
    completed = "completed"
    failed = "failed"
