#!/usr/bin/python3

import argparse
parser = argparse.ArgumentParser(prog='run_by_name.py', description='''
    This function takes a file name and a cmd line and replace {} in
    the cmd line and run it
''')
parser.add_argument('--cmd', help = '''
    The command wanted. E.g. `cat {} | grep apple > {}.temp`
''')
parser.add_argument('name')
args = parser.parse_args()

import os
import re

cmd = re.sub('{}', args.name, args.cmd)
print(cmd)
