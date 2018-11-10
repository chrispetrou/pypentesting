#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
┌════════════════════════════════════┐
│ fakeid generator using:            │
│ https://www.fakenamegenerator.com/ │
└════════════════════════════════════┘
"""

import warnings
from requests import get
from bs4 import BeautifulSoup
from tabulate import tabulate
from fake_useragent import UserAgent
warnings.filterwarnings("ignore")

url = "https://www.fakenamegenerator.com/"
headers = {'User-Agent':str(UserAgent().random)}

soup = BeautifulSoup(get(url, headers = headers, verify=False).text, 'html.parser')
data = soup.find('div', attrs={'class':'info'}).text.strip().split('\n\n')

info = {
    'name'    : data[0].strip(),
    'age'     : data[11].split('\n')[2],
    'phone'   : data[7].split('\n')[1],
    'email'   : data[14].split()[2],
    'password': data[16].split('\n')[2],
    'company' : data[24].split('\n')[1]
}
print tabulate(info.items(), tablefmt="fancy_grid")
