#!/usr/bin/python
import sys, os
import yaml
import time

def load_items():
    return [i for i in yaml.load_all(open('progress.yaml'))]

def save_items(items):
    stream = open('progress.yaml','w')
    dump_options = {'indent':4,'default_flow_style':False, 'explicit_start':'---'}
    for i in items:
        yaml.dump(i,stream,**dump_options)
    stream.close()

def add():
    "add a step/task/goal..."
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-t", "--title", dest="title")
    parser.add_option("-i", "--item", dest="type")
    (opts, args) = parser.parse_args(sys.argv[2:])
    if not getattr(opts,"title"):
        print "specify title with option -t"
        return
    print "title:", opts.title
    print "item type:", opts.type
    items_list = load_items()
    # prepend new item in the beginning
    if not opts.type:
        opts.type = 'step'
    items_list = [{
                opts.type: {
                    'title': opts.title,
                    'added_at':  time.strftime('%a %b %d %H:%M:%S %Y %Z')
                }
            }] + items_list
    save_items(items_list)
    return

def clean():
    done_list = []
    not_done_list = []
    for i in yaml.load_all(open('progress.yaml')):
        key = i.keys()[0]
        is_done = i[key].get("done",False)
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

def count():
    count_done = 0
    count_total = 0
    for i in yaml.load_all(open('progress.yaml')):
        count_total += 1
        key = i.keys()[0]
        is_done = i[key].get("done",False)
        if is_done:
            count_done += 1
    print "done: ",count_done
    print "total items: ",count_total
    return

def done():
    "mark an item done"
    try:
        print "will mark item %d done" % int(sys.argv[2])
        count_done = int(sys.argv[2])
        count = 1
        items = load_items()
        for i in items:
            key = i.keys()[0]
            is_done = i[key].get("done",False)
            if not is_done and i[key].has_key('title'):
                if count == count_done:
                    print "%2d - %s: %s" % (count, key, i[key]['title'])
                    i[key]['done'] = True
                    i[key]['done_at'] = time.strftime('%a %b %d %H:%M:%S %Y %Z')
                    save_items(items)
                    return
                count += 1
    except IndexError:
        print "you need to specify an item number"
    except ValueError:
        print "you need to specify an item number as integer"
    return

def help():
    "print help"
    print "usage: p [COMMAND [ARGS]]"
    print ""
    print "  add    [-i [(step,task,issue)]] -t TITLE"
    print "  clean  clean progress.yaml, move done items to progress.yaml.history"
    print "  count  count items done and to be done"
    print "  done   [n] - mark item n done"
    print "  help   print help"
    print "  html   generate progress.html"
    return

def html():
    print "creating html"
    
    fields_list = ['step', 'issue', 'task', 'version', 'goal', 'other']
    fields = {'step': [], 'issue': [], 'task': [], 'version': [], 'goal': [], 'other': []}

    # add to fields
    for i in yaml.load_all(open('progress.yaml')):
        key = i.keys()[0]
        if key in fields:
            fields[key].append(i[key])
        else:
            fields['other'].append(i[key])

    file = open("progress.html", "w")
    for f in fields_list:
        for i in fields[f]:
            is_done = i.get("done",False)
            if not is_done and i.has_key('title'):
                file.write("%s: %s<br/>\n" % (f,i['title']))
                for k in i.keys():
                    if not k == 'title':
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

    if command in ["help", "-h", "--help", "-help"]:
        help()
        return

    if command == "log":
        log()
        return

    item_count = 1
    for i in load_items():
        key = i.keys()[0]
        is_done = i[key].get("done",False)
        if not is_done and i[key].has_key('title'):
            print "%2d - %s: %s" % (item_count, key, i[key]['title'])
            item_count += 1

if __name__ == "__main__":
    main()
