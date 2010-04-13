#!/usr/bin/python
import yaml
import sys

def main():

    args = sys.argv
    command = None
    if len(args) > 1:
        command = args[1]
        print command

    for i in yaml.load_all(open('progress.yaml')):
        key = i.keys()[0]
        done = i[key].get("done",False)
        if not done and i[key].has_key('title'):
            print "%s: %s" % (key,i[key]['title'])

if __name__ == "__main__":
    main()
