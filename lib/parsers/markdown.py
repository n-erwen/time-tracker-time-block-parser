import datetime
import re
from lib.datetime_utils import DATETIME_DATE_FORMAT, get_datetime
from lib.parsers._abstract import Parser
from lib.TimeBlock import TimeBlock
from lib.utils import LogLevel, write_to_log_file


class MarkdownTaskListParser(Parser):
    TIME_BLOCK_TAG = '#time-block'
    MARKDOWN_TASK_CAPTURE_REGEX = r'- \[([x ])]( #time-block)? (\d{4}-\d{2}-\d{2}) ?(\d{2}:\d{2})? ?-? ?(\d{2}:\d{2})?(.*)(\n(?:\t| {4})- .*:.*)*'
    DURATION_HOUR_REGEX = r'(\d{1,2})\s?(?:hour[s]?|hr[s]?|h)'
    DURATION_MINUTE_REGEX = r'(\d{1,2})\s?(?:minute[s]?|min[s]?|m)'

    def parse(self, file):
        time_blocks = []
        matches = re.findall(self.MARKDOWN_TASK_CAPTURE_REGEX, file.read())
        for match in matches:
            (checklist_symbol, time_block_tag, date_str, start_time_str,
             end_time_str, description_and_tags_str, child_fields) = match
            description_and_tags_str += (' ' + time_block_tag if time_block_tag else '')
            time_block = self.validate_and_parse_task_data(
                checklist_symbol, date_str, start_time_str,
                end_time_str, description_and_tags_str, child_fields
            )
            if time_block:
                time_blocks.append(time_block)
        return time_blocks

    @classmethod
    def parse_duration_string(cls, duration_str):
        hour_match = re.search(cls.DURATION_HOUR_REGEX, duration_str)
        minute_match = re.search(cls.DURATION_MINUTE_REGEX, duration_str)
        hours = int(hour_match.group(1)) if hour_match else 0
        minutes = int(minute_match.group(1)) if minute_match else 0
        return (hours*60) + minutes

    @staticmethod
    def parse_task_child_fields(child_field_list, delimiter):
        child_field_values = {'details': None, 'duration': None, 'tags': None}
        for child_field_str in child_field_list:
            for field_name in ['details', 'duration', 'tags']:
                regex = rf'- {field_name}{delimiter} (.*)$'
                maybe_field = re.search(regex, child_field_str)
                if maybe_field:
                    child_field_values[field_name] = maybe_field.group(1)
                    break
        return child_field_values

    @classmethod
    def validate_and_parse_task_data(cls, checklist_symbol, date_str, start_time_str, end_time_str,
                                     description, child_fields, tags_str='', child_field_delimiter=':'):
        child_values = cls.parse_task_child_fields(child_fields.replace('\n', '', 1).split('\n'), child_field_delimiter)
        tags = (
                cls.split_tags_str(tags_str or child_values['tags'])
                or [
                    tag for tag in TimeBlock.read_tags_from_description(description)
                    if tag != cls.TIME_BLOCK_TAG
                ]
        )
        details, duration_str = child_values['details'], child_values['duration']
        is_valid, reason = cls.is_time_block_data_valid(
            description, tags_str, start_time_str, end_time_str, duration_str
        )
        if not is_valid:
            write_to_log_file(
                LogLevel.WARNING,
                reason + ' for match: ' +
                str((checklist_symbol, date_str, start_time_str, end_time_str,
                     description, tags_str, details, duration_str))
            )
            return None

        return cls.create_time_block_from_str_data(
            checklist_symbol, date_str, start_time_str, end_time_str, description, tags, details, duration_str
        )

    @classmethod
    def is_time_block_data_valid(cls, description, tags_str, start_time_str, end_time_str, duration_str):
        if (cls.TIME_BLOCK_TAG not in description) and (cls.TIME_BLOCK_TAG not in tags_str):
            return False, 'no #time-block tag'

        if not start_time_str and not end_time_str and not duration_str:
            return False, 'no start time, end time or duration'

        return True, None

    @classmethod
    def split_tags_str(cls, tags_str):
        return [tag for tag in tags_str.split() if tag != cls.TIME_BLOCK_TAG] if tags_str else []

    @classmethod
    def create_time_block_from_str_data(
            cls, checklist_symbol, date_str, start_time_str, end_time_str,
            description, tags, details, duration_str,
    ):
        duration_mins = cls.parse_duration_string(duration_str) if duration_str else None
        return (
            TimeBlock(
                datetime.datetime.strptime(date_str, DATETIME_DATE_FORMAT).date(),
                get_datetime(date_str, start_time_str) if start_time_str else None,
                get_datetime(date_str, end_time_str) if end_time_str else None,
                description.replace(cls.TIME_BLOCK_TAG, '').strip() if description else '',
                details if details else '',
                tags,
                duration_mins if duration_mins else None,
                completed=checklist_symbol == 'x'
            )
        )


class ObsidianMarkdownTaskListParser(MarkdownTaskListParser):
    OBSIDIAN_MARKDOWN_TASK_CAPTURE_REGEX_FORMAT_1 = r'- \[([ x])] (.*?) \| (.*?) \|.* (\d{4}-\d{2}-\d{2}) ?(\d{2}:\d{2})? ?-? ?(\d{2}:\d{2})?(?: \^(?:.*))?((?:\n(?:\t| {4})-.*:: .*)*)'
    OBSIDIAN_MARKDOWN_TASK_CAPTURE_REGEX_FORMAT_2 = r'- \[([ x])] (.*?)\n(?:\t| {4})\((\d{4}-\d{2}-\d{2}) ?(\d{2}:\d{2})? ?-? ?(\d{2}:\d{2})?\)(?: \^(?:.*))?((?:\n(?:\t| {4})-.*:: .*)*)'

    def __init__(self, format_id):
        self.format_id = format_id

    def parse(self, file):
        if self.format_id == 1:
            return self.parse_tasks_from_format_1(file)
        elif self.format_id == 2:
            return self.parse_tasks_from_format_2(file)

    @classmethod
    def parse_tasks_from_format_1(cls, file):
        time_blocks = []
        matches = re.findall(cls.OBSIDIAN_MARKDOWN_TASK_CAPTURE_REGEX_FORMAT_1, file.read())
        for match in matches:
            checklist_symbol, description, tags_str, date_str, start_time_str, end_time_str, child_fields = match
            time_block = cls.validate_and_parse_task_data(
                checklist_symbol, date_str, start_time_str,
                end_time_str, description, child_fields, tags_str, child_field_delimiter='::'
            )
            if time_block:
                time_blocks.append(time_block)
        return time_blocks

    @classmethod
    def parse_tasks_from_format_2(cls, file):
        time_blocks = []
        matches = re.findall(cls.OBSIDIAN_MARKDOWN_TASK_CAPTURE_REGEX_FORMAT_2, file.read())
        for match in matches:
            checklist_symbol, description, date_str, start_time_str, end_time_str, child_fields = match
            time_block = cls.validate_and_parse_task_data(
                checklist_symbol, date_str, start_time_str,
                end_time_str, description, child_fields, child_field_delimiter='::'
            )
            if time_block:
                time_blocks.append(time_block)
        return time_blocks