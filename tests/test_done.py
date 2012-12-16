import unittest

import os
import sys
sys.path.insert(0, "..")

from subprocess import call, Popen, PIPE

from progress.progress import add, load_items, done, PROGRESS_TXT_FILE_NAME, get_item


class TestDone(unittest.TestCase):
    def setUp(self):
        """Clean up old progress files."""
        filelist = [f for f in os.listdir(".") if f.startswith("progress.")]
        for f in filelist:
            os.remove(f)

    def test_done(self):
        """Test adding one item"""
        add('test that will be done')
        items = load_items()
        pk = items[1].pk
        done(pk)
        i = get_item(pk)
        self.assertTrue(i.done)

    def test_done_not_in_txt(self):

        # create progress.yaml
        p = Popen('../progress/progress.py', stdin=PIPE)
        p.communicate('y\n')

        def progress_txt_has_text(text):
            if not os.path.exists(PROGRESS_TXT_FILE_NAME):
                return False
            for line in open(PROGRESS_TXT_FILE_NAME, 'r'):
                if text in line:
                    return True
                return False

        ITEM_TITLE = 'first item'
        call('../progress/progress.py add -t "{0}"'.format(ITEM_TITLE),
             stdout=PIPE, shell=True)
        self.assertTrue(progress_txt_has_text('0 -'))

        call('../progress/progress.py done 0', stdout=PIPE, shell=True)
        self.assertFalse(progress_txt_has_text('0 -'),
                         'item 0 should be done and not on the list')

if __name__ == '__main__':
    unittest.main()
