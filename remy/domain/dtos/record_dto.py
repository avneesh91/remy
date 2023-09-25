import uuid
import math

import datetime
from rich.console import Console
from rich.table import Table
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

    def days_since_learned(self) -> int:
        diff = datetime.datetime.now() - self.learned_on
        return math.floor(diff.total_seconds()/(60 * 60 * 24))

    def update_revised_one(self, time_stamp, sheet: 'SheetObject'):
        pass

    @staticmethod
    def get_new_record_dto(topic_name: str):
        dto = RecordDTO()
        dto.row_id = str(uuid.uuid4())
        dto.topic = topic_name
        dto.learned_on = datetime.datetime.now()
        return dto

    @staticmethod
    def get_table_with_columns(table_heading='New Record Addition'):
        table = Table(title=table_heading)
        table.add_column("Row Id", style="cyan", no_wrap=True)
        table.add_column("Topic", style="magenta")
        table.add_column("Sub-Category", style="magenta")
        table.add_column("Category", style="magenta")
        table.add_column("Notes", no_wrap=False)
        table.add_column("Learned On", style="green")
        table.add_column("Last Revised On")
        table.add_column("Confidence Level")
        return table

    def get_record_table_for_print(self):
        table = RecordDTO.get_table_with_columns()
        table.add_row(self.row_id, self.topic, self.sub_category, self.category, self.notes, str(self.learned_on), str(self.last_revised_on), self.confidence_level)
        return table

    def get_record_row_for_table(self, table):
        table.add_row(self.row_id, self.topic, self.sub_category, self.category, self.notes, str(self.learned_on), str(self.last_revised_on), self.confidence_level)
        return table


