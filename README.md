
wowclp: World of Warcraft Combat Log Parser
==========

Overview
-----

wowclp parses combat log data such as WoWCombatLog.txt. Raw combat log file is just csv format and user can not recognize each parameter. The wowclp labels parameters of combat log based on wowwiki's guide.


Usage
-----

### Sample code

    #!/usr/bin/env python
	# -*- coding: utf-8 -*-

    import wowclp
    
    if __name__ == '__main__':
        psr = wowclp.Parser()
        for fname in sys.argv[1:]:
            for ev in psr.read_file(fname):
                print ev


### Result (by PrettyPrinter)

    { 'absorbed': 0,
      'amount': 817790,
      'blocked': 0,
      'critical': True,
      'crushing': False,
      'destFlags': [   'AFFILIATION_OUTSIDER',
               'CONTROL_NPC',
               'REACTION_HOSTILE',
               'TYPE_NPC',
               'TARGET'],
      'destFlags2': [],
      'destGUID': '0xF1311C28000000DD',
      'destName': "Kor'kron Skullsplitter",
      'event': 'SPELL_DAMAGE',
      'glancing': False,
      'overkill': '-1',
      'resisted': 0,
      'school': ['Shadow'],
      'sourceFlags': [   'AFFILIATION_MINE',
                 'CONTROL_PLAYER',
                 'REACTION_FRIENDLY',
                 'TYPE_PLAYER'],
      'sourceFlags2': [],
      'sourceGUID': '0x0300000007F97AFF',
      'sourceName': 'Muret',
      'spellId': '116858',
      'spellName': 'Chaos Bolt',
      'spellSchool': ['Shadow'],
      'timestamp': 1390652089.429}
