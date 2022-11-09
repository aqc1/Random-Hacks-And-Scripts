#!/usr/bin/env python3

import argparse
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from scapy.all import *

def broadcast(ip: str) -> list:
    """
    Use an ARP broadcast for network discovery
    :param subnet:
        subnet for ARP packet
    :return:
        list of clients
    """
    # Create Packet
    arp_request = ARP(pdst=ip)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = broadcast/arp_request
    answered = srp(packet, timeout=1, verbose=False)[0]

    # Gather clients from broadcast
    clients = list()
    for element in answered:
        client = {
            "ip": element[1].psrc,
            "mac": element[1].hwsrc
        }
        clients.append(client)
    return clients

def main():
    parser = argparse.ArgumentParser(
        description="Network Discovery via ARP Broadcast"
    )
    parser.add_argument(
        "--subnet",
        "-s",
        type=str,
        help="Subnet to broadcast ARP packet (CIDR)",
        required=True
    )
    args = parser.parse_args()

    clients = broadcast(args.subnet)
    for client in clients:
        print(f"IP: {client['ip']:<15} MAC: {client['mac']}")

if __name__ == "__main__":
    main()
