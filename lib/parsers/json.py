import datetime
import json
from lib.datetime_utils import DATETIME_DATE_FORMAT, DATETIME_ISO_FORMAT
from lib.parsers._abstract import Parser
from lib.TimeBlock import TimeBlock


class JSONFileParser(Parser):
    def parse(self, file):
        time_blocks = []
        loaded_json = json.loads(file.read())
        for row in loaded_json:
            time_blocks.append(TimeBlock(
                datetime.datetime.strptime(row['date'], DATETIME_DATE_FORMAT).date(),
                datetime.datetime.strptime(row['start'], DATETIME_ISO_FORMAT) if row['start'] else None,
                datetime.datetime.strptime(row['end'], DATETIME_ISO_FORMAT) if row['end'] else None,
                row['description'],
                row['details'],
                row['tags'],
                row['duration_mins'] if row['duration_mins'] else None,
                row['break_duration_mins'],
                row['completed']
            ))
        return time_blocks
