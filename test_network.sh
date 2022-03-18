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

# Grab IP that's not loopback
ip=$(ip -br a | grep -oE "([0-9]{1,3}\.){3}[0-9]{1,3}" | grep -v "127.0.0.1")

# Ping yourself
print_info "Pinging IP of self..."
ping -c 1 $ip
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
ping -c 1 $gateway
if [ $? -ne 0 ]
then
    print_error "Issue with router."
    exit
fi

# Ping Google DNS server
print_info "Pinging Google DNS server..."
ping -c 1 8.8.8.8
if [ $? -ne 0 ]
then
    print_error "Issue with ISP."
    exit
fi

# Ping google.com
print_info "Pinging Google's domain name..."
ping -c 1 "google.com"
if [ $? -ne 0 ]
then
    print_error "Issue with DNS."
    exit
fi

print_info "All good to go!"
