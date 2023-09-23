import os
import re
from pathlib import Path
from remy.domain.storage import BaseStorage
from remy.domain.dtos.record_dto import RecordDTO
from remy.domain.dtos.record_fetch_dto import RecordFetchDTO

class LocalStorage(BaseStorage):
    REMI_TOPIC_INFO_FILE_REGEX = r'\w+.remy'

    def __init__(self, **kwargs):
        self.storage_path = kwargs.get('storage_path')
        self._remy_file_name_regex = re.compile(LocalStorage.REMI_TOPIC_INFO_FILE_REGEX)
        self._topic_files_dict = {}

        if not self.storage_path:
            self.storage_path = os.path.join(os.path.expanduser('~'), 'remy')

        self._ensure_path()
        self._index_remy_files()


    def _get_remy_file_name(self, topic: str):
        return f'{topic}.remy'

    def get_topic_name_from_file_name(self, file_name: str):
        return file_name.split('.')[0]

    def _ensure_path(self):
        if os.path.isdir(self.storage_path):
            return

        os.makedirs(self.storage_path)

    def _get_remy_file_list(self):
        obj_list = os.listdir(self.storage_path)
        file_list = []

        for obj in obj_list:
            if os.path.isfile(os.path.join(self.storage_path, obj)):
                file_list.append(obj)


        remy_files = []

        for file in file_list:
            if self._remy_file_name_regex.match(file):
                remy_files.append(file)

        return remy_files

    def _index_remy_files(self):
        file_list = self._get_remy_file_list()

        if len(file_list) < 1:
            return

        for file in file_list:
            topic_name = self.get_topic_name_from_file_name(file)
            curr_topic_file = open(os.path.join(self.storage_path, file), 'r')
            topic_text = curr_topic_file.read()
            record_dto_list = map(lambda x: self.process_raw_row(x) , filter(None, topic_text.split('\n')))
            self._topic_files_dict[topic_name] = list(record_dto_list)
            curr_topic_file.close()

    def process_raw_row(self, row):
       curr_list = list(map(lambda x: x.strip(), filter(None,row.split(','))))

       return RecordDTO(**{
            'row_id': curr_list[0],
            'topic': curr_list[1],
            'sub_category': curr_list[2],
            'category': curr_list[3],
            'notes': curr_list[4],
            'learned_on': curr_list[5],
            'last_revised_on': curr_list[6]
       })


    def convert_to_raw_record(self, record_dto: RecordDTO):
        curr_row = ','.join(map(lambda x: str(x), [record_dto.row_id, record_dto.topic, record_dto.sub_category, record_dto.notes, record_dto.learned_on, record_dto.last_revised_on, record_dto.confidence_level]))
        return f'{curr_row}\n'

    def _write_record_to_file(self, record_dto: RecordDTO):
        converted_row = self.convert_to_raw_record(record_dto)
        curr_file = open(os.path.join(self.storage_path, self._get_remy_file_name(record_dto.topic)), 'a')
        curr_file.write(converted_row)
        curr_file.close()

    def _add_topic_file(self, topic_name: str):
        file_name = self._get_remy_file_name(topic_name)
        Path(os.path.join(self.storage_path, file_name)).touch()

        self._topic_files_dict[topic_name] = []


    def get_categories(self, topic: str):
        dto_list = self._topic_files_dict.get(topic)
        return list(set([i.category for i in dto_list]))

    def get_subcategories(self, topic:str, category: str):
        dto_list = self._topic_files_dict.get(topic)
        return list(set([i.sub_category for i in dto_list if i.category == category]))


    def add_record(self, record_dto: RecordDTO):
        curr_topic = record_dto.topic

        topic_list = self._topic_files_dict.get(curr_topic)

        if curr_topic not in self._topic_files_dict.keys():
            self._add_topic_file(curr_topic)

        self._topic_files_dict[curr_topic].append(record_dto)
        self._write_record_to_file(record_dto)

    def get_records(self, record_fetch_dto: RecordFetchDTO):
        pass

    def get_all_topics(self):
        return self._topic_files_dict.keys()

    def add_topic(self, topic_name: str):
        self._add_topic_file(topic_name)

    def delete_topic(self, topic_name: str):
        pass
