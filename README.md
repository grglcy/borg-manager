# borg manager
Summarises [borg](https://borgbackup.readthedocs.io/en/stable/#what-is-borgbackup) backups using output from '[borg create](https://borgbackup.readthedocs.io/en/stable/usage/create.html#description)'.

> This project has been superseded by [borg-web](https://github.com/georgelacey/borg-web),
> a client and web server that provides summaries in the form of a website

## Features:
* Parses json output from 'borg create --json'
* Stores repo and archive information in sqlite database
* Logs errors
* Prints summary of repos and recent errors

### Planned:
* Output to Graphs/HTML

## How to use
Pipe the output of 'borg create --json' to the script, for example:

> borg create --json /repo/path::name /important/data/ 2>&1 | python3 ./main.py -l [label]
> 
> <sup>Note: 2>&1 redirects errors to borg-manager for logging</sup>

### Arguments:
* -o / --output -> specify database location
> `-o /home/user/borg/logs`
* -l / --label -> specify label for borg repo
> `-l 'Server backups'`
* -s / --summary -> print summary