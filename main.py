from sys import stdin
from LogEntry import *

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
