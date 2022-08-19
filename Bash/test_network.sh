#!/usr/bin/env bash

# Pretty Colors
RED=$(tput setaf 1)
GREEN=$(tput setaf 2)
RESET=$(tput sgr0)

# Green for Information
print_info() {
    echo -e "${GREEN}\n[+] ${1}${RESET}"
}

# Red for Errors
print_error() {
    echo -e "${RED}\n[-] ${1}${RESET}"
}

# Less verbose output
quiet_ping() {
    target="$1"
    err_msg="$2"
    if ! ping -c 1 "$target" >/dev/null 2>&1; then
        print_err "$err_msg"
        exit
    fi
}

# More verbose output
verbose_ping() {
    target="$1"
    err_msg="$2"
    if ! ping -c 1 "$target"; then
        print_error "$err_msg"
        exit
    fi
}

# Usage upon errors
usage() {
    echo -e "\n[-] Incorrect usage!"
    echo -e "Usage: $0 [-v]\n"
    exit 1
}

# Grab IP that's not loopback or docker
ip=$(ip -br a | grep -v "docker" | grep -oE "([0-9]{1,3}\.){3}[0-9]{1,3}" | grep -v "127.0.0.1")

# Set verbosity
verbose=0
while getopts v opt; do
    case $opt in
        v) verbose=1 ;;
        *) usage ;;
    esac
done

# Ping yourself
print_info "Pinging IP of self..."
if (( verbose == 0 ))
then
    quiet_ping "$ip" "Issue with NIC."
else
    verbose_ping "$ip" "Issue with NIC."
fi

# Ping gateway
print_info "Pinging default gateway..."
set -f
octets=("${ip//./ }")
gateway="${octets[0]}.${octets[1]}.${octets[2]}.1"
if (( verbose == 0 ))
then
    quiet_ping "$gateway" "Issue with router."
else
    verbose_ping "$gateway" "Issue with router."
fi

# Ping Google DNS server
print_info "Pinging Google DNS server..."
if (( verbose == 0 ))
then
    quiet_ping "8.8.8.8" "Issue with ISP."
else
    verbose_ping "8.8.8.8" "Issue with ISP."
fi

# Ping google.com
print_info "Pinging Google's domain name..."
if (( verbose == 0 ))
then
    quiet_ping "google.com" "Issue with DNS." 
else
    verbose_ping "google.com" "Issue with DNS."
fi

print_info "All good to go!"
