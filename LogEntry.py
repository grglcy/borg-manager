from datetime import *
import re


class LogEntry(object):

    def __init__(self, name, fingerprint, datetime_string, duration_string,
                 file_count):
        self.name = name
        self.fingerprint = fingerprint
        self.datetime = get_datetime(datetime_string)
        self.duration = get_duration(duration_string)
        self.file_count = file_count
    
    def print_to_file(self, filename):
        x = open(filename, "w")
        
        x.write("name: %s\n" % self.name)
        x.write("fingerprint: %s\n" % self.fingerprint)
        x.write("date: %s time: %s\n" %
                (self.datetime.date(), self.datetime.time()))
        x.write("duration: %s\n" % self.duration)
        x.write("file_count: %s\n" % self.file_count)
        
        x.close()

    def datetime_string(self):
        x = self.datetime
        return "%04d-%02d-%02d %02d:%02d:%02d" % (x.year, x.month, x.day,
                                      x.hour, x.minute, x.second)


def get_duration(duration_string):
    total_seconds = 0.0

    seconds = re.search(r"((\d+)\.(\d+)|(\d+))\s(second|seconds)",
                        duration_string)
    minutes = re.search(r"((\d+)\.(\d+)|(\d+))\s(minute|minutes)",
                        duration_string)
    hours = re.search(r"((\d+)\.(\d+)|(\d+))\s(hour|hours)",
                      duration_string)

    if seconds is not None:
        seconds = seconds.group().strip(" seconds")
        seconds = float(seconds)
        total_seconds += seconds
    if minutes is not None:
        minutes = minutes.group().strip(" minutes")
        minutes = float(minutes)
        total_seconds += minutes * 60
    if hours is not None:
        hours = hours.group().strip(" hours")
        hours = float(hours)
        total_seconds += hours * 3600

    return total_seconds


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
