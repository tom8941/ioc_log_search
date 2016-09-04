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

import argparse
import os

parser = argparse.ArgumentParser(description='search ioc in logs')
argloggroup = parser.add_mutually_exclusive_group()
argloggroup.add_argument("-l", "--log", help="log file")
argloggroup.add_argument("-z", "--zlog", help="Compressed log file")
parser.add_argument("-i", "--iocfile", help="ioc file")
parser.add_argument("-s", "--split", help="split char")
parser.add_argument("-p", "--position", help="position in the split log")

args = parser.parse_args()

def iocInLog(line, iocset, split_char, position):
    '''
        Check if line contains an ioc

    '''
    return line.split(split_char)[int(position)] in iocset # ex : -4

iocset = frozenset(line.strip('\n') for line in open(args.iocfile))

if args.zlog:
    logset = frozenset(line for line in os.popen("zcat " + args.zlog) if iocInLog(line, iocset, args.split, args.position))
elif args.log:
    logset = frozenset(line for line in open(args.log) if iocInLog(line, iocset, args.split, args.position))

for log in logset:
    print log
