from ..datetime_utils import DATETIME_DATE_FORMAT, DATETIME_TIME_FORMAT, get_date_as_datetime, get_timedelta_as_string
from ..utils import add_tags_to_description


def get_time_block_data_in_markdown_str_format(time_block):
    return {
        'completed': 'x' if time_block.completed else ' ',
        'date': time_block.date.strftime(DATETIME_DATE_FORMAT),
        'start': time_block.start.strftime(DATETIME_TIME_FORMAT) if time_block.start else '',
        'end': time_block.end.strftime(DATETIME_TIME_FORMAT) if time_block.end else '',
        'duration': get_timedelta_as_string(time_block.duration) if time_block.duration is not None else '',
        'description': time_block.description if time_block.description else '',
        'details': time_block.details if time_block.details else '',
        'tags': ' '.join(time_block.tags),
        'break_duration': get_timedelta_as_string(time_block.break_duration)
    }

def format_time_blocks_to_markdown_tasklist(time_blocks, include_date=False):
    markdown_out_str = ''
    for t in sorted(time_blocks, key=lambda t: t.start or get_date_as_datetime(t.date)):
        time_block_str_data = get_time_block_data_in_markdown_str_format(t)
        markdown_out_str += (
                '- [' + time_block_str_data['completed'] + '] #time-block'
                + (' ' + time_block_str_data['date'] if include_date else '')
                + (' ' + time_block_str_data['start'] + '-' if t.start else '')
                + (time_block_str_data['end'] if t.end else '')
                + ' ' + add_tags_to_description(time_block_str_data['description'], t.tags, tags_first=False)
                + ('\n' + ' ' * 4 + '- details: ' + time_block_str_data['details'] if t.details else '')
                + (
                    '\n' + ' ' * 4 + '- '
                    + ('duration: ' + time_block_str_data['duration'] if t.duration is not None else '')
                    + (' (-' + time_block_str_data['break_duration'] + ' break)' if t.break_duration.seconds > 0 else '')
                    if t.duration is not None or t.break_duration else ''
                )
                + '\n\n'
        )
    return markdown_out_str.rstrip()


def format_time_blocks_to_markdown_table(time_blocks):
    markdown_out_str = ''
    headers = ['Date', 'Start', 'End', 'Description', 'Duration', 'Break Duration', 'Completed']
    markdown_out_str += '| ' + ' | '.join(headers) + ' |'
    markdown_out_str += '\n| ' + ' | '.join(['-' * len(header) for header in headers]) + ' |'
    for t in sorted(time_blocks, key=lambda t: t.start or get_date_as_datetime(t.date)):
        time_block_str_data = get_time_block_data_in_markdown_str_format(t)
        updated_description = add_tags_to_description(time_block_str_data['description'], t.tags)
        table_row = [
            time_block_str_data['date'],
            time_block_str_data['start'] if t.start else '',
            time_block_str_data['end'] if t.end else '',
            updated_description + (' (' + time_block_str_data['details'] + ')' if t.details else ''),
            time_block_str_data['duration'] if t.duration is not None else '',
            time_block_str_data['break_duration'] if t.break_duration.seconds > 0 else '',
            'Yes' if t.completed else 'No'
        ]
        markdown_out_str += '\n| ' + ' | '.join(table_row) + ' |'
    return markdown_out_str


def format_time_blocks_to_obsidian_markdown_tasklist_1(time_blocks):
    markdown_out_str = ''
    for t in sorted(time_blocks, key=lambda t: t.start or get_date_as_datetime(t.date)):
        time_block_str_data = get_time_block_data_in_markdown_str_format(t)
        markdown_out_str += (
                '- [' + time_block_str_data['completed'] + '] '
                + time_block_str_data['description'] + ' | ' + ' '.join(t.tags + ['#time-block']) + ' | '
                + time_block_str_data['date'] + ' '
                + (time_block_str_data['start'] + '-' if t.start else '')
                + (time_block_str_data['end'] if t.end else '')
                + ('\n' + ' ' * 4 + '- details:: ' + time_block_str_data['details'] if t.details else '')
                + (
                    '\n' + ' ' * 4 + '- duration:: '
                    + time_block_str_data['duration']
                    if t.duration is not None else ''
                )
                + '\n\n'
        )
    return markdown_out_str.rstrip()


def format_time_blocks_to_obsidian_markdown_tasklist_2(time_blocks):
    markdown_out_str = ''
    for t in sorted(time_blocks, key=lambda t: t.start or get_date_as_datetime(t.date)):
        time_block_str_data = get_time_block_data_in_markdown_str_format(t)
        markdown_out_str += (
                '- [' + time_block_str_data['completed'] + '] #time-block '
                + time_block_str_data['description']
                + '\n' + ' ' * 4 + '(' + time_block_str_data['date']
                + (' ' + time_block_str_data['start'] + '-' if t.start else '')
                + (time_block_str_data['end'] if t.end else '') + ')'
                + ('\n' + ' ' * 4 + '- tags:: ' + time_block_str_data['tags'] if t.tags else '')
                + ('\n' + ' ' * 4 + '- details:: ' + time_block_str_data['details'] if t.details else '')
                + (
                    '\n' + ' ' * 4 + '- duration:: '
                    + get_timedelta_as_string(t.duration - t.break_duration)
                    if t.duration is not None else ''
                )
                + '\n\n'
        )
    return markdown_out_str.rstrip()
