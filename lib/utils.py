import datetime
import os
import sys

log_file_name = os.path.join(
    os.path.dirname(os.path.realpath(sys.argv[0])),
    'log.txt'
)


class LogLevel:
    INFO = 'INFO'
    WARNING = 'WARNING'


def add_tags_to_description(description, tags, tags_first=False):
    updated_description = description
    for tag in tags:
        if tag not in updated_description:
            if tags_first:
                updated_description = tag + ' ' + updated_description
            else:
                updated_description += ' ' + tag
    return updated_description


def write_to_log_file(level_text, text):
    with open(log_file_name, 'a') as log_file:
        log_file.write(datetime.datetime.now().isoformat() + " " + level_text + " " + text + '"\n')
