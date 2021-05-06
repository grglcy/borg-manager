from datetime import datetime
from borgmanager.database.object import Repo, Archive, Error, Cache
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
        repo = Repo.from_json(self.borg_json['repository'])
        archive = Archive.from_json(self.borg_json['archive'])
        cache = Cache.from_json(self.borg_json['cache']['stats'])

        return repo, archive, cache

    def get_borg_error(self):
        return Error(self.borg_output, datetime.utcnow())
