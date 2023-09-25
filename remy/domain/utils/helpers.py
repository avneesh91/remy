import re
from datetime import datetime
from remy.domain.constants import TOPIC_NAME_REGEX


def get_parsed_date(date_string):
    if not date_string or date_string == 'None':
        return None

    return datetime.fromisoformat(date_string)

def topic_name_validator(topic_name):
    return re.compile(TOPIC_NAME_REGEX).match(topic_name)
