from borgmanager.database import BorgDatabase
from sys import stdin
from os.path import realpath
from pathlib import Path
import argparse
from borgmanager.borg import OutputHandler
from borgmanager.summary import Summary


def main(args, path: Path):
    if args.dir is not None:
        output_path = Path(args.dir)
        if not output_path.exists():
            output_path.mkdir()
        path = output_path
    db = BorgDatabase(path / 'borg.sqlite')

    if args.graph is not None:
        pass
    elif args.summary is not None:
        summary = Summary(db, args.summary)
    else:
        borg_output = " ".join(stdin.readlines())
        if args.label is None:
            raise Exception("No label supplied")
        else:
            bo = OutputHandler(borg_output)

            if bo.error:
                db.insert_error(bo.get_borg_error(), args.label)
            else:
                db.insert_record(*bo.get_borg_info(), args.label)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--summary", help="Print summary", type=str)
    parser.add_argument("-d", "--dir", help="Database directory", type=str)
    parser.add_argument("-l", "--label", help="Repo Label", type=str)
    return parser.parse_args()


if __name__ == "__main__":
    m_args = get_args()
    m_path = Path(realpath(__file__)).parent.parent
    main(m_args, m_path)
