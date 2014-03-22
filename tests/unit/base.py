import os
import sys
import unittest

sys.path.insert(0, "../..")
from progressio.progressio import PROGRESSIO_DIR


class BaseUnitCase(unittest.TestCase):
    
    def setUp(self):
        # clean up old progress files
        if os.path.exists(PROGRESSIO_DIR):
            for f in os.listdir(PROGRESSIO_DIR):
                os.remove(os.path.join(PROGRESSIO_DIR, f))
