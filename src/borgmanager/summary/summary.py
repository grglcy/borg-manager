from borgmanager.borg import Repo


class Summary(object):
    def __init__(self, db, args):
        self.db = db

        if args == "repo":
            print(self.print_repos())

    def print_repos(self):
        repo_sql = self.db.get_repos()
        repos = []
        for line in repo_sql:
            repos.append(Repo.from_sql(line))
        pass
