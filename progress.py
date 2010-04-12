#!/usr/bin/python
import yaml

for i in yaml.load_all(open('progress.yaml')):
    key = i.keys()[0]
    done = i[key].get("done",False)
    if not done and i[key].has_key('title'):
        print "%s: %s" % (key,i[key]['title'])
