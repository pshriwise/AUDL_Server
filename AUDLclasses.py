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
        
     ID = 0;

     Name = '';

     City = '';

     Coach = '';

     Schedule = [];

     Streak = '';

     Players = {};

     Games = {};

     Top_Fives = ();

     def add_players(self):

         # Get information from ultimate-numbers server
         base_url = 'http://www.ultimate-numbers.com/rest/view'
         req = urllib2.Request(base_url + '/team/' + str(self.ID) + '/stats/player/')
         response =  urllib2.urlopen(req)
         page = response.read()
         # Decode json string as python dict
         data = json.loads(page)

         # For every player in the data, 
         # create a new player
         for player in data:
             self.add_player(player)


     def add_player(self, player_info):
         #Add player to team's Players dictionary
         self.Players[player_info['playerName']] = player_info['playerName']
         # NOTE: This currently just adds a player name instead of a 'Player' class.

