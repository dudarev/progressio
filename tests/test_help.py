import unittest

import os
import sys
import subprocess

sys.path.insert(0, "..")


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

    def test_help(self):
        """
        Test help is shown for `help`, `-h`, `--help` commands.
        """
        output = subprocess.check_output(
            "../progressio/progressio.py help",
            stderr=subprocess.STDOUT,
            shell=True)
        print output
        self.assertTrue('usage:' in output)

        output = subprocess.check_output(
            "../progressio/progressio.py -h",
            stderr=subprocess.STDOUT,
            shell=True)
        print output
        self.assertTrue('usage:' in output)

        output = subprocess.check_output(
            "../progressio/progressio.py --help",
            stderr=subprocess.STDOUT,
            shell=True)
        print output
        self.assertTrue('usage:' in output)


if __name__ == '__main__':
    unittest.main()
