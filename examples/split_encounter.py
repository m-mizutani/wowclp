#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

path = os.path.abspath(sys.argv[0])
bdir = os.path.dirname(path)
sys.path.append(os.path.join(bdir, '..'))

import wowclp

if __name__ == '__main__':
    psr = wowclp.Parser()
    for fname in sys.argv[1:]:
        fd = None
        for line in open(fname, 'r'):
            ev = psr.parse_line(line)
            if ev['event'] == 'ENCOUNTER_START':
                enc_name = ev['encounterName'].replace(' ', '_')
                fname = 'WoWCombatLog_{2}_{0}_{1}man.txt'.format(enc_name, 
                                                                 ev['groupSize'],
                                                                 int(ev['timestamp']))
                print 'Open', fname
                fd = open(fname, 'w')
                
            if fd: fd.write(line)
                
            if ev['event'] == 'ENCOUNTER_END':
                print 'Close', fname
                fd.close()
                fd = None

