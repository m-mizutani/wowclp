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
        for ev in psr.read_file(fname):
            print ev
