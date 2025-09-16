import itertools
from lib.datetime_utils import DATETIME_DATE_FORMAT, DATETIME_TIME_FORMAT, get_date_as_datetime, get_timedelta_as_string
from lib.utils import LogLevel, add_tags_to_description, write_to_log_file


def format_time_blocks_to_klog(time_blocks, reverse_date_order=False):
    klog_records = []
    sorted_time_blocks = sorted(time_blocks, key=lambda t: t.start or get_date_as_datetime(t.date))
    grouped_by_date_time_blocks = itertools.groupby(
        sorted_time_blocks, lambda t: (t.start or t.date).strftime(DATETIME_DATE_FORMAT)
    )
    for key, group in grouped_by_date_time_blocks:
        klog_record_str = key + '\n'
        for t in group:
            if not t.start:
                write_to_log_file(
                    LogLevel.WARNING, 'Excluding time block with no start date from klog output: ' + repr(t)
                )
                continue
            updated_description = add_tags_to_description(t.description, t.tags)
            for tag in t.tags:
                updated_description = updated_description.replace(tag, tag.replace('/', '=', 1))
            klog_record_str += (
                    ' ' * 4 + t.start.strftime(DATETIME_TIME_FORMAT)
                    + '-' + (t.end.strftime(DATETIME_TIME_FORMAT) if t.end else '?')
                    + ' ' + updated_description + '\n'
                    + (' ' * 8 + t.details + '\n' if t.details else '')
                    + (' ' * 4 + '-' + get_timedelta_as_string(t.break_duration) + ' break' + '\n'
                       if t.break_duration.seconds > 0 else '')
            )
        klog_records.append(klog_record_str)

    return '\n'.join(reversed(klog_records) if reverse_date_order else klog_records).rstrip()
