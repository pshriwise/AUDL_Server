#!/usr/bin/python

import statget
import urllib2
import json


base_url = 'http://www.ultimate-numbers.com/rest/view'

class League():
    News = {};

    Videos = {};

    Teams = {};

    This_week = [];

    Apple_users = [];

    Android_users = [];

    Video_feeds = [];

    RSS_feeds = [];

    Top_fives = {};


    def add_teams(self):

        teams = statget.team_dict()
      
        # Restructures the teams dict so that the keys are the Team IDs
        # Also creates a new team class instance for each Team ID
        for team in teams: 
            self.Teams[teams[team]] = Team()
        # Right now the list of teams is taken from the team dictionary object in statget.
        # Eventually we will want to grab this list from the server and create
        # new Team classes accordingly.

        # Gives each team its ID value so it can grab its own information from the server.
        for team in self.Teams:
            self.Teams[team].ID = team
            
        
   
   
    

class Team():
        
     ID = None;
