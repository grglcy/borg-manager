from sys import stdin
from src.logentry import LogEntry
from src.database import Database


def main(input_lines: list):
    raw_borg_output = input_lines

    borg_log_entry = create_log_entry(raw_borg_output)
    borg_log_entry.print_to_file("borg.txt")

    database = Database("borg.db")
    database.insert(borg_log_entry)


def create_log_entry(raw_borg_output: list):
    attributes = {"Archive name: ": "",
                  "Archive fingerprint: ": "",
                  "Time (start): ": "",
                  "Time (end): ": "",
                  "Duration: ": "",
                  "Number of files: ": ""}

    for line in raw_borg_output:
        for key in attributes:
            if line.startswith(key):
                attributes[key] = line[len(key):].strip()

    return LogEntry(attributes["Archive name: "],
                    attributes["Archive fingerprint: "],
                    attributes["Time (start): "],
                    attributes["Time (end): "],
                    attributes["Duration: "],
                    attributes["Number of files: "])


if __name__ == "__main__":
    input_text = stdin.readlines()
    main(input_text)
