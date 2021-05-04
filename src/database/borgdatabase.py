from .connection import RepoConn, ArchiveConn, StatsConn, ErrorConn
from pathlib import Path
from src import borg
import json


class BorgDatabase(object):
    def __init__(self, db_path: Path):
        self.repo_name = "repo"
        self.archive_name = "archive"
        self.stats_name = "stats"
        self.error_name = "error"

        self.repo_conn = RepoConn(db_path, table_name=self.repo_name)
        self.archive_conn = ArchiveConn(db_path, self.repo_name,
                                        table_name=self.archive_name)
        self.stats_conn = StatsConn(db_path, self.repo_name, self.archive_name,
                                    table_name=self.stats_name)
        self.error_conn = ErrorConn(db_path,
                                    table_name=self.error_name)

    def process_borg_output(self, borg_output: str):
        borg_json = None
        try:
            borg_json = json.loads(borg_output)
        except json.JSONDecodeError:
            self.handle_borg_error(borg_output)
        self.process_borg_json(borg_json)

    def process_borg_json(self, borg_json: dict):
        repo = borg.Repo.from_json(borg_json['repository'])
        archive = borg.Archive.from_json(borg_json['archive'])
        stats = borg.Stats.from_json(borg_json['archive']['stats'])

        repo_id = self.repo_conn.insert(repo)
        archive_id = self.archive_conn.insert(archive, repo_id)
        self.stats_conn.insert(stats, repo_id, archive_id)

    def handle_borg_error(self, borg_error: str):
        pass
