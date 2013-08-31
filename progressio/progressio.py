#!/usr/bin/python
"""
Data structure:

Each task/step/ticket is an Item instance.

Each item may have one parent and several children nodes.
"""

import os
import sys
import time
import re
import sqlite3
from datetime import datetime


DATE_FORMAT = '%a %b %d %H:%M:%S %Y %Z'


__version__ = '0.3.0'
__author__ = "Artem Dudarev"
__url__ = 'https://github.com/dudarev/progressio'

PROGRESS_DB_FILE_NAME = 'progress.db'


class Item(object):
    """
    The following fields are stored in the database:

    pk (id)     - int
    children    - str - a list of children ids, order is important
    title       - str - title
    added_at    - datetime
    is_done     - boolean
    done_at     - datetime
    """

    def __init__(self, pk, children=None, title=None, added_at=None, is_done=False, done_at=None):
        self.pk = int(pk)
        if children is not None:
            self.children = map(int, filter(None, children.split(',')))
        else:
            self.children = []
        self.title = title
        self.added_at = added_at
        self.is_done = is_done
        self.done_at = done_at

    def __str__(self):
        return self.__unicode__()

    def __repr__(self):
        return self.__unicode__()

    def __unicode__(self):
        return '{} - {}'.format(self.pk, self.title)

    def __cmp__(self, other):
        return cmp(int(self.pk), int(other.pk))

    @property
    def children_str(self):
        return ','.join(set(map(str, self.children)))


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
    done_items = load_items(is_done=True)
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


def load_items(is_done=False):
    """
    :returns: a list with Item instances that are NOT done.
    """
    con = sqlite3.connect(PROGRESS_DB_FILE_NAME)
    cur = con.cursor()
    if is_done:
        query = "SELECT * FROM item WHERE is_done='TRUE'"
    else:
        query = "SELECT * FROM item WHERE is_done='FALSE'"
    cur.execute(query)
    items = cur.fetchall()
    item_instances = [Item(*i) for i in items]
    con.close()
    return item_instances


def parse_item_from_string(line):
    """
    :param line: format: pk - title

    :returns: Item with such pk and title.
    """

    item_re = re.compile('(\w+) - (.+)')
    pk, title = item_re.findall(line)[0]
    return Item(pk, title)


def get_item(pk):
    """
    :returns: Item for a given :param pk:, primary key.
    :returns: None if such item does not exist.
    """
    con = sqlite3.connect(PROGRESS_DB_FILE_NAME)
    cur = con.cursor()
    cur.execute('SELECT * FROM item WHERE pk={}'.format(pk))
    item_data = cur.fetchone()
    if item_data is None:
        return None
    item = Item(*item_data)
    con.close()
    return item


def active(pk_active=None):
    """
    Mark an item `pk_active` as active.
    If item is not specified as a variable get it from stdin.
    """

    _create_db_if_needed()

    try:
        if pk_active is None:
            if len(sys.argv) > 2:
                pk_active = sys.argv[2]
            else:
                print "Specify item to make active."
                return
        con = sqlite3.connect(PROGRESS_DB_FILE_NAME)
        cur = con.cursor()
        query = "UPDATE item SET is_done='FALSE' WHERE pk={pk_active}".format(
            pk_active=pk_active)
        cur.execute(query)
        con.commit()
        con.close()
        print "Item {} is marked as active.".format(pk_active)
    except sqlite3.OperationalError, e:
        print "Database error:", e


def add(item_title=None, parent_pk=0):
    """
    Adds a item - step/task/goal...

    Title is obtained from sys.argv.
    
    If no parent_pk is specified item is added to root (pk=0).
    """

    if not item_title:
        from optparse import OptionParser
        parser = OptionParser()
        parser.add_option("-t", "--title", dest="title")
        parser.add_option("-p", "--parent", dest="parent_pk")
        (opts, args) = parser.parse_args(sys.argv[2:])
        if not getattr(opts, "title"):
            sys.stderr.write('Error: no title is specified (use flag -t)\n')
            exit(1)
        item_title = opts.title
        if opts.parent_pk:
            parent_pk = opts.parent_pk

    # save new item and update its parent in database

    _create_db_if_needed()

    parent = get_item(parent_pk)

    con = sqlite3.connect(PROGRESS_DB_FILE_NAME)
    cur = con.cursor()
    added_at = time.strftime(DATE_FORMAT)
    query = "INSERT INTO item(title, added_at) values('{title}', '{added_at}')".format(
        title=item_title,
        added_at=added_at)
    cur.execute(query)
    con.commit()
    pk = cur.lastrowid
    parent.children.append(pk)
    children = ','.join(map(str, parent.children))
    query = "UPDATE item SET children='{children}' WHERE pk={parent_pk}".format(
        children=children, parent_pk=parent_pk)
    cur.execute(query)
    con.commit()
    con.close()

    print "Added item:"
    item = get_item(pk)
    print item


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
    for i in load_items(opts.print_done):
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

    items = load_items()
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
    items = load_items()
    # select ids that are not first level
    not_first_level = set()
    items_dict = {}
    for i in items:
        not_first_level = not_first_level.union(set(i.children))
        items_dict[i.pk] = i
    for i in items:
        if not i.pk in not_first_level:
            show_one_item(i, items_dict)


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

    if command == 'active':
        active()
        return

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
