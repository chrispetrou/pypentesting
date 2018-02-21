#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
from selenium import webdriver
from os.path import isfile, exists
from colorama import Fore,Back,Style
from argparse import ArgumentParser, ArgumentTypeError

# console colors
FG, FR, FC = Fore.GREEN, Fore.RED, Fore.CYAN
F, S, BT = Fore.RESET, Style.RESET_ALL, Style.BRIGHT

class Explorer(object):
    """ Explorer: a webdriver that browses a series of urls in new tabs."""
    def __init__(self, urls):
        self.driver = webdriver.Chrome()
        self.urls = urls

    def explore(self):
        try:
            for url in self.urls:
                self.driver.execute_script("window.open('{}');".format(url))
        except Exception, error:
            print error

def console():
    """argument parser"""
    parser = ArgumentParser(description="{}explorer.py:{} dirsearch results-explorer".format(BT+FG,S))
    parser._optionals.title = "{}arguments{}".format(BT,S)
    parser.add_argument('-f', "--file", type=ValidateFile, 
                    help='Specify an dirsearch output-file',
                    metavar='')
    return parser.parse_args()

def ValidateFile(file):
    """validate that the file exists and is readable"""
    if not os.path.isfile(file):
        raise ArgumentTypeError('{}[x] File does not exist{}'.format(FR,S))
    if os.access(file, os.R_OK):
        return file
    else:
        raise ArgumentTypeError('{}[x] File is not readable{}'.format(FR,S))

def process(data):
    """processes dirsearch data"""
    urls = {}
    for line in data:
        st_code, _, url = line.split()
        urls[url] = st_code
    return urls

if __name__ == '__main__':
    filename = console().file
    if filename:
        with open(filename, 'r') as f: 
            data = f.read().splitlines()
        
        if data:
            dt = process(data)
            driver = Explorer(url for url in dt if dt[url]=='200')
            driver.explore()
        else:
            print '[!] No urls found.\n[*] Exiting!'
            sys.exit(0)
    else: print '{}usage:{} explorer.py [-h] [-f]'.format(BT,S)
#_EOF