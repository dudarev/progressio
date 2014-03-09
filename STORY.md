A user may write:

```
    p add -t "title of the step/ticket/task"
```

Information about current items is saved in .progressio - directory where progress is tracked.

When a user enters just `p` all tickets are shown in the following format:

    id - title
        id - title 
    id - title 
    id - title 
        id - title 
        id - title 

Id is an alphanumeric, automatically generated.

To add a substep to a ticket one makes the following command:

```
    p add -p id -t "title of the subticket for item id, flag -p stands for parent"
```

Ids are generated based on time: 
combine creation time into a string "YYYYMMDDHHMMSS",
treat this string as a decimal number,
convert it to base 32,
reverse order of the digits.

An item may be moved from one parent to another.
