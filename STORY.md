A user may write:

```
    p add -t "title of the step/ticket/task"
```

Information about current items is saved in progress.db - sqlite database.

When a user enters just `p` all tickets are shown in the following format:

    id - title
        id - title 
    id - title 
    id - title 
        id - title 
        id - title 

Id is an integer, automatically generated.

To add a substep to a ticket one makes the following command:

```
    p add -p id -t "title of the subticket for item id, flag -p stands for parent"
```

Ids are generated based on global increment, for subitems they do not start with 1.

An item may be moved from one parent to another.
