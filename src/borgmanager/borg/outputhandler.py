from datetime import datetime
from borgmanager import borg
import json


class OutputHandler(object):
    def __init__(self, borg_output: str):
        self.borg_output = borg_output
        self.borg_json = None

        self.error = False
        try:
            self.borg_json = json.loads(borg_output)
        except json.JSONDecodeError:
            self.error = True

    def get_borg_info(self):
        repo = borg.Repo.from_json(self.borg_json['repository'])
        archive = borg.Archive.from_json(self.borg_json['archive'])
        stats = borg.Stats.from_json(self.borg_json['archive']['stats'])

        return repo, archive, stats

    def get_borg_error(self):
        return borg.Error(self.borg_output, datetime.now())
