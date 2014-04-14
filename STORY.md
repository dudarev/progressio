A user may write:

```
    p add -t "title of the step/ticket/task"
```

Information about current items is saved in .progressio - directory where progress is tracked.

When a user enters just `p` all tickets are shown in the following format:

    1 - title
        11 - title 
    2 - title 
    3 - title 
        3-1 - title 
        3-2 - title 
            3-2-1 subsubitem title

Id is an numeric, it encodes the full pass to it from parent. Path changes for different listing of tasks. 
It stays the same until the tasks are shown.

To add a substep to a ticket one makes the following command:

```
    p add -p id -t "title of the subticket for item id, flag -p stands for parent"
```

An item may be moved from one parent to another.
