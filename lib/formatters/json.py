import datetime
import json
from lib.datetime_utils import (
    DATETIME_DATE_FORMAT, DATETIME_TIME_FORMAT,
    get_date_as_datetime, get_timedelta_as_minutes
)


def format_time_blocks_to_json(time_blocks, separate_date_and_time=False):
    time_block_dicts = []
    sorted_time_blocks = sorted(time_blocks, key=lambda t: t.start or get_date_as_datetime(t.date))
    for t in sorted_time_blocks:
        t_dict = {
            'id': t.id,
            'date': t.date.strftime(DATETIME_DATE_FORMAT),
            'start': t.start.isoformat() if t.start else None,
            'end': t.end.isoformat() if t.end else None,
            'duration_mins': int(get_timedelta_as_minutes(t.duration)) if t.duration is not None else None,
            'description': t.description,
            'details': t.details,
            'tags': t.tags,
            'break_duration_mins': int(get_timedelta_as_minutes(t.break_duration)),
            'completed': t.completed
        }
        if separate_date_and_time:
            t_dict = {
                **t_dict,
                'start': datetime.datetime.fromisoformat(t_dict['start']).strftime(
                    DATETIME_TIME_FORMAT),
                'end':
                    datetime.datetime.fromisoformat(t_dict['end']).strftime(DATETIME_TIME_FORMAT)
                    if t_dict['end'] else None
            }
        time_block_dicts.append(t_dict)
    return json.dumps(time_block_dicts, indent=4)
