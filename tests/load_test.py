#!/usr/bin/python

import AUDLclasses

AUDL = AUDLclasses.League()

AUDL.add_teams()


def test_add_teams_load():

    for team in AUDL.Teams:
        try:
            assert AUDL.Teams[team].ID != 0
        finally:
            print "No team ID found."

        try:
            assert AUDL.Teams[team].Name != ''
        finally:
            print "error for" , AUDL.Teams[team].ID
