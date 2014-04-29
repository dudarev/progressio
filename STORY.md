A user may write:

```
    p add -t "title of the step/ticket/task"
```

Information about current items is saved in `.progressio` - directory where progress is tracked.
Items are stored in two files: `progress.txt` and `done.txt`.

When a user enters just `p` all items are shown in the following format:

    1 - title
        1 - title 
    2 - title 
    3 - title 
        1 - subitem title 
        2 - subitem title 
            1 - subsubitem title

The path ids may change for different listing of tasks. It stays the same until the tasks are shown.
In various commands item path ids are specified similar to files paths, for example, "3/2/1". 
The path separator in the path can be any non-numeric character.

To add a substep to a ticket one uses the following command:

```
    p add -p 3/2 -t "title of the subticket for item id, flag -p stands for parent"
```

An item may be moved from one parent to another:

```
    p move 3/2/1 -p 3/1
```

Mark an item as done with:

```
    p done 3/2/1
```
