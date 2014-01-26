#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
World of Warcraft, Combat Log Parser
---------

Copyright (c) 2013 Masayoshi Mizutani <mizutani@sfc.wide.ad.jp>
All rights reserved.
 *
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:
1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE FOUNDATION OR CONTRIBUTORS
BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.

-----------
Reference: http://www.wowwiki.com/API_COMBAT_LOG_EVENT
'''

import csv
import time
import datetime

'''
---------------------------------------------------------
Prefix Parser Set
---------------------------------------------------------
'''

class SpellParser:
    def __init__(self): pass
    def parse(self, cols):
        return ({
            'spellId': cols[0],
            'spellName': cols[1],
            'spellSchool': cols[2]
        }, cols[3:])

class EnvParser:
    def __init__(self): pass
    def parse(self, cols):
        return ({
            'environmentalType': cols[0]
        }, cols[1:])

class SwingParser:
    def __init__(self): pass
    def parse(self, cols): return ({}, cols)


'''
---------------------------------------------------------
Suffix Parser Set
---------------------------------------------------------
'''

class DamageParser:        
    def __init__(self): pass
    def parse(self, cols):
        return {
            'amount': cols[0],
            'overkill': cols[1],
            'school': cols[2],
            'resisted': cols[3],
            'blocked': cols[4],
            'absorbed': cols[5],
            'critical': (cols[6] == '1'),
            'glancing': (cols[7] == '1'),
            'crushing': (cols[8] == '1'),
        }

class MissParser:
    def __init__(self): pass
    def parse(self, cols):
        obj = {
            'missType': cols[0]
        }
        if len(cols) > 1: obj['isOffHand'] = cols[1]
        if len(cols) > 2: obj['amountMissed'] = cols[2]
        return obj

class HealParser:
    def __init__(self): pass
    def parse(self, cols):
        return {
            'amount': cols[0],
            'overhealing': cols[1],
            'absorbed': cols[2],
            'critical': cols[3],
        }

class EnergizeParser:
    def __init__(self): pass
    def parse(self, cols):
        return {
            'amount': cols[0],
            'powerType': cols[1],
        }

class DrainParser:
    def __init__(self): pass
    def parse(self, cols):
        return {
            'amount': cols[0],
            'powerType': cols[1],
            'extraAmount': cols[2],
        }

class DrainParser:
    def __init__(self): pass
    def parse(self, cols):
        return {
            'amount': cols[0],
            'powerType': cols[1],
            'extraAmount': cols[2],
        }

class LeechParser:
    def __init__(self): pass
    def parse(self, cols):
        return {
            'amount': cols[0],
            'powerType': cols[1],
            'extraAmount': cols[2],
        }

class SpellBlockParser:
    def __init__(self): pass
    def parse(self, cols):
        obj = {
            'extraSpellID': cols[0],
            'extraSpellName': cols[1],
            'extraSchool': cols[2],
        }
        if len(cols) == 4: obj['auraType'] = cols[3]
        return obj

class ExtraAttackParser:
    def __init__(self): pass
    def parse(self, cols):
        return {
            'amount': cols[0]
        }

class AuraParser:
    def __init__(self): pass
    def parse(self, cols):
        obj = {
            'auraType': cols[0]
        }
        if len(cols) == 2: obj['amount'] = cols[1]
        return obj

class AuraBrokenParser:
    def __init__(self): pass
    def parse(self, cols):
        return {
            'extraSpellID': cols[0],
            'extraSpellName': cols[1],
            'extraSchool': cols[2],
            'auraType': cols[3],
        }

class CastFailedParser:
    def __init__(self): pass
    def parse(self, cols):
        return {
            'failedType': cols[0],
        }

'''
---------------------------------------------------------
Special Event Parser Set
---------------------------------------------------------
'''

class EnchantParser:
    def __init__(self): pass
    def parse(self, cols):
        return ({
            'spellName': cols[0],
            'itemID': cols[1],
            'itemName': cols[2],
        }, cols)

class EncountParser:
    def __init__(self): pass
    def parse(self, cols):
        obj = {
            'encounterID': cols[0],
            'encounterName': cols[1],
            'difficultyID': cols[2],
            'groupSize': cols[3],
        }
        if len(cols) == 5: obj['success'] = (cols[4] == '1')
        return obj

class VoidParser:
    def __init__(self): pass
    def parse(self, cols): return ({}, cols)

class VoidSuffixParser:
    def __init__(self): pass
    def parse(self, cols): return {}
    



class Parser:
    def __init__(self):
        self.ev_prefix = {
            'SWING': SwingParser(),
            'SPELL_BUILDING': SpellParser(),
            'SPELL_PERIODIC': SpellParser(),
            'SPELL': SpellParser(),
            'RANGE': SpellParser(),
            'ENVIRONMENTAL': EnvParser(),
        }
        self.ev_suffix = {
            '_DAMAGE': DamageParser(),
            '_MISSED': MissParser(),
            '_HEAL': HealParser(),
            '_ENERGIZE': EnergizeParser(),
            '_DRAIN': DrainParser(),
            '_LEECH': LeechParser(),
            '_INTERRUPT': SpellBlockParser(),
            '_DISPEL': SpellBlockParser(),
            '_DISPEL_FAILED': SpellBlockParser(),
            '_STOLEN': SpellBlockParser(),
            '_EXTRA_ATTACKS': ExtraAttackParser(),
            '_AURA_APPLIED': AuraParser(),
            '_AURA_REMOVED': AuraParser(),
            '_AURA_APPLIED_DOSE': AuraParser(),
            '_AURA_REMOVED_DOSE': AuraParser(),
            '_AURA_REFRESH': AuraParser(),
            '_AURA_BROKEN': AuraParser(),
            '_AURA_BROKEN_SPELL': AuraBrokenParser(),
            '_CAST_START': VoidSuffixParser(),
            '_CAST_SUCCESS': VoidSuffixParser(),
            '_CAST_FAILED': CastFailedParser(),
            '_INSTAKILL': VoidSuffixParser(),
            '_DURABILITY_DAMAGE': VoidSuffixParser(),
            '_DURABILITY_DAMAGE_ALL': VoidSuffixParser(),
            '_CREATE': VoidSuffixParser(),
            '_SUMMON': VoidSuffixParser(),
            '_RESURRECT': VoidSuffixParser(),
        }
        self.sp_event = {
            'DAMAGE_SHIELD': (SpellParser(), DamageParser()),
            'DAMAGE_SPLIT': (SpellParser(), DamageParser()),
            'DAMAGE_SHIELD_MISSED': (SpellParser(), MissParser()),
            'ENCHANT_APPLIED': (EnchantParser(), VoidSuffixParser()),
            'ENCHANT_REMOVED': (EnchantParser(), VoidSuffixParser()),
            'PARTY_KILL': (VoidParser(), VoidSuffixParser()),
            'UNIT_DIED': (VoidParser(), VoidSuffixParser()),
            'UNIT_DESTROYED': (VoidParser(), VoidSuffixParser()),
        }
        self.enc_event = {
            'ENCOUNTER_START': EncountParser(),
            'ENCOUNTER_END': EncountParser(),
        }

    def parse_line(self, cols):
        head = cols[0].split(' ')
        if len(head) != 4: raise Exception('invalid head format, ' + repr(cols))

        s = '{2} {0[0]:02d}/{0[1]:02d} {1}'.format(map(int, head[0].split('/')), head[1][:-4], datetime.datetime.today().year)
        d = datetime.datetime.strptime(s, '%Y %m/%d %H:%M:%S')
        ts = time.mktime(d.timetuple()) + float(head[1][-4:])
        event = head[3]

        if self.enc_event.get(event):
            obj = {
                'timestamp': ts,
                'event': event,
            }
            obj.update(self.enc_event[event].parse(cols[1:]))
            print obj
            return obj

        obj = {'timestamp': ts,
               'event': event,
               'sourceGUID':   cols[1],
               'sourceName':   cols[2],
               'sourceFlags':  cols[3],
               'sourceFlags2': cols[4],
               'destGUID':   cols[5],
               'destName':   cols[6],
               'destFlags':  cols[7],
               'destFlags2': cols[8]}

        if len(cols) < 9: raise Exception('invalid format, ' + repr(cols))

        suffix = ''
        prefix_psr = None
        suffix_psr = None

        matches = []
        for (k, p) in self.ev_prefix.iteritems():
            if obj['event'].startswith(k): matches.append(k)

        if len(matches) > 0:
            prefix = max(matches, key=len)
            prefix_psr = self.ev_prefix[prefix]
            suffix = obj['event'][len(prefix):]
            suffix_psr = self.ev_suffix[suffix]
        else:
            for (k, psrs) in self.sp_event.iteritems():
                if obj['event'] == k:
                    (prefix_psr, suffix_psr) = psrs
                    break

        if prefix_psr is None or suffix_psr is None:
            raise Exception('Unknown event format, ' + repr(cols))

        (res, remain) = prefix_psr.parse(cols[9:])
        obj.update(res)
        obj.update(suffix_psr.parse(remain))

        if obj['destName'] == 'Muret' and obj['event'] == 'SPELL_HEAL': 
            for i in range(len(cols)):
                print i, cols[i]
            print obj

        return obj


    def read_file(self, fname):
        for cols in csv.reader(open(fname, 'r')):
            yield self.parse_line(cols)

if __name__ == '__main__':
    import sys
    p = Parser()
    for arg in sys.argv[1:]:
        for a in p.read_file(arg):
            pass
                # print a['timestamp'], a['event'], a['sourceName'], a['amount']

