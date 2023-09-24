from remy.domain.dtos.record_dto import RecordDTO

class TopicRevisionHandler:

    def __init__(self, **kwargs):
        self.storage_handler = kwargs.get('storage_handler')
