# borg manager
Summarises borg backups using output from 'borg create'.

## Features
* Parses json output from 'borg create --json'
* Stores Repo and archive information in sqlite database

### Planned:
* Summary CLI interface
* Output to HTML

## How to use
Pipe the output of 'borg create --json' to the script, e.g.
> borg create --json /repo/path::name /important/data/ | python3 ./main.py