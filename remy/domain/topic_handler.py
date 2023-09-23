from domain.dtos.topic_dto import TopicDTO
from domain.constants import TOPICS, TIME_CONSTRAINT

class TopicHandler:

    def __init__(self, **kwargs):
        self._topic_sheet = kwargs.get('topic_sheet')
        self._topic_dto_list_dict = {}

    def get_ds_algo_topic_dtos(self) -> [TopicDTO]:
        record_list = self._topic_sheet.get_all_records()

        curr_row_id = 1
        topic_dto_list = []

        for record in record_list:
            record['RowId'] = curr_row_id
            topic_dto_list.append(TopicDTO.get_topic_dto_from_raw_record(record))
            curr_row_id = curr_row_id + 1

        self._topic_dto_list_dict[TOPICS.DS_ALGO] = topic_dto_list

        return topic_dto_list

    def get_revision_recommendation(self, time_constraint):
        if time_constraint == TIME_CONSTRAINT.TIME_CRUNCH:
            pass
        elif time_constraint == TIME_CONSTRAINT.HOUR:
            pass
        elif time_constraint == TIME_CONSTRAINT.MORE_THAN_A_HOUR:
            pass
