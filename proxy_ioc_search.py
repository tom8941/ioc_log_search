#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ioc_log_search - Optimised search of high IOC number in logs 
#
# Copyright (C) 2016 Thomas Hilt
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import re
import argparse
import os

SPLIT_CHAR = ' ' # separator to split log file
IP_POS = -4 # position of the IP in the split log array
DOM_POS = 6 # url of the IP in the split log array

parser = argparse.ArgumentParser(description='search ioc in logs')
argloggroup = parser.add_mutually_exclusive_group()
argloggroup.add_argument("-l", "--log", help="log file")
argloggroup.add_argument("-z", "--zlog", help="Compressed log file")
parser.add_argument("-i", "--ipioc", help="Ip ioc file")
parser.add_argument("-d", "--domioc", help="Domain ioc file")

args = parser.parse_args()

def ipInIoc(line, iocipset, split_char, position):
    '''
        Check if line contains an ip from iocipset
    '''
    return line.split(split_char)[int(position)] in iocipset # ex : -4

def domInIoc(line, iocdomset, split_char, position):
    '''
        Check if line contains a domain from
    '''
    url = line.split(split_char)[int(position)] # ex : 6
    if re.search('^(\w)*://',url):
        dom = url.split('/')[2]
        if re.search('^www.',dom):
            dom = dom[4:]
    else:
        try:
            portindex = url.index(':')
            if portindex != -1:
                index = len(url) - portindex
                dom = url[:portindex]
            else:
                dom = url
        except Exception:
            dom = url  # malformed domain

    dompart = dom.split('.')
    currdom = '' # domain build progressively by adding one by one top domain

    i=0 # treat the first part of the list that doesn't need '.'

    for part in reversed(dompart):
        if i == 0:
            currdom = part
            i = 1
        else:
            currdom = part + '.' + currdom

        if currdom in iocdomset:
            return True

    return False

iocdomset = frozenset(line.strip('\n') for line in open(args.domioc))
iocipset = frozenset(line.strip('\n') for line in open(args.ipioc))

if args.zlog:
    logset = frozenset(line for line in os.popen("zcat " + args.zlog) if domInIoc(line, iocdomset, SPLIT_CHAR, DOM_POS) or ipInIoc(line, iocipset, SPLIT_CHAR, IP_POS))
elif args.log:
    logset = frozenset(line for line in open(args.log) if domInIoc(line, iocdomset, SPLIT_CHAR, DOM_POS) or ipInIoc(line, iocipset, SPLIT_CHAR, IP_POS))

for log in logset:
    print log
