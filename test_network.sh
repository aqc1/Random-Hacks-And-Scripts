#!/usr/bin/env bash

# Pretty Colors
RED=$(tput setaf 1)
GREEN=$(tput setaf 2)
RESET=$(tput sgr0)

print_info() {
    echo -e "${GREEN}\n[+] ${1}${RESET}"
}

print_error() {
    echo -e "${RED}\n[-] ${1}${RESET}"
}

# Usage func
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
if (( $verbose == 0 ))
then
    ping -c 1 $ip 2>&1 >/dev/null
else
    ping -c 1 $ip
fi

if [ $? -ne 0 ]
then
    print_error "Issue with NIC."
    exit
fi

# Ping gateway
print_info "Pinging default gateway..."
set -f
octets=(${ip//./ })
gateway="${octets[0]}.${octets[1]}.${octets[2]}.1"
if (( $verbose == 0 ))
then
    ping -c 1 $gateway 2>&1 >/dev/null
else
    ping -c 1 $gateway
fi

if [ $? -ne 0 ]
then
    print_error "Issue with router."
    exit
fi

# Ping Google DNS server
print_info "Pinging Google DNS server..."
if (( $verbose == 0 ))
then
    ping -c 1 8.8.8.8 2>&1 >/dev/null
else
    ping -c 1 8.8.8.8
fi

if [ $? -ne 0 ]
then
    print_error "Issue with ISP."
    exit
fi

# Ping google.com
print_info "Pinging Google's domain name..."
if (( $verbose == 0 ))
then
    ping -c 1 "google.com" 2>&1 >/dev/null
else
    ping -c 1 "google.com"
fi

if [ $? -ne 0 ]
then
    print_error "Issue with DNS."
    exit
fi

print_info "All good to go!"
