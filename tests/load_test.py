#!/usr/bin/python

import AUDLclasses

AUDL = AUDLclasses.League()

def load_test():


    AUDL.add_teams()
    for team in AUDL.Teams:
        AUDL.Teams[team].get_info()
        AUDL.Teams[team].add_players()


