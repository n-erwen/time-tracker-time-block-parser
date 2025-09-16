from lib.datetime_utils import DATETIME_DATE_FORMAT, DATETIME_ISO_FORMAT, get_date_as_datetime, get_timedelta_as_minutes


def get_time_block_as_csv_row(time_block):
    row_data = [
        time_block.date.strftime(DATETIME_DATE_FORMAT),
        time_block.start.strftime(DATETIME_ISO_FORMAT) if time_block.start else '',
        time_block.end.strftime(DATETIME_ISO_FORMAT) if time_block.end else '',
        str(int(get_timedelta_as_minutes(time_block.duration))) if time_block.duration is not None else '',
        time_block.description,
        ' '.join(time_block.tags) if time_block.tags else '',
        time_block.details if time_block.details else '',
        str(int(get_timedelta_as_minutes(time_block.break_duration))),
        str(int(time_block.completed))
    ]
    return ','.join(['"' + field.replace('"', '""') + '"' for field in row_data])


def format_time_blocks_to_csv(time_blocks):
    csv_out_str = ''
    header_list = [
        'date', 'start', 'end', 'duration_mins', 'description',
        'tags', 'details', 'break_duration_mins', 'completed'
    ]
    csv_out_str += ','.join(['"' + header + '"' for header in header_list])
    sorted_time_blocks = sorted(time_blocks, key=lambda t: t.start or get_date_as_datetime(t.date))
    for t in sorted_time_blocks:
        row_str = get_time_block_as_csv_row(t)
        csv_out_str += '\n' + row_str
    return csv_out_str.rstrip()
