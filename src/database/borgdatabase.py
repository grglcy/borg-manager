from .connection import RepoConn, ArchiveConn, StatsConn, ErrorConn
from pathlib import Path


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

    # region INSERT

    def insert_record(self, repo, archive, stats):
        repo_id = self.repo_conn.insert(repo)
        archive_id = self.archive_conn.insert(archive, repo_id)
        self.stats_conn.insert(stats, repo_id, archive_id)

    def insert_error(self, borg_error):
        self.error_conn.insert(borg_error)

    # endregion

    # region GET

    def get_repos(self):
        return self.repo_conn.get_all()

    # endregion
