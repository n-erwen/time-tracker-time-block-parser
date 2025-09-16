from lib.parsers.csv import CSVFileParser
from lib.parsers.json import JSONFileParser
from lib.parsers.klog import KlogFileParser
from lib.parsers.markdown import MarkdownTaskListParser, ObsidianMarkdownTaskListParser


class InvalidInputFormatException(Exception):
    pass


class TimeBlockParser:
    VALID_FORMATS = [
        'csv', 'json', 'klog', 'markdown_tasklist',
        'obsidian_markdown_tasklist', 'obsidian_markdown_tasklist_2'
    ]

    def __init__(self, format_str):
        if format_str not in self.VALID_FORMATS:
            raise InvalidInputFormatException(
                'Input format must be one of: '
                + ', '.join(['"' + f + '"' for f in self.VALID_FORMATS])
            )
        if format_str == 'csv':
            self.parser = CSVFileParser()
        elif format_str == 'json':
            self.parser = JSONFileParser()
        elif format_str == 'klog':
            self.parser = KlogFileParser()
        elif format_str == 'markdown_tasklist':
            self.parser = MarkdownTaskListParser()
        elif format_str == 'obsidian_markdown_tasklist':
            self.parser = ObsidianMarkdownTaskListParser(format_id=1)
        elif format_str == 'obsidian_markdown_tasklist_2':
            self.parser = ObsidianMarkdownTaskListParser(format_id=2)

    def read(self, file_name):
        with open(file_name, 'r') as file:
            return self.parser.parse(file)
