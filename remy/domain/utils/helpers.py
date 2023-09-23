import re
from datetime import datetime
from remy.domain.constants import TOPIC_NAME_REGEX


def get_parsed_date(date_string):
    if not date_string:
        return None

    return datetime.strptime(date_string, "%d %B, %Y")

def topic_name_validator(topic_name):
    return re.compile(TOPIC_NAME_REGEX).match(topic_name)
