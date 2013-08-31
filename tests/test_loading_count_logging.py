import unittest
from subprocess import Popen, PIPE

import os
import sys
import sqlite3
import subprocess
import time

sys.path.insert(0, "..")

from progressio.progressio import (
    add, get_item,
    load_items, done,
    PROGRESS_DB_FILE_NAME, DATE_FORMAT)


class TestLoading(unittest.TestCase):
    def setUp(self):
        """Clean up old progress files."""
        filelist = [f for f in os.listdir(".") if f.startswith("progress.")]
        for f in filelist:
            os.remove(f)

    def test_get_non_existant_item(self):
        add('test')
        self.assertTrue(get_item(9999999) is None)

    def test_subitem_tabulated(self):
        add('test1')
        add('test2')
        add('subitem of test1', parent_pk=1)
        out, err = Popen(["../progressio/progressio.py"], stdout=PIPE).communicate()
        self.assertTrue('1 - test1\n    3 - subitem of test1' in out)

    def test_count(self):
        add('test1')
        add('test2')
        out, err = Popen(["../progressio/progressio.py", "count"], stdout=PIPE).communicate()
        self.assertTrue('done: 0' in out)
        self.assertTrue('total items: 2' in out)
        items = load_items()
        pk = items[0].pk
        done(pk)
        out, err = Popen(["../progressio/progressio.py", "count"], stdout=PIPE).communicate()
        self.assertTrue('done: 1' in out)
        self.assertTrue('total items: 2' in out)

    def test_count_done_today(self):
        """
        Test that message about count of items done today is shown.
        """
        add("step that will be done")
        items = load_items()
        pk = items[0].pk
        p = subprocess.Popen(
            '../progressio/progressio.py done {}'.format(pk),
            shell=True)
        p.communicate('y\n')
        output = subprocess.check_output(
            '../progressio/progressio.py count',
            stderr=subprocess.STDOUT,
            shell=True)
        self.assertTrue("done today: 1" in output)
        
    def test_count_done_yesterday(self):
        """
        Test that message about count of items done yesterday is shown.
        """
        add("step that will be marked as done yesterday")
        items = load_items()
        pk = items[0].pk
        # updated time to 1 day 1 second ago
        query = "UPDATE item SET is_done='TRUE', done_at='{done_at}' WHERE pk={pk}".format(
            pk=pk,
            done_at=time.strftime(
                DATE_FORMAT, time.localtime(time.time() - 60 * 60 * 24 - 1)
            )
        )
        con = sqlite3.connect(PROGRESS_DB_FILE_NAME)
        cur = con.cursor()
        cur.execute(query)
        con.commit()
        con.close()
        output = subprocess.check_output(
            '../progressio/progressio.py count',
            stderr=subprocess.STDOUT,
            shell=True)
        print output
        self.assertTrue("done yesterday: 1" in output)
        
    def test_log(self):
        add('test1')
        add('test2')

        out, err = Popen(["../progressio/progressio.py", "log"], stdout=PIPE).communicate()
        self.assertTrue('test1' in out)
        self.assertTrue('test2' in out)

        items = load_items()
        pk = items[0].pk
        done(pk)

        out, err = Popen(["../progressio/progressio.py", "log"], stdout=PIPE).communicate()
        self.assertFalse(items[0].title in out)

        out, err = Popen(["../progressio/progressio.py", "log", "-d"], stdout=PIPE).communicate()
        self.assertTrue(items[0].title in out)


if __name__ == '__main__':
    unittest.main()
