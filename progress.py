#!/usr/bin/python
import sys, os
import yaml

def add():
    "add a step/task/goal..."
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-t", "--title", dest="title")
    (opts, args) = parser.parse_args(sys.argv[2:])
    if not getattr(opts,"title"):
        print "specify title with option -t"
        return
    print "title:",opts.title
    items_list = [i for i in yaml.load_all(open('progress.yaml'))]
    # prepend new item in the beginning
    items_list = [{'step':{'title':opts.title}}] + items_list
    stream = open('progress.yaml','w')
    dump_options = {'indent':4,'default_flow_style':False, 'explicit_start':'---'}
    for i in items_list:
        yaml.dump(i,stream,**dump_options)
    stream.close()
    return

def html():
    print "creating html"
    
    fields_list = ['step', 'task', 'issue', 'version', 'goal', 'other']
    fields = {'step': [], 'task': [], 'issue': [], 'version': [], 'goal': [], 'other': []}

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
            done = i.get("done",False)
            if not done and i.has_key('title'):
                file.write("%s: %s<br/>\n" % (f,i['title']))
                for k in i.keys():
                    if not k == 'title':
                        file.write("&nbsp;&nbsp;&nbsp;&nbsp;%s: %s<br/>\n" % (k,i[k]))
        if fields[f]:
            file.write("<br/>")

def main():

    progress_file_name = 'progress.yaml'
    if not os.path.exists(progress_file_name):
        f = open(progress_file_name, 'w')
        f.close()
        print 'created %s file' % progress_file_name
        return

    args = sys.argv
    command = None
    if len(args) > 1:
        command = args[1]
        print command

    if command == 'clean':
        done_list = []
        not_done_list = []
        for i in yaml.load_all(open('progress.yaml')):
            key = i.keys()[0]
            done = i[key].get("done",False)
            if done and i[key].has_key('title'):
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

    if command == "html":
        html()
        return

    if command == "add":
        add()
        return

    for i in yaml.load_all(open('progress.yaml')):
        key = i.keys()[0]
        done = i[key].get("done",False)
        if not done and i[key].has_key('title'):
            print "%s: %s" % (key,i[key]['title'])

if __name__ == "__main__":
    main()
