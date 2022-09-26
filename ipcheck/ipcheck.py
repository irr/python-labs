from ipaddress import ip_address, ip_network

import csv
import os

ipv4_reserved = [
    "10.0.0.0/8",
    "100.64.0.0/10",
    "172.16.0.0/12",
    "192.0.0.0/24",
    "192.168.0.0/16",
    "198.18.0.0/15",
]

ipv6_reserved = [
    "64:ff9b:1::/48",
    "fc00::/7",
]

ip_ranges = ipv4_reserved + ipv6_reserved


def internal(ipaddress):
    if ipaddress is None or len(ipaddress.strip()) == 0:
        return False
    for ip in ip_ranges:
        if ip_address(ipaddress) in ip_network(ip):
            return True
    return False


with open(f"{os.path.expanduser('~')}/tmp/fraud.csv", 'r' ) as f:
    reader = csv.DictReader(f)
    for row in reader:
        if internal(row['IP Address']):
            print(row) 
