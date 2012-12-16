import unittest

import os
import sys
sys.path.insert(0, "..")


class TestLoading(unittest.TestCase):
    def setUp(self):
        """Clean up old progress files."""
        filelist = [f for f in os.listdir(".") if f.startswith("progress.")]
        for f in filelist:
            os.remove(f)


if __name__ == '__main__':
    unittest.main()
