from abc import ABCMeta, abstractmethod
from remy.domain.dtos.record_fetch_dto import RecordFetchDTO
from remy.domain.dtos.record_dto import RecordDTO

class BaseStorage(metaclass=ABCMeta):

    @abstractmethod
    def get_categories(self, topic: str):
        pass

    @abstractmethod
    def get_subcategories(self, category: str):
        pass

    @abstractmethod
    def add_record(self, record_dto: RecordDTO):
        pass

    @abstractmethod
    def get_records(self, record_fetch_dto: RecordFetchDTO):
        pass

    @abstractmethod
    def get_all_topics(self):
        pass

    @abstractmethod
    def add_topic(self, topic_name: str):
        pass

    @abstractmethod
    def delete_topic(self, topic_name: str):
        pass
