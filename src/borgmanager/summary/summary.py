from borgmanager.database.object import Repo, Cache
from math import floor, pow, log


class Summary(object):
    def __init__(self, db, args):
        self.db = db

        if args == "repo":
            print(self.print_repo_stats())

    def print_repo_stats(self):
        repo_sql = self.db.get_repos()

        return_string = ""
        for line in repo_sql:
            repo = Repo.from_sql(line)
            cache = Cache.from_sql(self.db.get_cache(repo))
            return_string += f"repo: {repo.location}\n"
            return_string += f"last backup: {self.seconds_to_string(repo.seconds_since(), 'day', True)} ago\n"
            return_string += f"size: {self.bytes_to_string(cache.unique_csize)}\n"
            return_string += "\n"
        return return_string.strip()

    @staticmethod
    def seconds_to_string(seconds: int, detail='hour', short=False):
        seconds = int(seconds)
        increments = [('year', 31557600),
                      ('week', 604800),
                      ('day', 86400),
                      ('hour', 3600),
                      ('minute', 60),
                      ('second', 1)]
        if short:
            increments = [('yr', 31557600),
                          ('wk', 604800),
                          ('day', 86400),
                          ('hr', 3600),
                          ('min', 60),
                          ('sec', 1)]

        time_string = ""

        remainder = seconds
        for st, s in increments:
            if remainder == 0:
                break
            if remainder < s or remainder == 0:
                continue
            else:
                exact = remainder // s
                remainder = remainder % s
                if exact > 1:
                    time_string += f"{exact} {st}s, "
                else:
                    time_string += f"{exact} {st}, "
                if st == detail:
                    break
        return time_string.strip().strip(',')[::-1].replace(' ,', ' dna ', 1)[::-1]

    @staticmethod
    def bytes_to_string(bytes: int):
        suffixes = ("B", "KB", "MB", "GB", "TB", "PB")
        if bytes == 0:
            return f"0{suffixes[0]}"
        else:
            index = int(floor(log(bytes, 1024)))
            s = round(bytes / pow(1024, index), 2)
            return "%s %s" % (s, suffixes[index])
