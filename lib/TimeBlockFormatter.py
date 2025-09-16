from lib.TimeBlock import TimeBlock

from lib.formatters.csv import format_time_blocks_to_csv
from lib.formatters.json import format_time_blocks_to_json
from lib.formatters.klog import format_time_blocks_to_klog
from lib.formatters.markdown import (
    format_time_blocks_to_markdown_tasklist,
    format_time_blocks_to_markdown_table,
    format_time_blocks_to_obsidian_markdown_tasklist_1,
    format_time_blocks_to_obsidian_markdown_tasklist_2
)


class NonTimeBlocksPassedToFormatterException(Exception):
    pass


class InvalidOutputFormatException(Exception):
    pass


class TimeBlockFormatter:
    VALID_FORMATS = [
        'csv', 'json', 'klog', 'klog_reverse_date_order', 'markdown_table',
        'markdown_tasklist', 'markdown_tasklist_no_date', 'obsidian_markdown_tasklist', 'obsidian_markdown_tasklist_2'
    ]

    def __init__(self, time_blocks):
        if not all([isinstance(maybe_time_block, TimeBlock) for maybe_time_block in time_blocks]):
            raise NonTimeBlocksPassedToFormatterException('Must only provide TimeBlock instances to TimeBlockFormatter')
        self.time_blocks = time_blocks

    def to(self, out_format):
        if out_format not in self.VALID_FORMATS:
            raise InvalidOutputFormatException(
                'Output format must be one of: '
                + ', '.join(['"' + f + '"' for f in self.VALID_FORMATS])
            )

        out_str = None

        if out_format == 'csv':
            out_str = format_time_blocks_to_csv(self.time_blocks)

        elif out_format == 'json':
            out_str = format_time_blocks_to_json(self.time_blocks, separate_date_and_time=False)

        elif out_format == 'klog':
            out_str = format_time_blocks_to_klog(self.time_blocks, reverse_date_order=False)

        elif out_format == 'klog_reverse_date_order':
            out_str = format_time_blocks_to_klog(self.time_blocks, reverse_date_order=True)

        elif out_format == 'markdown_tasklist':
            out_str = format_time_blocks_to_markdown_tasklist(self.time_blocks, include_date=True)

        elif out_format == 'markdown_tasklist_no_date':
            out_str = format_time_blocks_to_markdown_tasklist(self.time_blocks, include_date=False)

        elif out_format == 'obsidian_markdown_tasklist':
            out_str = format_time_blocks_to_obsidian_markdown_tasklist_1(self.time_blocks)

        elif out_format == 'obsidian_markdown_tasklist_2':
            out_str = format_time_blocks_to_obsidian_markdown_tasklist_2(self.time_blocks)

        elif out_format == 'markdown_table':
            out_str = format_time_blocks_to_markdown_table(self.time_blocks)

        return out_str
