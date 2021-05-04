from sys import stdin
from os.path import realpath
from pathlib import Path
from database import RepoConn, ArchiveConn, StatsConn
import json
import borg


def main(input_json: dict, path: Path):
    db_path = path / 'borg.sqlite'

    repo = borg.Repo.from_json(input_json['repository'])
    barchive = borg.Archive.from_json(input_json['archive'])
    stats = borg.Stats.from_json(input_json['archive']['stats'])

    repo_conn = RepoConn(db_path)
    archive_conn = ArchiveConn(db_path)
    stats_conn = StatsConn(db_path)

    repo_id = repo_conn.insert(repo)
    archive_id = archive_conn.insert(barchive, repo_id)
    stat_id = stats_conn.insert(stats, repo_id, archive_id)


if __name__ == "__main__":
    path = Path(realpath(__file__)).parent.parent
    input_text = stdin.readlines()

    try:
        input_json = json.loads(" ".join(input_text))
    except:
        # todo: output input_text somewhere
        print("Error parsing json, output:")
        print("\n".join(input_text))
        exit(1)
    main(input_json, path)
