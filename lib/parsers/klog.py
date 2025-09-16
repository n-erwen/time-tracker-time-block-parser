import datetime
import re
from lib.datetime_utils import DATETIME_DATE_FORMAT, get_datetime
from lib.parsers._abstract import Parser
from lib.TimeBlock import TimeBlock


class KlogFileParser(Parser):
    def parse(self, file):
        # Not implemented yet
        date_sections = [section.rstrip() for section in self.split_date_sections(file.read())]
        time_blocks = []
        for section in date_sections:
            rows = section.rstrip().split('\n')
            section_date_str = re.search(r'^\d{4}-\d{2}-\d{2}', rows[0]).group()
            for row in rows:
                maybe_time_block = self.create_time_block_instance_from_row(row, section_date_str)
                if isinstance(maybe_time_block, TimeBlock):
                    time_blocks.append(maybe_time_block)
                    continue
                maybe_details = re.search('^ {8}(.*)', row)
                if maybe_details:
                    time_blocks[-1].details = maybe_details.group(1)
                    continue
                maybe_break_mins = re.search(r'^ {4}-(\d+)m', row)
                if maybe_break_mins:
                    time_blocks[-1].add_break_time(minutes=int(maybe_break_mins.group(1)))
        return time_blocks

    @staticmethod
    def split_date_sections(file_content):
        sections = []
        date_matches = list(re.finditer(r'\d{4}-\d{2}-\d{2}', file_content))
        for match_index in range(len(date_matches)):
            if match_index + 1 < len(date_matches):
                sections.append(file_content[date_matches[match_index].start():date_matches[match_index+1].start()])
            else:
                sections.append(file_content[date_matches[match_index].start():])
        return sections

    @staticmethod
    def create_time_block_instance_from_row(row_str, date_str):
        match = re.match(r'^ {4}(\d{1,2}:\d{2}) ?- ?(\?|\d{1,2}:\d{2}) ?(.*)?$', row_str)

        if match:
            tags = TimeBlock.read_tags_from_description(match.group(3))
            description = match.group(3)
            for tag in tags:
                description = description.replace(tag, tag.replace('=', '/'))
            return TimeBlock(
                datetime.datetime.strptime(date_str, DATETIME_DATE_FORMAT).date(),
                get_datetime(date_str, match.group(1)),
                get_datetime(date_str, match.group(2)) if match.group(2) != '?' else None,
                description
            )

        return None
