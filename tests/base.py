import os
import subprocess
import unittest


class BaseCase(unittest.TestCase):
    
    def setUp(self):
        # clean up old progress files
        filelist = [f for f in os.listdir(".") if f.startswith("progress.")]
        for f in filelist:
            os.remove(f)
        # create progressio.db
        p = subprocess.Popen('../progressio/progressio.py', stdin=subprocess.PIPE)
        p.communicate('y\n')
