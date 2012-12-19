#!/usr/bin/python
"""
Data structure:

Each task/step/ticket is an Item instance.

Each item may have one parent and several children nodes.
"""

import os
import sys
import yaml
import time
import string
import re
import sqlite3


__version__ = '0.2dev'

PROGRESS_TXT_FILE_NAME = 'progress.txt'
PROGRESS_DB_FILE_NAME = 'progress.db'

BASE_FOR_ID = 36


class Item(object):
    """
    The following fields are stored in the database:

    pk (id)     - int
    children    - str - a list of children ids, order is important (limit of 8 items!)
    title       - str - title
    added_at    - datetime
    is_done     - boolean
    done_at     - datetime

    TODO: Think about using materialized path (it is not necessary yet):

    path        - str - materialized path - root, subroot, ..., grandparent, parent

    It should be added if its used would seem to be required.
    """

    def __init__(self, pk, children=None, title=None, added_at=None, is_done=False, done_at=None):
        self.pk = int(pk)
        if children is not None:
            self.children = children.split(',')
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
        return cmp(int(self.pk, BASE_FOR_ID), int(other.pk, BASE_FOR_ID))


def base_encode(num, base, dd=False):
    """
    Converts a number in base 10
    to new base from 2 to 36.
    
    http://www.daniweb.com/forums/thread159163.html
    to convert back  int(string, BASE_FOR_ID)

    :param num:
    :param base:
    :param dd:

    :returns: number in `base`
    """
    if not 2 <= base <= 36:
        raise ValueError('The base number must be between 2 and 36.')
    if not dd:
        dd = dict(zip(range(36), list(string.digits + string.ascii_lowercase)))
    if num < base:
        return dd[num]
    num, rem = divmod(num, base)
    return base_encode(num, base, dd) + dd[rem]


def _create_db_if_needed():
    """
    Checks if db file exists. Creates it if it does not exist.

    :returns: a string with message describing what happened.
    """

    if not os.path.exists(PROGRESS_DB_FILE_NAME):
        con = sqlite3.connect(PROGRESS_DB_FILE_NAME)
        cur = con.cursor()
        cur.execute(
            "CREATE TABLE item(" +
            "pk INTEGER PRIMARY KEY, children, title, added_at, is_done DEFAULT FALSE, done_at)")
        cur.execute("INSERT INTO item(pk, children, title) values(0, '', 'root')")
        con.commit()
        con.close()
        return 'DB file did not exist and was created.'

    return 'DB file exists'


def load_items():
    """
    :returns: a list with Item instances that are NOT done.
    """
    con = sqlite3.connect(PROGRESS_DB_FILE_NAME)
    cur = con.cursor()
    cur.execute("SELECT * FROM item WHERE is_done='FALSE'")
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


# TODO: stopped refactoring here


def load_txt():
    items = []
    if not os.path.exists(PROGRESS_TXT_FILE_NAME):
        return []
    for line in open(PROGRESS_TXT_FILE_NAME, 'r'):
        items.append(parse_item_from_string(line))
    return items


def save_txt(items):
    with open(PROGRESS_TXT_FILE_NAME, 'w') as f:
        for i in items:
            f.write(' {0} - {1}'.format(
                i.pk,
                i.title))
            f.write('\n')


def get_item(pk):
    con = sqlite3.connect(PROGRESS_DB_FILE_NAME)
    cur = con.cursor()
    cur.execute('SELECT * FROM item WHERE pk={}'.format(pk))
    item = Item(*cur.fetchone())
    con.close()
    return item


def add(item_title=None, item_pk=None, parent_pk=0):
    """
    add a step/task/goal...
    
    If no parent_pk is specified item is added to root (pk=0)
    """

    if not item_title:
        from optparse import OptionParser
        parser = OptionParser()
        parser.add_option("-t", "--title", dest="title")
        parser.add_option("-i", "--item", dest="type", default="step")
        (opts, args) = parser.parse_args(sys.argv[2:])
        if not getattr(opts, "title"):
            return
        item_title = opts.title

    _create_db_if_needed()

    parent = get_item(parent_pk)

    con = sqlite3.connect(PROGRESS_DB_FILE_NAME)
    cur = con.cursor()
    query = "INSERT INTO item(title) values('{title}')".format(title=item_title)
    cur.execute(query)
    con.commit()
    parent.children.append(cur.lastrowid)
    children = ','.join(map(str, parent.children))
    query = "UPDATE item SET children='{children}' WHERE pk={parent_pk}".format(
        children=children, parent_pk=parent_pk)
    cur.execute(query)
    con.commit()
    con.close()

    items = load_items()
    save_txt(items)

    """
    try:
        last_id = items['info']['last_id']
    except KeyError:
        last_id = '0'
    new_id = base_encode(int(last_id, BASE_FOR_ID) + 1, BASE_FOR_ID)
    if item_pk:
        items['items'][item_pk]['items'] = {}
        items['items'][item_pk]['items']['0'] = {
            'title': item_title,
            'added_at':  time.strftime('%a %b %d %H:%M:%S %Y %Z'),
            'id': new_id
            }
    else:
        items['items'][new_id] = {
                    'title': item_title,
                    'added_at':  time.strftime('%a %b %d %H:%M:%S %Y %Z'),
                    'id': new_id
                    }
    items['info']['last_id'] = new_id
    save_items(items)


    return
    """


def clean():
    done_list = []
    not_done_list = []
    for i in yaml.load_all(open('progress.yaml')):
        key = i.keys()[0]
        is_done = i[key].get("done", False)
        if is_done and i[key].has_key('title'):
            print "%s: %s" % (key,i[key]['title'])
            done_list.append(i)
        else:
            not_done_list.append(i)
    stream = open('progress.history.yaml','a')
    dump_options = {'indent':4,'default_flow_style':False, 'explicit_start':'---'}
    for i in done_list:
        yaml.dump(i,stream,**dump_options)
    stream.close()
    stream = open('progress.yaml','w')
    dump_options = {'indent':4,'default_flow_style':False, 'explicit_start':'---'}
    for i in not_done_list:
        yaml.dump(i,stream,**dump_options)
    stream.close()
    return

def convert():
    print "converting to new progress.txt format"
    if os.path.exists(PROGRESS_TXT_FILE_NAME):
        print '{} already exists'.format(PROGRESS_TXT_FILE_NAME)
        return
    with open(PROGRESS_TXT_FILE_NAME, 'w') as f:
        for i in load_items():
            key = i.keys()[0]
            is_done = i[key].get("done", False)
            if not is_done and i[key].has_key('title') and i[key].has_key('id'):
                f.write("%s - %s\n" % (i[key]['id'], i[key]['title']))
    return

def count():
    count_done = 0
    count_total = 0
    items = load_items()['items']
    for i in items:
        count_total += 1
        is_done = items[i].get("done", False)
        if is_done:
            count_done += 1
    print "done: ", count_done
    print "total items: ", count_total
    return

def done(pk_done=None):
    """
    Mark an item as done.
    """

    _create_db_if_needed()

    try:
        if pk_done is None:
            pk_done = sys.argv[2]
        print "Marking item %s as done." % pk_done
        con = sqlite3.connect(PROGRESS_DB_FILE_NAME)
        cur = con.cursor()
        done_at = time.strftime('%a %b %d %H:%M:%S %Y %Z')
        query = "UPDATE item SET done_at='{done_at}', is_done='TRUE' WHERE pk={pk_done}".format(
            done_at=done_at, pk_done=pk_done)
        cur.execute(query)
        con.commit()
        con.close()
        items = load_items()
        save_txt(items)
    except sqlite3.OperationalError, e:
        print "Database error:", e
    return


def help():
    """
    Print help.
    """
    print "usage: p [COMMAND [ARGS]]"
    print ""
    print "  add    [-p id] -t TITLE  - add an item with TITLE, flag -p points to parent id"
    print "  count                    - count items done and to be done"
    print "  done   n                 - mark item with id n as done"
    print "  help                     - print help"
    print "  log    [-d]              - log items, flag -d for done"


def html():
    print "creating html"
    
    fields_list = ['step', 'issue', 'task', 'version', 'goal', 'other']
    fields = {'step': [], 'issue': [], 'task': [], 'version': [], 'goal': [], 'other': []}
    ignore_keys = ('added_at', 'title')

    # add to fields
    for i in yaml.load_all(open('progress.yaml')):
        key = i.keys()[0]
        if key in fields:
            fields[key].append(i[key])
        else:
            fields['other'].append(i[key])

    file = open("progress.html", "w")
    file.write("""<style> body { padding: 1em; } </style>""")
    for f in fields_list:
        file.write("""<h2>%ss</h2>""" % f)
        for i in fields[f]:
            is_done = i.get("done",False)
            if not is_done and i.has_key('title'):
                file.write("%s<br/>\n" % i['title'])
                for k in i.keys():
                    if not k in ignore_keys:
                        file.write("&nbsp;&nbsp;&nbsp;&nbsp;%s: %s<br/>\n" % (k,i[k]))
        if fields[f]:
            file.write("<br/>")


def log():
    "log [-i item_type] [-d]"
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-i", "--item", dest="type", default="all")
    parser.add_option('-d', dest='print_done', default=False, action='store_true')
    (opts, args) = parser.parse_args(sys.argv[2:])
    print "item type:", opts.type
    print "print done:", opts.print_done
    item_count = 1
    for i in load_items():
        key = i.keys()[0]
        is_done = i[key].get("done",False)
        if is_done==opts.print_done and i[key].has_key('title'):
            if opts.type=="all" or opts.type==key:
                print "%2d - %s: %s" % (item_count, key, i[key]['title'])
                item_count += 1
    load_txt()


def main():
    progress_file_name = 'progress.yaml'
    if not os.path.exists(progress_file_name):
        sys.stdout.write("progress.yaml does not exist. Create? y/n [n] ")
        choice = raw_input().lower()
        if choice == '' or choice == 'n':
            return
        f = open(progress_file_name, 'w')
        f.close()
        print 'created %s file' % progress_file_name
        return

    args = sys.argv
    command = None
    if len(args) > 1:
        command = args[1]

    if command == 'clean':
        clean()
        return

    if command == "html":
        html()
        return

    if command == "add":
        add()
        return

    if command == "done":
        done()
        return

    if command == "count":
        count()
        return

    if command == "convert":
        convert()
        return

    if command in ["help", "-h", "--help", "-help"]:
        help()
        return

    if command == "log":
        log()
        return

    _create_db_if_needed()

    items = load_items()
    for i in items:
        print i

if __name__ == "__main__":
    main()
