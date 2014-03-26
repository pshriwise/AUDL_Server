#!/usr/bin/python

import sys
sys.path.insert(0,'..')
import AUDLclasses

import os
os.chdir('../')

from subprocess import call

def load_test():

    test_league = AUDLclasses.League()
    test_league.add_teams()


#def test_schedules():

#    test_league = AUDLclasses.League()
#    test_league.add_teams()

#    for team in test_league.Teams:
#        assert 14 == len(test_league.Teams[team].Games), len(test_league.Teams[team].Games)

def test_news():

    test_league = AUDLclasses.League()
    test_league.get_news()

    assert 0 != len(test_league.News)


