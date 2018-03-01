#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import validators
from colorama import Fore,Back,Style
from requests import request
from requests.exceptions import ProxyError, Timeout
from argparse import ArgumentParser, ArgumentTypeError, RawTextHelpFormatter

# console colors
F, S, BT = Fore.RESET, Style.RESET_ALL, Style.BRIGHT
FG, FR, FC, BR = Fore.GREEN, Fore.RED, Fore.CYAN, Back.RED

HOST, PORT = 'localhost', 8080
# you can configure that to use methods of your choice
VERBS = ['TAMPER','GET','POST','HEAD','CONNECT','PATCH','PUT','DELETE','OPTIONS','TRACE','MKCOL']

# headerbugs = {'header':'possible bug'}
headerbugs = {
    'X-XSS-Protection': '{}possibly vulnerable to XSS{}'.format(FR,F),
    'X-Frame-Options': '{}possibly vulnerable to clickjacking{}'.format(FR,F),
    'X-Content-Type-Options': '{}possibly vulnerable to MIME types security risks{}'.format(FR,F),
    'Strict-Transport-Security': '{}HSTS not implemented{}'.format(FR,F),
    'Content-Security-Policy': '{}possibly vulnerable to XSS, clickjacking or other code injection attacks{}'.format(FR,F)}

def console():
    """argument parser"""
    parser = ArgumentParser(description="{}vtamper.py:{} a simple verb tampering/avalaibility checker".format(BT+FG,S),formatter_class=RawTextHelpFormatter)
    parser._optionals.title = "{}arguments{}".format(BT,S)
    parser.add_argument('-u', "--url", type=ValidateURL, 
                    help='Specify a url to check', metavar='')
    parser.add_argument('-vb', '--verb', required=False, 
                    help="Use only a specific verb [{0}default {2}{1}None{2}]".format(BT,FG,S),
                    default=None, choices=VERBS, metavar='')
    parser.add_argument('-p', "--proxy",
                    help="Use a proxy [{0}Default:{1} {2}burp settings{1}]".format(BT,S,FG), action='store_true')
    parser.add_argument('-i', "--inspect",
                    help="Inspect header for each response [{0}Default:{2} {1}False{2}]".format(BT,FR,S), action='store_true')
    return parser.parse_args()

def ValidateURL(url):
    """check if url is valid"""
    if validators.url(url):
        return url
    else: raise ArgumentTypeError('{}[x] Invalid url provided{}'.format(FR,F))

def verbRequest(verb, url, proxy):
    if proxy:
        proxies = {"http":'{}:{}'.format(HOST,PORT), 
                   "https":'{}:{}'.format(HOST,PORT)}
        return request(verb, url, proxies=proxies, verify=False, timeout=10.0)
    else: return request(verb, url, timeout=10.0)

def inspectHeader(headers):
    print '{0}{2}[ HEADER ]{2}{1}'.format(BT,S,'-'*7)
    for k,v in headers.items():
        print '{}{}{} {}'.format(BT, k, S, v)
    print ''
    for bug in headerbugs:
        try:
            headers[bug]
            if bug == 'X-XSS-Protection': 
                if headers[bug]=='0': print '{}=0: {}'.format(bug, headerbugs[bug])
            if bug == 'X-Content-Type-Options': 
                if headers[bug]!='nosniff': print '{}="nosniff": {}'.format(bug, headerbugs[bug])
                pass
        except KeyError:
            print '{} missing: {}'.format(bug, headerbugs[bug])

def proceed(verb, url, proxy, inspect):
    resp = verbRequest(verb, url, proxy)
    if verb=='TAMPER':
        if resp.status_code==200:
            print '[{0}{1}{4}{2}] {0}{5}{2} ...probably {3}vulnerable{2} to verb tampering'.format(BT, FG, S, FR, verb, resp.status_code)
        else: print '[{0}{1}{3}{2}] {5} ({0}{4}{2})'.format(BT, FG, S, verb, resp.status_code, resp.reason)
    else:
        print '[{0}{1}{3}{2}] {5} ({0}{4}{2})'.format(BT, FG, S, verb, resp.status_code, resp.reason)
    if inspect and resp.status_code==200: 
        inspectHeader(resp.headers)

def vtcheck(url, inspect, proxy, verb=None):
    """checks for verb tampering/avalaibility"""
    if proxy:
        print '\n{0}[*]{1} Proxy: {0}{2}ON{1}'.format(BT,S,FG)
    else: print '\n{0}[*]{1} Proxy: {0}{2}OFF{1}'.format(BT,S,FR)
    print "{}[+]{} Checking for HTTP methods availability".format(BT,S)
    try:
        if verb:
            proceed(verb, url, proxy, inspect)
        else:
            for vb in VERBS: proceed(vb, url, proxy, inspect)
    except ProxyError:
        print '{0}[x] Cannot connect to proxy.{1}'.format(FR,F)
    except Timeout:
        print '{0}[x] Connection timed-out (timeout set to 10.0)\n{1}'.format(FR,F)
    except Exception, error:
        print '{0}[x] {2}{1}'.format(FR,F,error)
    except KeyboardInterrupt:
        print '\n{}[*] Exiting!{}\n'.format(BR,S)
        sys.exit(0)

if __name__ == '__main__':
    args = console()
    if args.url:
        vtcheck(args.url, args.inspect, args.proxy, args.verb)
    else: print '{}usage:{} vtamper.py [-h] [-u] [-vb] [-p] [-i]'.format(BT,S)
#_EOF