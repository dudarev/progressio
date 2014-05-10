#!/usr/bin/python
"""
Data structure:

Each task/step/ticket is an Item instance.

Each item may have one parent and several children nodes.
"""

import os
import re
import string
import sqlite3
import sys
import time
from datetime import datetime

__version__ = '0.4.0-dev'
__author__ = "Artem Dudarev"
__url__ = 'https://github.com/dudarev/progressio'

DATE_FORMAT = '%Y%m%d%H%M%S'
PROGRESS_DB_FILE_NAME = 'progress.db'
PROGRESSIO_DIR = '.progressio'
PROGRESS_FILENAME = 'progress.txt'
FULL_PROGRESS_FILENAME = os.path.join(PROGRESSIO_DIR, PROGRESS_FILENAME)
DONE_FILENAME = 'done.txt'
BASE_FOR_HASH = 36
ITEM_TAB = 2 * ' '


def base_encode(num, base, dd=False):
    """http://www.daniweb.com/forums/thread159163.html
    to convert back  int(string, 36)
    """
    if not 2 <= base <= 36:
        raise ValueError('The base number must be between 2 and 36.')
    if not dd:
        dd = dict(zip(range(36), list(string.digits + string.ascii_lowercase)))
    if num < base:
        return dd[num]
    num, rem = divmod(num, base)
    return base_encode(num, base, dd) + dd[rem]


class Item(object):
    """
    The following fields are stored in the database:

    pk (id)     - int
    path        - str - a string that represents order for its parent
    parent      - parent of the item
    children    - str - a list of children ids, order is important
    title       - str - title
    added_at    - datetime
    is_done     - boolean
    done_at     - datetime
    """

    def __init__(self, path=None, children=None, parent=None,
                 title=None, added_at=None, is_done=False, done_at=None):
        self.path = path
        if children is not None:
            self.children = map(int, filter(None, children.split(',')))
        else:
            self.children = []
        self.parent = parent
        self.title = title
        self.added_at = added_at
        self.is_done = is_done
        self.done_at = done_at
        self.level = 0

    def add_child(self, child):
        self.children.append(child)
        child.parent = self

    def remove_from_children(self):
        if self.parent:
            self.parent.children.remove(self)
            self.parent = None

    def __str__(self):
        return self.__unicode__()

    def __repr__(self):
        return self.__unicode__()

    def __unicode__(self):
        return '{}'.format(self.title)

    def __cmp__(self, other):
        return cmp(int(self.pk), int(other.pk))

    def __hash__(self):
        return int(self.added_at.strftime(DATE_FORMAT))

    @property
    def hash_str(self):
        # reversed string in BASE_FOR_HASH corresponding to hash
        return ''.join(reversed(base_encode(hash(self), BASE_FOR_HASH)))

    @property
    def children_str(self):
        return ','.join(set(map(str, self.children)))

    def show(self):
        print self.level * ITEM_TAB + str(self)


def _create_db_if_needed():
    """
    Checks if db file exists. Creates it if it does not exist.

    :returns: a string with message describing what happened.
    """

    if not os.path.exists(PROGRESS_DB_FILE_NAME):
        con = sqlite3.connect(PROGRESS_DB_FILE_NAME)
        cur = con.cursor()
        # root item that has pk=0 is always considered done
        cur.execute(
            "CREATE TABLE item(" +
            "pk INTEGER PRIMARY KEY, children, title, added_at, is_done DEFAULT FALSE, done_at)")
        cur.execute("INSERT INTO item(pk, children, title, is_done) values(0, '', 'root', 1)")
        con.commit()
        con.close()
        return 'DB file did not exist and was created.'

    return 'DB file exists'


def _create_dir_if_needed():
    if not os.path.exists(PROGRESSIO_DIR):
        os.makedirs(PROGRESSIO_DIR)


def _parse_file(filename):
    """Parses an item for a string.

    :param filename: name of the file to parse
    :type filename: str
    :rtype: Item
    """
    item = Item(1)
    basename = os.path.basename(filename)
    with open(filename, 'r') as f:
        item.title = f.readline()
        item.path = basename.split('-')[0]
    return item


def _parse_line(line):
    item = Item(title=line.strip())
    return item


def _get_filename(s, parent_hash=0):
    """Returns file with count prepended.
    It is incremented until such count does not exist.
    """
    allowed_characters = string.ascii_lowercase + string.digits + ' '
    # leave only allowed characters
    s_filtered = ''.join([l for l in s.lower() if l in allowed_characters])
    # timestamp to prepend
    items = load_items_list()
    paths_taken = [int(i.path) for i in items]
    path = 1
    while path in paths_taken:
        path += 1
    # filename always has '-' after timestamp
    return str(path) + '-' + '-'.join(s_filtered.split())


def count_items():
    """
    :returns: a dictionary with counts in fields 'total', 'done'.
    """
    con = sqlite3.connect(PROGRESS_DB_FILE_NAME)
    cur = con.cursor()
    # do not count root
    cur.execute("SELECT COUNT(*) FROM item WHERE pk<>0")
    total = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM item WHERE is_done='TRUE' AND pk<>0")
    done = cur.fetchone()[0]
    done_items = load_items_list(is_done=True)
    done_today = 0
    done_yesterday = 0
    for i in done_items:
        date_item = datetime.strptime(i.done_at, DATE_FORMAT)
        date_now = datetime.now()
        if date_now.date() == date_item.date():
            done_today += 1
        if (date_now.date() - date_item.date()).days == 1:
            done_yesterday += 1
    return {
        'done': done,
        'total': total,
        'done_today': done_today,
        'done_yesterday': done_yesterday,
    }


def load_items_list(is_done=False):
    """
    :returns: a list with Item instances that are NOT done.
    """
    items_list = []
    with open(FULL_PROGRESS_FILENAME, 'r') as f:
        items_list = [_parse_line(line) for line in f]
    return items_list


def load_items_dict(is_done=False):
    """
    :returns: a dict with Item instances that are NOT done.
    """
    items = {}
    items_list = load_items_list()
    for j, item in enumerate(items_list):
        item.path_id = j + 1
        items[str(j + 1)] = item
    return items


def parse_item_from_string(line):
    """
    :param line: format: pk - title

    :returns: Item with such pk and title.
    """

    item_re = re.compile('(\w+) - (.+)')
    pk, title = item_re.findall(line)[0]
    return Item(pk, title)


def get_item(path):
    """
    :returns: Item for a given :param path:, path to it.
    :returns: None if such item does not exist.
    """
    items = load_items_dict()
    return items[path]


def add(item_title=None, parent_path=None):
    """Adds a item - step/task/goal.

    Title is obtained from `sys.argv`.
    
    If no `parent_path` is specified item is added to root.

    :param item_title: Title of the item. If `None` it is read from `sys.argv`.
        If it is specified it is probably a test.
    :type item_title: str or None
    :param parent_path: Path to parent, specified as for example as "3/1/2".
        If `None` a check of command line arguments is made.
    :type parent_path: str or None
    """

    _create_dir_if_needed()

    if not item_title:
        from argparse import ArgumentParser
        parser = ArgumentParser()
        parser.add_argument('-t', '--title', dest='item_title', default=None)
        parser.add_argument('-p', '--parent', dest='parent_path', default=None)
        args = parser.parse_args(sys.argv[2:])
        item_title = args.item_title
        if item_title is None:
            sys.stderr.write('Error: no title is specified (use flag -t)\n')
            exit(1)

    with open(FULL_PROGRESS_FILENAME, 'a') as f:
        f.write(item_title + '\n')

    print "Added item:"
    print args.item_title


def count():
    counts = count_items()
    print "done: {}".format(counts['done'])
    print "total items: {}".format(counts['total'])
    print ""
    print "done today: {}".format(counts['done_today'])
    print "done yesterday: {}".format(counts['done_yesterday'])


def done(pk_done=None):
    """
    Mark an item `pk_done` as done.
    If item is not specified as a variable get it from stdin.
    """

    _create_db_if_needed()

    try:
        if pk_done is None:
            if len(sys.argv) > 2:
                pk_done = sys.argv[2]
            else:
                print "Specify item done."
                return
        print "Marking item %s as done." % pk_done
        con = sqlite3.connect(PROGRESS_DB_FILE_NAME)
        cur = con.cursor()
        done_at = time.strftime(DATE_FORMAT)
        query = "UPDATE item SET done_at='{done_at}', is_done='TRUE' WHERE pk={pk_done}".format(
            done_at=done_at, pk_done=pk_done)
        cur.execute(query)
        con.commit()
        con.close()
    except sqlite3.OperationalError, e:
        print "Database error:", e


def delete(pk_delete=None):
    """
    Remove item with `pk_delete` from database.
    """

    try:
        if pk_delete is None:
            if len(sys.argv) > 2:
                pk_delete = sys.argv[2]
            else:
                print "Specify item to delete."
                return
        sys.stdout.write(
            "Do you really want to delete item {}? y/n [n] ".format(pk_delete)
        )
        choice = raw_input().lower().strip()
        if choice == 'y':
            con = sqlite3.connect(PROGRESS_DB_FILE_NAME)
            cur = con.cursor()
            query = "DELETE FROM item WHERE pk='{pk_delete}'".format(
                pk_delete=pk_delete)
            cur.execute(query)
            con.commit()
            con.close()
            print 'Deleted item {}'.format(pk_delete)
    except sqlite3.OperationalError, e:
        print "Database error:", e


def help():
    """
    Prints help.
    """
    print "usage: p [COMMAND [ARGS]]"
    print ""
    print "  add    [-p id] -t TITLE  - add an item with TITLE, flag -p points to parent id"
    print "  count                    - count items done and to be done"
    print "  delete n                 - delete item with id n"
    print "  done   n                 - mark item with id n as done"
    print "  help                     - print help"
    print "  log    [-d]              - log items, flag -d for done"
    print "  move   n -p m            - move item n to parent m"
    print "  version                  - version of the program (-v and --version also work)"


def log():
    """
    log [-d]
    """
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option('-d', dest='print_done', default=False, action='store_true')
    (opts, args) = parser.parse_args(sys.argv[2:])
    print "print done:", opts.print_done
    for i in load_items_list(opts.print_done):
        print str(i)


def move(item_pk=None, new_parent_pk=None):
    """
    Move item with `item_pk` to new parent with `new_parent_pk`.
    """

    if item_pk is None:
        if len(sys.argv) > 2:
            try:
                item_pk = int(sys.argv[2])
            except ValueError:
                print "Incorrect item value"
                exit(1)
        else:
            print "Specify item to move."
            exit(1)
        from optparse import OptionParser
        parser = OptionParser()
        parser.add_option("-p", "--parent", dest="new_parent_pk")
        (opts, args) = parser.parse_args(sys.argv[2:])
        new_parent_pk = getattr(opts, "new_parent_pk")
        if new_parent_pk is None:
            sys.stderr.write('Error: no new parent is specified (use flag -p)\n')
            exit(1)

    items = load_items_list()
    queries = []
    for i in items:
        if item_pk in i.children:
            i.children.remove(item_pk)
            queries.append("UPDATE item SET children='{children}' WHERE pk={old_parent_pk}".format(
                children=i.children_str, old_parent_pk=i.pk
            ))
            break
    print 'new_parent_pk', new_parent_pk
    new_parent_item = get_item(new_parent_pk)
    new_parent_item.children.append(item_pk)
    print 'new_parent_imtem.children_str=', new_parent_item.children_str
    queries.append("UPDATE item SET children='{children}' WHERE pk={new_parent_pk}".format(
        children=new_parent_item.children_str, new_parent_pk=new_parent_pk
    ))
    con = sqlite3.connect(PROGRESS_DB_FILE_NAME)
    cur = con.cursor()
    for q in queries:
        print 'q=', q
        cur.execute(q)
    con.commit()
    con.close()
    return


def show_one_item(item, items_dict={}, tab=''):
    """
    Prints `item` and all its subitems that are in `items_dict`.
    The item is tabulated with `tab` characters.
    """
    print tab + str(item)
    for pk in item.children:
        if pk in items_dict:
            show_one_item(items_dict[pk], items_dict, tab=tab + '    ')


def show_items():
    """
    Shows items in terminal.
    """
    items = load_items_list()
    for i in items:
        i.show()


def version():
    """
    Shows version of the program.
    """
    print 'Progressio {version}'.format(version=__version__)
    print '<{url}>'.format(url=__url__)


def main():
    # check if db exists and create it if confirmed
    if not os.path.exists(PROGRESS_DB_FILE_NAME):
        sys.stdout.write(
            "{0} does not exist. Create? y/n [n] ".format(
                PROGRESS_DB_FILE_NAME))
        choice = raw_input().lower()
        if choice == '' or choice == 'n':
            return
        _create_db_if_needed()
        print "created %s file" % PROGRESS_DB_FILE_NAME

    args = sys.argv
    command = None
    if len(args) > 1:
        command = args[1]

    if command == 'add':
        add()
        return

    if command == 'done':
        done()
        return

    if command == 'delete':
        delete()
        return

    if command == 'count':
        count()
        return

    if command in ['help', '-h', '--help', '-help']:
        help()
        return

    if command == 'log':
        log()
        return

    if command == 'move':
        move()
        return

    if command in ['version', '-v', '--version']:
        version()
        return

    show_items()


if __name__ == "__main__":
    main()
