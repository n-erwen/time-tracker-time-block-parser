import datetime
import json
from lib.datetime_utils import DATETIME_DATE_FORMAT, TIMEZONE
from lib.parsers._abstract import Parser
from lib.TimeBlock import TimeBlock


class JSONFileParser(Parser):
    def parse(self, file):
        time_blocks = []
        loaded_json = json.loads(file.read())
        for row in loaded_json:
            time_blocks.append(TimeBlock(
                datetime.datetime.strptime(row['date'], DATETIME_DATE_FORMAT).date(),
                datetime.datetime.fromisoformat(row['start']).replace(tzinfo=TIMEZONE)
                if row['start'] else None,
                datetime.datetime.fromisoformat(row['end']).replace(tzinfo=TIMEZONE)
                if row['end'] else None,
                row['description'],
                row['details'],
                row['tags'],
                row['duration_mins'] or None,
                row['break_duration_mins'],
                row['completed'],
                row['id'] or None,
            ))
        return time_blocks
