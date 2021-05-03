from datetime import *
import re


class LogEntry(object):

    def __init__(self, name, fingerprint, start_time, end_time, duration_string,
                 file_count):
        self.name = name
        self.fingerprint = fingerprint
        self.start_time = self.get_datetime(start_time)
        self.end_time = self.get_datetime(end_time)
        self.duration = self.get_duration(duration_string)
        self.file_count = file_count
    
    def print_to_file(self, filename):
        with open(filename, "w") as file:
            file.writelines([f"name: {self.name}",
                             f"fingerprint: {self.fingerprint}",
                             f"start: {self.start_time.date()} time: {self.start_time.time()}",
                             f"end: {self.end_time.date()} time: {self.end_time.time()}",
                             f"duration: {self.duration}",
                             f"file_count: {self.file_count}"])

    def get_duration(self, duration_string):
        total_seconds = 0.0
        time_strings = [('second', 1), ('minute', 60), ('hour', 3600), ('day', 86400)]
        for ts, mult in time_strings:
            total_seconds += self.get_time_unit_string(duration_string, ts, mult)

        return total_seconds

    @staticmethod
    def get_time_unit_string(text: str, time_text: str, multiplier: int = 1):
        substring = re.search(rf"((\d+)\.(\d+)|(\d+))\s({time_text}|{time_text}s)", text)
        if substring is not None:
            substring = substring.group().strip(f" {time_text}s")
            return float(substring) * multiplier
        else:
            return 0

    @staticmethod
    def get_datetime(datetime_string):
        date_string = re.search(r"....-..-..", datetime_string).group()
        time_string = re.search(r"..:..:..", datetime_string).group()

        year = int(date_string[0:4])
        month = int(date_string[5:7])
        day = int(date_string[8:10])

        hour = int(time_string[0:2])
        minute = int(time_string[3:5])
        second = int(time_string[6:8])

        converted_datetime = datetime(year, month, day, hour, minute, second)

        return converted_datetime
