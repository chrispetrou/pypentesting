#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, re
from pyperclip import copy
from os.path import isfile, exists
from colorama import Fore,Back,Style
from argparse import ArgumentParser, ArgumentTypeError

# console colors
FG, FR, FC = Fore.GREEN, Fore.RED, Fore.CYAN
F, S, BT = Fore.RESET, Style.RESET_ALL, Style.BRIGHT

def console():
    """argument parser"""
    parser = ArgumentParser(description="{}shconverter.py:{} an objdump to shellcode converter".format(BT+FG,S))
    parser._optionals.title = "{}arguments{}".format(BT,S)
    parser.add_argument('-f', "--file", type=ValidateFile, 
                    help='Specify an objdump output-file',
                    metavar='')
    parser.add_argument('-c', "--copy",
                    help="Copy shellcode to clipboard",
                    action='store_true')
    return parser.parse_args()

def ValidateFile(file):
    """validate that the file exists and is readable"""
    if not os.path.isfile(file):
        raise ArgumentTypeError('{}[x] File does not exist{}'.format(FR,S))
    if os.access(file, os.R_OK):
        return file
    else:
        raise ArgumentTypeError('{}[x] File is not readable{}'.format(FR,S))

def convert(filename, cp):
    """converts objdump output --> shellcode"""
    with open(filename, 'r') as f:
        lines = f.read().splitlines()
    
    hxpat = r'[a-f0-9]'
    opcodes = []
    for line in lines:
        asm = filter(lambda x: len(x)==2 and re.match(hxpat,x), line.split())
        if asm:
            opcodes.append('\\x'+'\\x'.join(asm))
    
    shellcode = ''.join(opcodes)
    if cp:
        copy(shellcode)
        print '{}[+]{} Shellcode copied successfully to clipboard!'.format(BT+FG, S)
    print '\n{}[+]{} Shellcode length: {}{}{}'.format(BT+FG, S, FR, len(shellcode)/4, F)
    print '{0}[+]{1} Here is your shellcode:\n\n"{3}{2}{1}"\n'.format(BT+FG, S, shellcode, FC)

if __name__ == '__main__':
    args = console()
    if args.file:
        convert(args.file, args.copy)
    else: print '{}usage:{} shconverter.py [-h] [-f] [-c]'.format(BT,S)
#_EOF