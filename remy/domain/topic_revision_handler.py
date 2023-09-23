from domain.dtos.topic_dto import TopicDTO
from domain.constants import TOPICS, TIME_CONSTRAINT

class TopicRevisionHandler:

    def __init__(self, **kwargs):
        self.storage_handler = kwargs.get('storage_handler')
