from remy.domain.utils.helpers import get_parsed_date

class RecordDTO:

    def __init__(self, **kwargs):
        self.row_id = kwargs.get('row_id')
        self.topic = kwargs.get('topic')
        self.sub_category = kwargs.get('sub_category')
        self.category = kwargs.get('category')
        self.notes = kwargs.get('notes')
        self.learned_on = kwargs.get('learned_on')
        self.last_revised_on = kwargs.get('last_revised_on')
        self.confidence_level = kwargs.get('confidence_level')

    def update_revised_one(self, time_stamp, sheet: 'SheetObject'):
        pass

    @staticmethod
    def get_topic_dto_from_raw_record(raw_record):
        intialization_dict = {
            'row_id': raw_record.get('RowId'),
            'topic': raw_record.get('Topic'),
            'sub_category': raw_record.get('Sub-Category'),
            'category': raw_record.get('Category'),
            'notes': raw_record.get('Notes'),
            'learned_on': get_parsed_date('Date'),
            'last_revised_on': get_parsed_date('Last Revised On')
        }

        return RecordDTO(**intialization_dict)
