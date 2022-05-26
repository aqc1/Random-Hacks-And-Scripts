#!/usr/bin/env python3

import argparse
import dns.resolver

# DNS Record types
RECORDS = ["A", "AAAA", "NS", "CNAME", "MX", "PTR", "SOA", "TXT"]

# Resolv DNS record
def resolve_record(host, record_type):
    print(f"\n{record_type} Records")
    print("=" * len(f"{record_type} Records"))
    try:
        response = dns.resolver.resolve(host, record_type) 
        for server in response:
            print(server.to_text())
    except:
        pass

def main():
    # CLI Args
    parser = argparse.ArgumentParser()
    parser.add_argument("--address", "-a", type=str, required=True, help="Address to enumerate DNS records of")
    args = parser.parse_args()

    # Loop through record types, get records
    host = args.address.strip()
    for record in RECORDS:
        resolve_record(host, record)
    
if __name__ == "__main__":
    main()
