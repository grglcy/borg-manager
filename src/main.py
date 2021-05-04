from borgmanager.database import BorgDatabase
from sys import stdin
from os.path import realpath
from pathlib import Path
import argparse
from borgoutputhandler import BorgOutputHandler
from borgmanager.summary import Summary


def main(args, path: Path):
    db = BorgDatabase(path / 'borg.sqlite')
    if args.graph is not None:
        pass
    elif args.summary is not None:
        summary = Summary(db, args.summary)
    else:
        borg_output = " ".join(stdin.readlines())
        bo = BorgOutputHandler(borg_output)

        if bo.error:
            db.insert_error(bo.get_borg_error())
        else:
            db.insert_record(*bo.get_borg_info())


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--graph", help="Produce graphs at specified location", type=str)
    parser.add_argument("-s", "--summary", help="Print summary", type=str)
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    path = Path(realpath(__file__)).parent.parent
    main(args, path)
