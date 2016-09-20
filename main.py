from sys import stdin
from LogEntry import *
from Database import *

raw_borg_output = stdin.readlines()

attributes = {"Archive name: ": "",
              "Archive fingerprint: ": "",
              "Time (start): ": "",
              "Duration: ": "",
              "Number of files: ": ""}
                
for i in range(0, len(raw_borg_output)):
    
    for key in attributes:
        if raw_borg_output[i].startswith(key):
            attributes[key] = raw_borg_output[i] \
                .strip(key) \
                .rstrip()

borg_output = LogEntry(attributes["Archive name: "],
                       attributes["Archive fingerprint: "],
                       attributes["Time (start): "],
                       attributes["Duration: "],
                       attributes["Number of files: "])

borg_output.print_to_file("borg.txt")

database = Database("borg.db")

row_list = ["ID INTEGER PRIMARY KEY",
            "NAME TEXT NOT NULL",
            "FINGERPRINT TEXT NOT NULL",
            "START_TIME DATETIME NOT NULL",
            "DURATION REAL NOT NULL",
            "FILE_COUNT INTEGER NOT NULL"]

database.create_table("log_entries", row_list)

database.insert(borg_output, "log_entries")
