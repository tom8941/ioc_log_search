#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import time
import sys
import gzip
import argparse
import os
import datetime

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
