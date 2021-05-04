from sys import stdin
from os.path import realpath
from pathlib import Path
from database import Repo, Archive
import json


def main(input_json: dict, path: Path):
    db_path = path / 'borg.sqlite'

    repo = Repo(db_path, input_json['repository'])
    log_entry = Archive(db_path, repo, input_json['archive'])


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
