from database import BorgDatabase
from sys import stdin
from os.path import realpath
from pathlib import Path


def main(borg_output: str, path: Path):
    db_path = path / 'borg.sqlite'
    db = BorgDatabase(db_path)

    db.process_borg_output(borg_output)


if __name__ == "__main__":
    path = Path(realpath(__file__)).parent.parent
    borg_output = "\n".join(stdin.readlines())
    main(borg_output, path)
