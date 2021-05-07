from borgmanager.database import BorgDatabase
from sys import stdin
from os.path import realpath
from pathlib import Path
import argparse
from borgmanager.borg import OutputHandler
from borgmanager.summary import Summary
from borgmanager.logging import Log, LEVEL_DEBUG
from time import sleep


def main(args, path: Path, log: Log):
    if args.dir is not None:
        output_path = Path(args.dir)
        if not output_path.exists():
            output_path.mkdir()
        path = output_path
    log.debug(f"Path: {path}")
    db = BorgDatabase(path / 'borg.sqlite', log)

    if args.summary:
        log.debug("args.summary")
        summary = Summary(db)
        print(summary.repo_stats())
    else:
        log.debug("reading from stdin")
        borg_output = " ".join(stdin.readlines())
        log.debug(f"stdin output: {borg_output}")
        if args.label is None:
            log.error("No label supplied")
            raise Exception("No label supplied")
        else:
            bo = OutputHandler(borg_output)

            if bo.error:
                log.debug("processing error")
                db.insert_error(bo.get_borg_error(), args.label)
            else:
                log.debug("processing borg json")
                db.insert_record(*bo.get_borg_info(), args.label)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--summary", help="Print summary", action='store_true')
    parser.add_argument("-d", "--dir", help="Database directory", type=str)
    parser.add_argument("-l", "--label", help="Repo Label", type=str)
    return parser.parse_args()


if __name__ == "__main__":
    m_args = get_args()
    m_path = Path(realpath(__file__)).parent.parent
    m_log = Log(LEVEL_DEBUG)
    main(m_args, m_path, m_log)
