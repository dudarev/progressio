#!/usr/bin/python
import sys, os
import yaml

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

    for i in yaml.load_all(open('progress.yaml')):
        key = i.keys()[0]
        done = i[key].get("done",False)
        if not done and i[key].has_key('title'):
            print "%s: %s" % (key,i[key]['title'])

if __name__ == "__main__":
    main()
