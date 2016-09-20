from datetime import *
import re


class logEntry(object):

    def __init__(self, name, fingerprint, datetime_string, duration,
                 file_count):
        self.name = name
        self.fingerprint = fingerprint
        self.datetime = self.set_datetime(datetime_string)
        self.duration = duration
        self.file_count = file_count
    
    def print_to_file(self, filename):
        x = open(filename, "w")
        
        x.write("name: %s\n" % self.name)
        x.write("fingerprint: %s\n" % self.fingerprint)
        x.write("date: %s time: %s\n" % \
            (self.datetime.date(), self.datetime.time()))
        x.write("duration: %s\n" % self.duration)
        x.write("file_count: %s\n" % self.file_count)
        
        x.close()


def set_datetime(datetime_string):
    date = re.search(r"....-..-..", datetime_string).group()
    time = re.search(r"..:..:..", datetime_string).group()

    year = int(date[0:4])
    month = int(date[5:7])
    day = int(date[8:10])

    hour = int(time[0:2])
    minute = int(time[3:5])
    second = int(time[6:8])

    converted_datetime = datetime(year, month, day, hour, minute, second)

    return converted_datetime