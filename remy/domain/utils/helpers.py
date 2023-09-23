from datetime import datetime

def get_parsed_date(date_string):
    if not date_string:
        return None

    return datetime.strptime(date_string, "%d %B, %Y")
