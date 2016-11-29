#!/usr/bin/env python
# This is a parser to parse Kippo ssh log attemps and return the data in tab seperated values.

from sys import argv
import re

regex = re.compile(
    r"(2\d\d\d-\d\d-\d\d) (\d\d:\d\d:\d\d)([+-]\d{4}) [^,]+,\d+,([\d.]+)\] login attempt \[([^\/]+)\/([^\]]+)\] (\w*)"
)
with open(argv[1], 'r', encoding="ISO-8859-1") as logfile:
    for line in logfile.readlines():
        match = regex.search(line.rstrip())
        if match is None:
            continue
        else:
            date_log = match.group(1)
            time_log = match.group(2)
            #timezone = match.group(3)
            source_ip = match.group(4)
            username = match.group(5)
            password = match.group(6)
            result = match.group(7)
            print(
                date_log,
                time_log,
                source_ip,
                username,
                password,
                result,
                sep='\t')
