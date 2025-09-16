import csv
import datetime
from lib.datetime_utils import DATETIME_DATE_FORMAT, DATETIME_ISO_FORMAT
from lib.parsers._abstract import Parser
from lib.TimeBlock import TimeBlock


class CSVFileParser(Parser):
    def parse(self, file):
        time_blocks = []
        reader = csv.DictReader(file)
        for row in reader:
            time_blocks.append(TimeBlock(
                datetime.datetime.strptime(row['date'], DATETIME_DATE_FORMAT).date(),
                datetime.datetime.strptime(row['start'], DATETIME_ISO_FORMAT) if row['start'] else None,
                datetime.datetime.strptime(row['end'], DATETIME_ISO_FORMAT) if row['end'] else None,
                row['description'],
                row['details'],
                row['tags'].split(' '),
                int(row['duration_mins']) if row['duration_mins'] else None,
                int(row['break_duration_mins']),
                bool(row['completed']),
                row['id'] or None
            ))
        return time_blocks
