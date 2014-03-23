#!/usr/bin/python

import sys
sys.path.insert(0,'/home/patrick/AUDL_server')

import os
os.chdir('../')
import AUDLclasses

def load_test():

    test_league = AUDLclasses.League()
    test_league.add_teams()


def check_schedules():

    AUDL = AUDL.League()
    AUDL.add_teams()

    for team in AUDL.Teams:
        assert 14 == len(AUDL.Teams[team].Games)

def check_news():

    AUDL = AUDL.League()
    AUDL.get_news()

    assert 0 != len(AUDL.News)
