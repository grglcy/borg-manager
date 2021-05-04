from database import BorgDatabase
from sys import stdin
from os.path import realpath
from pathlib import Path
import argparse
from borgoutputhandler import BorgOutputHandler


def main(args, path: Path):
    if args.graph is not None:
        pass
    else:
        borg_output = " ".join(stdin.readlines())
        bo = BorgOutputHandler(borg_output)
        db = BorgDatabase(path / 'borg.sqlite')

        if bo.error:
            db.insert_error(bo.get_borg_error())
        else:
            db.insert_record(*bo.get_borg_info())


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--graph", help="Produce graphs at specified location",
                        type=str)
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    path = Path(realpath(__file__)).parent.parent
    main(args, path)
