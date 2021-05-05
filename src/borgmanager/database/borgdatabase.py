from .connection import RepoConn, ArchiveConn, StatsConn, ErrorConn, LabelConn
from borgmanager.borg.label import Label
from pathlib import Path


class BorgDatabase(object):
    def __init__(self, db_path: Path):
        self.repo_name = "repo"
        self.archive_name = "archive"
        self.stats_name = "stats"
        self.error_name = "error"
        self.label_name = "label"

        self.repo_conn = RepoConn(db_path, table_name=self.repo_name)
        self.archive_conn = ArchiveConn(db_path, self.repo_name,
                                        table_name=self.archive_name)
        self.stats_conn = StatsConn(db_path, self.repo_name, self.archive_name,
                                    table_name=self.stats_name)
        self.error_conn = ErrorConn(db_path,
                                    label_table=self.label_name,
                                    table_name=self.error_name)
        self.label_conn = LabelConn(db_path,
                                    repo_table=self.repo_name,
                                    table_name=self.label_name)

    # region INSERT

    def insert_record(self, repo, archive, stats, label):
        repo_id = self.repo_conn.insert(repo)
        label_id = self.insert_label(label, repo_id=repo_id)
        archive_id = self.archive_conn.insert(archive, repo_id=repo_id)
        self.stats_conn.insert(stats, repo_id=repo_id, archive_id=archive_id)

    def insert_error(self, borg_error, label):
        label_id = self.insert_label(label)
        self.error_conn.insert(borg_error, label_id=label_id)

    def insert_label(self, label, repo_id=None):
        return self.label_conn.insert(Label(label), repo_id=repo_id)

    # endregion

    # region GET

    def get_repos(self):
        return self.repo_conn.get_all()

    def get_repo_stats(self, repo):
        return self.stats_conn.get_latest_stats(repo)

    # endregion
