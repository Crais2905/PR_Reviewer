from app.repositories.connector import Connector
from app.db.models import Review


class ReviewRepo(Connector):
    def __init__(self):
        super().__init__(Review)

