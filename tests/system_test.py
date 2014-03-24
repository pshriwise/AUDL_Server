#!/usr/bin/python

import sys
sys.path.insert(0,'..')
import AUDLclasses

import os
os.chdir('../')


def load_test():

    test_league = AUDLclasses.League()
    test_league.add_teams()


def check_schedules():

    test_league = AUDL.League()
    test_league.add_teams()

    for team in AUDL.Teams:
        assert 14 == len(AUDL.Teams[team].Games)

def check_news():

    test_league = AUDL.League()
    test_league.get_news()

    assert 0 != len(AUDL.News)


