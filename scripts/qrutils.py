#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import requests
from argparse import *
from bs4 import BeautifulSoup
from subprocess import Popen, PIPE
from colorama import Fore,Back,Style

# console colors
FG, FR, FC = Fore.GREEN, Fore.RED, Fore.CYAN
F, S, BT = Fore.RESET, Style.RESET_ALL, Style.BRIGHT

def console():
    """a simple cli-parser with optional and required options """
    parser = ArgumentParser(description="{}qrutils.py:{} QR encoder/decoder".format(BT+FG,S))
    parser._optionals.title = "{}arguments{}".format(BT,S)
    group = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument('-f', "--filename",
                        help="Specify an output-name", metavar='')
    group.add_argument('-i', "--img", type=ValidateImg, 
                        help='Specify a QR-image to decode', metavar='')
    group.add_argument('-m', "--msg", 
                        help="Specify a message to QR-encode", metavar='')
    return parser.parse_args()

def ValidateImg(img):
    """kind of validate the img"""
    SUFFIX = ('.jpg','.tiff','.png','.jpeg')
    if img.endswith(SUFFIX):
        return img
    else:
        print '\n{}[x] Invalid image!{}\n'.format(FR,F)
        sys.exit(0)

class QR_Reader(object):
    """decode QR-code using zxing online decoder"""
    def __init__(self, img):
        self.img = img

    def decode(self):
        url = "http://zxing.org/w/decode"
        payload = {
            'f':open(self.img, "rb"),
        }
        try:
            response = requests.Session().post(url, files=payload)
            soup = BeautifulSoup(response.text, 'html.parser')
            return str(soup.find('pre').text)
        except Exception, error:
            raise error

def main():
    args = console()
    if args.img:
        msg = QR_Reader(args.img).decode()
        print "\n{}[+]{} QR decoded ~~> {}\n".format(BT+FG,S,msg)
        sys.exit(0)
    else:
        if args.filename is None:
            print '\n{}[x] No name provided for the output!{}\n'.format(FR,F)
            sys.exit(0)
        msg = args.msg
        Popen(['qrencode', '-o', args.filename, msg, '-s', '10'], stdout=PIPE)
        sys.exit(0)

if __name__ == '__main__':
    main()
# -EOF