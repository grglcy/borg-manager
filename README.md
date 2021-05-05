# borg manager
Summarises [borg](https://borgbackup.readthedocs.io/en/stable/#what-is-borgbackup) backups using output from '[borg create](https://borgbackup.readthedocs.io/en/stable/usage/create.html#description)'.

## Features:
* Parses json output from 'borg create --json'
* Stores Repo and archive information in sqlite database
* Print summary of repos

### Planned:
* Output to Graphs/HTML

## How to use
Pipe the output of 'borg create --json' to the script, for example:
> borg create --json /repo/path::name /important/data/ | python3 ./main.py -l [label]

### Arguments:
* -o / --output -> specify database location
> -o /home/user/borg/logs
* -l / --label -> specify label for borg repo
> -l "Server backups"
* -s / --summary -> print summary