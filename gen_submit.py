#!/usr/bin/python3

import argparse
parser = argparse.ArgumentParser(prog='gen_submit.py', description='''
    This function generates submit sbatch script
''')
parser.add_argument('--prefix')
parser.add_argument('--suffix')
parser.add_argument('--fromm', type = int)
parser.add_argument('--to', type = int)
parser.add_argument('--name', help = 'It will be replace the NAME is template')
parser.add_argument('--template')
parser.add_argument('--ntasks', type = int)
parser.add_argument('--out_prefix')
parser.add_argument('--cmd', default = 'bash,&')
args = parser.parse_args()

import os
import re

def gen_one_submit(from_idx, to_idx, prefix, suffix, submit_idx, header_name, out_prefix, script, cmd):
    submit_name = '{outname}.{idx}.sbatch'.format(outname = out_prefix, idx = submit_idx)
    node_name = '{name}.{idx}'.format(name = header_name, idx = submit_idx)
    script_idx = re.sub('NAME', node_name, script)
    ntasks = to_idx - from_idx + 1
    script_idx = re.sub('NTASKS', str(ntasks), script_idx)
    submit = open(submit_name, 'w')
    submit.write(script_idx)
    _write_bash(submit, from_idx, to_idx, prefix, suffix, cmd)
    submit.write('wait')
    submit.close()

def _write_bash(submit, f, t, p, s, cmd):
    cmd = cmd.split(',')
    cmds = cmd[0]
    cmde = cmd[1]
    for i in range(f, t + 1):
        line = '{cmds} {pre}{i}{suf} {cmde}\n'.format(pre = p, suf = s, i = i, cmds = cmds, cmde = cmde)
        submit.write(line)

f = open(args.template, 'r')
script = f.read()
f.close()
nsubmit = int((args.to - args.fromm + 1) / args.ntasks)

for i in range(nsubmit - 1):
    from_idx = args.fromm + i * args.ntasks
    to_idx = args.fromm + (i + 1) * args.ntasks - 1
    gen_one_submit(from_idx, to_idx, args.prefix, args.suffix, i, args.name, args.out_prefix, script, args.cmd)
from_idx = args.fromm + (nsubmit - 1) * args.ntasks
to_idx = args.to
gen_one_submit(from_idx, to_idx, args.prefix, args.suffix, nsubmit - 1, args.name, args.out_prefix, script, args.cmd)
