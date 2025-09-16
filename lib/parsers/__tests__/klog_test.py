import datetime
import unittest

from lib.parsers.klog import KlogFileParser


class TestKlogFileParser(unittest.TestCase):
    klog_file_parser = KlogFileParser()

    def test_valid_single_record(self):
        test_input = """2025-09-08 (7h!)
Record Description
    13:14-13:31 test #nested=tag #tag2
        details
    -4m break"""
        result = self.klog_file_parser.parse(test_input)
        self.assertEqual(len(result), 1)
        time_block = result[0]
        self.assertEqual(
            time_block.start,
            datetime.datetime(2025, 9, 8, 13, 14)
        )
        self.assertEqual(
            time_block.end,
            datetime.datetime(2025, 9, 8, 13, 31)
        )
        self.assertEqual(time_block.description, 'test #nested/tag #tag2')
        self.assertEqual(time_block.tags, ['#nested/tag', '#tag2'])
        self.assertEqual(time_block.details, 'details')
        self.assertEqual(time_block.duration, datetime.timedelta(minutes=17))
        self.assertEqual(time_block.break_duration, datetime.timedelta(minutes=4))
