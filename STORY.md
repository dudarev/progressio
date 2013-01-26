A user may write:

```
    p add -t "title of the step/ticket/task"
```

All tickets are collected in progress.txt.

Information about them is saved in progress.db - sqlite database.

When a user enters just `p` all tickets are shown in the following format:

    id - title
        id - title 
    id - title 
    id - title 
        id - title 
        id - title 

Id is an integer, automatically generated.

To add a substep to a ticket one make the following command:

```
    p add -p id -t "title of the subticket for item id, flag -p stands for parent"
```

Ids are generated based on global increment, for subitems they do not start with 1.