#!/usr/bin/python3

from os.path import realpath
from lib.parse_args import parse_args
from lib.TimeBlockFormatter import TimeBlockFormatter
from lib.TimeBlockParser import TimeBlockParser
from lib.utils import LogLevel, write_to_log_file

if __name__ == '__main__':
    arg_values, input_files = parse_args([
        {'name': 'from', 'shorthand': 'f', 'is_bool': False},
        {'name': 'to', 'shorthand': 't', 'is_bool': False}
    ])
    input_format, output_format = arg_values['from'], arg_values['to']
    all_time_blocks = []
    parser = TimeBlockParser(input_format)
    for file_name in input_files:
        file_time_blocks = parser.read(file_name)
        write_to_log_file(LogLevel.INFO, 'parsed ' + str(len(file_time_blocks)) + ' records from file: "' + realpath(file_name))
        all_time_blocks += file_time_blocks
    formatter = TimeBlockFormatter(all_time_blocks)
    if output_format == 'klog':
        write_to_log_file(LogLevel.WARNING, 'Completion status is ignored when writing to klog output')
    output = formatter.to(output_format)
    print(output)
