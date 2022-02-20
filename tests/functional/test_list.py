import unittest

import os
import sys
import subprocess

sys.path.insert(0, "..")


SAMPLE_TASKS = """task 1
    subtask 1-1
task 2
    subtask 2-1
        subtask 2-1-1
    subtask 2-2
"""


class TestList(unittest.TestCase):
    def setUp(self):
        """Clean up old progress files."""
        filelist = [f for f in os.listdir(".") if f.startswith("progress.")]
        filelist.extend([f for f in os.listdir(".") if f.startswith("TASKS.")])
        for f in filelist:
            os.remove(f)

    def test_list_all(self):
        """ Test listing all items """
        with open('TASKS.md', 'w') as f:
            f.write(SAMPLE_TASKS)
        output = subprocess.check_output(
            '../../progressio/progressio.py',
            stderr=subprocess.STDOUT,
            shell=True)
        print('output=', output)
        self.assertEqual(output, SAMPLE_TASKS)


if __name__ == '__main__':
    unittest.main()
