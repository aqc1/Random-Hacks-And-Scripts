#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Script asks for an IP address to encode in various ways
# Useful for bypassing regex in WAFs for matching IP addresses

import random
import re
import sys


class IP_Encoder:
    """
    Class to define methods of encoding IPv4 addresses

    ip (str)
        An IPv4 address
    octets (list)
        An IP address split into its octets
    """
    def __init__(self, ip: str):
        self.ip = ip
        self.octets = ip.split(".")

    def to_binary(self, octet: str) -> str:
        """
        Convert an octet to its binary equivalent
        :param octet:
            octet to convert
        :return:
            binary representation of octet
        """
        return str(bin(int(octet)))

    def to_octal(self, octet: str) -> str:
        """
        Convert an octet to its octal equivalent
        :param octet:
            octet to convert
        :return:
            octal representation of octet
        """
        return str(oct(int(octet))).replace("0o", "0")

    def to_hex(self, octet: str) -> str:
        """
        Convert an octet to its hex equivalent
        :param octet:
            octet to convert
        :return:
            hex representation of octet
        """
        return str(hex(int(octet)))

    def raw_decimal(self) -> str:
        """
        Convert IP to a decimal string
        :return:
            decimal string
        """
        decimal_value = 0
        for index, octet in enumerate(self.octets, 1):
            decimal_value += (int(octet) * pow(256, 4-index))
        return str(decimal_value)

    def raw_octal(self) -> str:
        """
        Convert IP to an octal string
        :return:
            octal string
        """
        return self.to_octal(self.raw_decimal())

    def raw_hex(self) -> str:
        """
        Convert IP to a hex string
        :return:
            hex string
        """
        return self.to_hex(self.raw_decimal())

    def octal_octets(self) -> str:
        """
        Convert each octet to octal equivalent
        :return:
            IP with octets in octal
        """
        return ".".join([self.to_octal(octet) for octet in self.octets])

    def hex_octets(self) -> str:
        """
        Convert each octet to hex equivalent
        :return:
            IP with octets in hex
        """
        return ".".join([self.to_hex(octet) for octet in self.octets])

    def random_octet_encoding(self) -> str:
        """
        Convert each octet to a random encoding
        :return:
            IP with randomly encoded octets
        """
        operations = [
            lambda x: x,
            lambda x: self.to_octal(x),
            lambda x: self.to_hex(x)
        ]
        encoded_octets = list()
        for octet in self.octets:
            operation = random.choice(operations)
            encoded_octets.append(operation(octet))
        return ".".join(encoded_octets)

    def random_octet_encoding_with_padding(self) -> str:
        """
        Convert each octet to a random encoding
        Each octet will have random padding
        :return:
            IP with randomly encoded and padded octets
        """
        operations = [
            lambda x: x,
            lambda x: "0" * random.randint(4, 9) + self.to_octal(x),
            lambda x: self.to_hex(x).replace(
                "0x",
                "0x" + "0" * random.randint(4, 9)
            )
        ]
        encoded_octets = list()
        for octet in self.octets:
            operation = random.choice(operations)
            encoded_octets.append(operation(octet))
        return ".".join(encoded_octets)


def main():
    initial_ip = input("IP Address: ")
    if not re.match("^\d{1,3}(\.\d{1,3}){3}$", initial_ip):
        usage()
    encoder = IP_Encoder(initial_ip)
    print("[+] Raw Conversions")
    print(f"\t[>] Decimal    : {encoder.raw_decimal()}")
    print(f"\t[>] Octal      : {encoder.raw_octal()}")
    print(f"\t[>] Hexadecimal: {encoder.raw_hex()}")
    print("[+] Octet Encodings:")
    print(f"\t[>] Octal Octets      : {encoder.octal_octets()}")
    print(f"\t[>] Hexadecimal Octets: {encoder.hex_octets()}")
    print("[+] Random Octet Encodings")
    for _ in range(5):
        print(f"\t[>] {encoder.random_octet_encoding()}")
    print("[+] Random Octet Encodings with Random Padding")
    for _ in range(5):
        print(f"\t[>] {encoder.random_octet_encoding_with_padding()}")


def usage():
    print("[-] Invalid IP Address!")
    print("[!] Example Valid IP Addresses:")
    print("\t[>] 127.0.0.1")
    print("\t[>] 10.10.10.10")
    print("\t[>] 192.168.10.5")
    sys.exit(-1)

if __name__ == "__main__":
    main()
