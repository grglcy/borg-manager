from borgmanager.database.object import Repo, Archive, Cache
from math import floor, pow, log
from datetime import datetime, timedelta


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
            latest_archive = Archive.from_sql(self.db.get_latest_archive(repo))
            cache = Cache.from_sql(self.db.get_cache(repo))
            repo_name = self.db.get_repo_name(repo)
            if repo_name is not None:
                return_string += f"{repo_name} ({repo.location}):\n"
            else:
                return_string += f"{repo.location}:\n"
            return_string += f"\t> Last backup: {self.seconds_to_string(latest_archive.seconds_since(), 'day', True)}" \
                             f" ago\n"
            return_string += f"\t> Un/Compressed size: {self.bytes_to_string(cache.unique_size)}" \
                             f"/{self.bytes_to_string(cache.unique_csize)}\n"
            return_string += f"\t> {self.get_backup_line(repo.primary_key)}\n"
            return_string += "\n"
        return return_string.strip()

    def get_backup_line(self, repo_id):
        units = []
        units.append(['H' if h else '_' for h in self.get_archive_hours(repo_id, 24)])
        units.append(['D' if d else '_' for d in self.get_archive_days(repo_id, 7)])
        units.append(['W' if w else '_' for w in self.get_archive_units(repo_id, 5, 7)])
        units.append(['M' if m else '_' for m in self.get_archive_units(repo_id, 12, 30)])

        return f"[{']['.join([''.join(u) for u in units])}]"

    def get_archive_hours(self, repo_id, n=12):
        hours = []
        for hours_ago in range(n):
            exists = self.db.archive_conn.archive_on_hour(repo_id, datetime.today() - timedelta(hours=hours_ago))
            hours.append(exists)
        return hours

    def get_archive_days(self, repo_id, n=7):
        days = []
        for days_ago in range(n):
            exists = self.db.archive_conn.archive_on_date(repo_id, datetime.today() - timedelta(days=days_ago))
            days.append(exists)
        return days

    def get_archive_units(self, repo_id, n: int, dmult: int):
        weeks = []
        for weeks_ago in range(0, n):
            last_day = datetime.today() - timedelta(days=weeks_ago * dmult)
            first_day = datetime.today() - timedelta(days=(weeks_ago * dmult) + dmult - 1)
            exists = self.db.archive_conn.between_dates(repo_id, first_day, last_day)
            weeks.append(exists)
        return weeks

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
        suffixes = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB", "HB")
        if bytes == 0:
            return f"0{suffixes[0]}"
        else:
            index = int(floor(log(bytes, 1024)))
            s = round(bytes / pow(1024, index), 2)
            return f"{s}{suffixes[index]}"
