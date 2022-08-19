#!/usr/bin/env python3

# Script to analyze PHP/JS code
# Searches for possible PHP/JS type juggling

import argparse
from colorama import Fore, Style
import re
import requests

# For parsing CLI args
parser = argparse.ArgumentParser()
location = parser.add_mutually_exclusive_group(required=True)

# Regex for detecting Type Juggling
collision_regex = re.compile("(.*)[!<>=]=(.*)")
avoid_regex = re.compile("(.*)[!<>=]==(.*)")

# Keep track of line number/if issues were found
line_number = 0
found_issues = False


# Regex matching
def check_for_collision(line):
    collides = bool(re.match(collision_regex, line.strip()))
    false_positive = bool(re.match(avoid_regex, line.strip()))
    return collides and not false_positive


# Yay! Pretty Colors!
def pretty_print(line):
    print(f"{Fore.GREEN}[Line {line_number}]{Style.RESET_ALL} "
          f"{Fore.RED}{line.strip()}{Style.RESET_ALL}")


# Iterate over the lines of a local file
def analyze_local_file(file):
    global line_number, found_issues
    with open(file, "r") as handle:
        while True:
            line = handle.readline()
            if line:
                line_number += 1
                if check_for_collision(line):
                    found_issues = True
                    pretty_print(line)
            else:
                break
        if not found_issues:
            print("[-] No type juggling issues found...")


# Iterate over the lines of a GET request
def analyze_remote_code(req):
    global line_number, found_issues
    for line in req.iter_lines():
        line_number += 1
        if check_for_collision(line.decode()):
            found_issues = True
            pretty_print(line.decode())
    if not found_issues:
        print("[-] No type juggling issues found...")


def main():
    # Get Arguments
    parser.add_argument(
        "--file",
        "-f",
        type=str,
        required=True,
        help="Local/Remote File to Scan"
    )
    location.add_argument(
        "--local",
        "-l",
        action="store_true",
        help="Scan Local File"
    )
    location.add_argument(
        "--remote",
        "-r",
        action="store_true",
        help="Scan Remote File"
    )
    args = parser.parse_args()

    # Parse depending on args
    if args.local:
        analyze_local_file(args.file)
    elif args.remote:
        req = requests.get(args.file, "html.parser")
        analyze_remote_code(req)

if __name__ == "__main__":
    main()
