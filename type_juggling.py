#!/usr/bin/env python3

# Script to analyze PHP/JS code
# Searches for possible PHP/JS type juggling

import argparse
import colorama
from colorama import Fore, Style
from pathlib import Path
import re
import requests

parser = argparse.ArgumentParser()
location = parser.add_mutually_exclusive_group(required=True)
collision_regex = re.compile("(.*)[!=]=(.*)")
avoid_regex = re.compile("(.*)[!=]==(.*)")

def analyze_local_file(file):
    global collision_regex

    # Keep track of line #
    # Keep track if issue was found
    line_number = 0
    found_issues = False

    # Read local file
    with open(file, "r") as handle:
        while True:
            line = handle.readline()
            if line:
                line_number += 1

                # Possible collisions
                if bool(re.match(collision_regex, line.strip())) and not bool(re.match(avoid_regex, line.strip())):
                    found_issues = True
                    print(f"{Fore.GREEN}[Line {line_number}]{Style.RESET_ALL} {Fore.RED}{line.strip()}{Style.RESET_ALL}")
            else:
                break
        if not found_issues:
            print("[-] No type juggling issues found...")

def main():
    # Get Arguments
    parser.add_argument("--file", "-f", type=str, required=True)
    location.add_argument("--local", "-l", action="store_true")
    location.add_argument("--remote", "-r", action="store_true")
    args = parser.parse_args()

    if args.local:
        analyze_local_file(args.file)
    elif args.remote:
        req = requests.get(args.file, "html.parser")
        remote_file = Path("remote_source_code")
        remote_file.touch()
        with open(remote_file, "w+") as output:
            output.write(req.text)
            output.close()
        analyze_local_file(remote_file)

if __name__ == "__main__":
        main()
