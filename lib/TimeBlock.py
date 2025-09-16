import datetime
import re


class TimeBlock:
    def __init__(self, date, start=None, end=None, description='', details='',
                 tags=None, duration_mins=None, break_mins=0, completed=None, id=None):
        if tags is None:
            tags = []
        self.id = id
        self.date = date
        self.start = start
        self.end = end or self.calculate_end_time(self.start, duration_mins)
        self.duration = (
            datetime.timedelta(minutes=duration_mins)
            if duration_mins else (self.end - self.start if self.start and self.end else None)
        )
        self.completed = completed if completed is not None else bool(self.start and self.end or self.duration)
        self.description = description
        self.details = details
        self.tags = tags or self.read_tags_from_description(self.description)
        self.break_duration = (
            datetime.timedelta(minutes=break_mins)
            if break_mins > 0 else (self.end - self.start - self.duration if self.start and self.end and self.duration
                                    else datetime.timedelta(minutes=0))
        )

    def __repr__(self):
        return (
                'TimeBlock('
                + 'date="' + str(self.date) + '", '
                + 'start=' + ('"' + str(self.start) + '"' if self.start else 'None') + ', '
                + 'end=' + ('"' + str(self.end) + '"' if self.end else 'None') + ', '
                + 'duration=' + ('"' + str(self.duration) + '"' if self.duration else 'None') + ', '
                + 'description="' + self.description + '", '
                + 'details="' + self.details + '", '
                + 'tags=[' + ','.join(['"' + tag + '"' for tag in self.tags]) + '],'
                + 'break_duration="' + str(self.break_duration) + '", '
                + 'completed=' + ('True' if self.completed else 'False') + ', '
                + 'id=' + ('"' + str(self.id) + '"' if self.id else '') + ')'
        )

    @staticmethod
    def calculate_end_time(start_datetime, duration_mins=None):
        return start_datetime + datetime.timedelta(minutes=duration_mins) if start_datetime and duration_mins else None

    @staticmethod
    def read_tags_from_description(description):
        return re.findall(r'#[a-zA-Z0-9\-_=/]+', description)

    def add_break_time(self, hours=0, minutes=0):
        minutes_to_add = hours*60 + minutes
        self.break_duration += datetime.timedelta(minutes=minutes_to_add)
