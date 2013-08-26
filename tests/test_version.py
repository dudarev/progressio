import unittest

import os
import sys
import subprocess

sys.path.insert(0, "..")

from progressio.progressio import __version__


class TestVersion(unittest.TestCase):
    def setUp(self):
        """
        Clean up old progress files.
        """
        filelist = [f for f in os.listdir(".") if f.startswith("progress.")]
        for f in filelist:
            os.remove(f)
        # create progress.db
        p = subprocess.Popen('../progressio/progressio.py', stdin=subprocess.PIPE)
        p.communicate('y\n')

    def test_version(self):
        """
        Test version output.
        """
        output = subprocess.check_output(
            "../progressio/progressio.py version",
            stderr=subprocess.STDOUT,
            shell=True)
        print output
        self.assertTrue(__version__ in output)


if __name__ == '__main__':
    unittest.main()
