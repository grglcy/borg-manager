from .connection import RepoConn, ArchiveConn, ErrorConn, LabelConn, CacheConn
from .object.label import Label
from pathlib import Path


class BorgDatabase(object):
    def __init__(self, db_path: Path, log):
        self.log = log
        self.repo_name = "repo"
        self.archive_name = "archive"
        self.cache_name = "cache"
        self.error_name = "error"
        self.label_name = "label"

        self.repo_conn = RepoConn(db_path, table_name=self.repo_name)
        self.archive_conn = ArchiveConn(db_path, repo_table=self.repo_name,
                                        table_name=self.archive_name)
        self.error_conn = ErrorConn(db_path,
                                    label_table=self.label_name,
                                    table_name=self.error_name)
        self.label_conn = LabelConn(db_path,
                                    repo_table=self.repo_name,
                                    table_name=self.label_name)
        self.cache_conn = CacheConn(db_path,
                                    archive_table=self.archive_name,
                                    table_name=self.cache_name)

    # region INSERT

    def insert_record(self, repo, archive, cache, label):
        self.log.debug("Inserting record")
        repo_id = self.repo_conn.insert(repo)
        self.insert_label(label, repo_id=repo_id)
        archive_id = self.archive_conn.insert(archive, repo_id=repo_id)
        self.cache_conn.insert(cache, archive_id=archive_id)

    def insert_error(self, borg_error, label):
        self.log.debug("Inserting error")
        label_id = self.insert_label(label)
        self.error_conn.insert(borg_error, label_id=label_id)

    def insert_label(self, label, repo_id=None):
        self.log.debug("Inserting label")
        return self.label_conn.insert(Label(label), repo_id=repo_id)

    # endregion

    # region GET

    def get_repo_name(self, repo):
        return self.label_conn.get_repo_name(repo.primary_key)

    def get_cache(self, repo):
        archive = self.archive_conn.get_latest(repo.primary_key)
        return self.cache_conn.get(archive.primary_key)

    def get_repo_errors(self, repo_id):
        label = self.label_conn.get_label_id(repo_id)
        return self.error_conn.get_repo_errors(label)

    def get_recent_repo_errors(self, repo_id, days=7):
        label = self.label_conn.get_label_id(repo_id)
        return self.error_conn.get_recent_repo_errors(label, days)

    # endregion
