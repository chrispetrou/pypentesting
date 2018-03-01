#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import dns.zone
import dns.query
from socket import gethostbyname
from validators.domain import domain
from colorama import Fore,Back,Style
from argparse import ArgumentParser, RawTextHelpFormatter, ArgumentTypeError

# console colors
F, S, BT = Fore.RESET, Style.RESET_ALL, Style.BRIGHT
FG, FR, FC, BR = Fore.GREEN, Fore.RED, Fore.CYAN, Back.RED

class DNS_zt():
    """a class that handles dns zone transfers using dnspython"""
    def __init__(self, master, zone, port, timeout, relativize):
        self.master = master
        self.zone = zone
        self.port = port
        self.timeout = timeout
        self.relativize = relativize

    def get_ip(self):
        try:
            return gethostbyname(self.master)
        except Exception, socket_error:
            raise socket_error

    def zone_transfer(self):
        try:
            data = dns.zone.from_xfr(
                dns.query.xfr(
                    zone = self.zone,
                    where = self.get_ip(),
                    port = self.port,
                    relativize = self.relativize,
                    timeout = self.timeout
                )
            )
            info = data.nodes.keys()
            info.sort()
            for i in info: print data[i].to_text(i)
        except Exception, error:
            raise error
            sys.exit(0)

def console():
    """argument parser"""
    parser = ArgumentParser(description="{}dnz.py:{} performs DNS zone transfers".format(BT+FG,S),formatter_class=RawTextHelpFormatter)
    parser._optionals.title = "{}arguments{}".format(BT,S)
    parser.add_argument('-m', "--master", type=validateDomain, help='Specify a master DNS server', metavar='', required=True)
    parser.add_argument('-z', "--zone", type=validateDomain, help='Specify a zone', metavar='', required=True)
    parser.add_argument('-p', '--port', help="Specify a port to use [{0}default {2}{1}53{2}]".format(BT,FG,S), default=53, type=validatePort, metavar='')
    parser.add_argument('-t', '--timeout', help="Set timeout [{0}default {2}{1}120{2}]".format(BT,FG,S), default=120, type=int, metavar='')
    parser.add_argument('-r', "--relativize", help="Relativize [{0}Default:{1} {2}True{1}]".format(BT,S,FG), action='store_false')
    return parser.parse_args()

def validatePort(port):
    if isinstance(int(port), (int, long)):
        if int(port) < 65536: return int(port)
    else: raise ArgumentTypeError('{}[x] Port must be in range 0-65535{}'.format(FR,F))

def validateDomain(url):
    if domain(url): return url
    else: raise ArgumentTypeError('{}[x] Invalid url provided{}'.format(FR,F))

if __name__ == '__main__':
    args = console()
    dn = DNS_zt(args.master, args.zone, args.port, args.timeout, args.relativize)
    try:
        dn.zone_transfer()
    except KeyboardInterrupt:
        print '\n{}[!] Exiting!{}\n'.format(BR,S)
        sys.exit(0)
#_EOF