A file-based project management and bug-tracking tool.

Version: 0.3.0-dev


## Installation

```
pip install progressio
```


## Usage

```bash
p [COMMAND [ARGS]]
```

    typing just 'p' will output all items to do
    
    add     [-p id] -t TITLE  - add an item with TITLE, flag -p points to parent id
    count                     - count items done and to be done
    done    [n]               - mark item with id n as done
    help                      - print help
    log     [-d]              - log items, flag -d for done
    version                   - version of the program (-v and --version also work)


## Inspirations

"A journey of a thousand miles begins with a single step." 
-- Confucius 

A research published in Harvard Bussiness Review found that "making progress in one's work" is the biggest motivator.
http://www.youtube.com/watch?v=9j2aTwNor5k&nofeather=True#t=34m44s

http://ginatrapani.github.com/todo.txt-cli/
http://code.google.com/p/todotxt/


## Development

Development is done in `dev` branch. To install code under development:

```
git clone https://github.com/dudarev/progressio.git
cd progressio
git checkout dev
pip uninstall progressio
pip install .
```
