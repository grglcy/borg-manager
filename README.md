# borg manager
Summarises [borg](https://borgbackup.readthedocs.io/en/stable/#what-is-borgbackup) backups using output from '[borg create](https://borgbackup.readthedocs.io/en/stable/usage/create.html#description)'.

## Features:
* Parses json output from 'borg create --json'
* Stores Repo and archive information in sqlite database

### Planned:
* Summary CLI interface
* Output to Graphs/HTML

## How to use
Pipe the output of 'borg create --json' to the script, for example:
> borg create --json /repo/path::name /important/data/ | python3 ./main.py