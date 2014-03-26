#!/usr/bin/python

import urllib2, json
import feedparser as fp
import MediaClasses
from datetime import datetime as dt
import datetime

base_url = 'http://www.ultimate-numbers.com/rest/view'

class League():
    """ 
    Class which acts as a central node for all other classes
    on the AUDL server.
    """
    def __init__(self):
         # A dictionary containing all video link class instances
        self.Videos = {};
        # A list of information about the upcoming
        # week in the AUDL
        self.This_week = [];
        # A list of apple product device IDs
        # on which the AUDL app is installed
        self.Apple_users = [];
        # A list of android OS device IDs on
        # which the AUDL app is installed
        self.Android_users = [];
        # A list of video feeds that the server is
        # to glean information from
        self.Video_feeds = [];
        # A list of RSS feeds the server is to
        # glean information from 
        self.RSS_feeds = ['http://www.theaudl.com/appfeed.xml'];
        # A dictionary containing lists of the top five 
        # players for a given statistic and their stat
        # in sorted order
        self.Top_fives = {};


    def add_teams(self, filename='Teams_Info', players = True, games = True, stats = True):
        """
        This method retrieves all known teams from the ultimate-numbers
        server using a dictionary that keeps track of team IDs we care about. 
        filename - file that the teams information should be read from*
        players - boolean indicating whether or not to add players
        games -  boolean indicating whether or not to add games
        stats -  boolean indicating whether or not to add team stats

        For each team, the basic info for that team is taken from a file
        in the repository and their game information is retrieved from the 
        ultimate-numbers server. 
        
        * expects a certain format (see Teams_Info)
        """
        #Open teams information file
        teams_info = open(filename, 'r')
        found = False
        self.Teams={}
        self.Divisions = {}
        for line in teams_info: 
              # See if we've reached the beginning of
              # some team info

             if line.count("ID") == 1:
                       found = True
                       line = line.split(":")[1]
                       # An int containing the team ID
                       ID = int(line[1:].rstrip())
                       line = teams_info.next().split(":")[1]
                       # A string containing the team's name. 
                       Name = line[1:].rstrip()
                       line = teams_info.next().split(":")[1]
                       # Add team to division
                       Div = line[1:].rstrip()
                       if Div in self.Divisions.keys():
                           self.Divisions[Div].append(ID)
                       else:
                           self.Divisions[Div] = [ID]        
                       line = teams_info.next().split(":")[1]    
                       # A string containing the team's home city. 
                       City = line[1:].rstrip()
                       line = teams_info.next().split(":")[1]
                       # A string containing the name of the team's coach
                       Coach = line[1:].rstrip()
                       self.Teams[ID] = Team(self, ID, Name, City, Coach)
        if not found: print "No Team with that ID on record"
   
        # Gives each team its ID value so it can grab its own information from the server.
        for team in self.Teams:
            if players: self.Teams[team].add_players()
            if games: self.Teams[team].add_games()
            if stats:   self.Teams[team].populate_team_stats()

    def get_news(self):
        """
        Gets all news articles for the rss feeds provided to the League class
        """
        # A dictionary containing all related news article
        # class instances
        self.News = {};

        for feed in self.RSS_feeds:
            # parse the feed into a python dictionary
            data = fp.parse(feed)
            # create a new article for each article in the feed
            # later, we will need to limit the number of articles in the feed
            for ent in data.entries:
                temp_news_class = MediaClasses.Article(ent.published, ent.link, ent.title)
                self.News[id(temp_news_class)] = temp_news_class
    
    def team_list(self):
        """
        A method for populating the Teams page in the UI. Returns a list of all teams in the 
        League class along with their IDs.
        """
        data_out = []
        for team in self.Teams:
            if hasattr(self.Teams[team], 'Name') and hasattr(self.Teams[team], 'City'):
                AUDL_Name = self.Teams[team].City + " " + self.Teams[team].Name
                new_tup = (AUDL_Name, self.Teams[team].ID)
                data_out.append(new_tup)
        return data_out

    def news_page_info(self):
        """
        Returns information needed to populate the news page in the app UI
        """
        # Init the output list, add a header
        art_list=["AUDL News"]
        # shorten the path to the News dictionary
        News = self.News
        # Get the title and article url for every article
        # create a tuple and append to the output lits
        for art in News:
            art_tup = (News[art].Title, News[art].url)
            art_list.append(art_tup)

        return art_list

    def league_game_exist(self, name, date):
        """
        Returns whether nor not a game exists for a team (by name)
        for a given date. 

        """

        for team in self.Teams:
            AUDL_Name = self.Teams[team].City + " " + self.Teams[team].Name

            if AUDL_Name in name:
                return self.Teams[team].game_exist(date)
            else:
                pass
        return False,None
        

    def return_upcoming_games(self, teams=None, days_ahead=14):
        """
        Returns any games occurring within 2 weeks of the current date.

        teams - a list of team ids to check for games
        days_ahead - indicates that games beyond this many days ahead of
                today should not be included. Default is two weeks.

        If no teams are passed to the function, return this information
        for all teams in the league
        """

        data_out = []
        # If no teams are passed in, add all available teams to the schedule
        if teams == None:
            teams = []
            for team in self.Teams:
                ID = self.Teams[team].ID
                teams.append(ID)
   
        game_list = []
        #loop through each team and get their game class instances
        for team in teams:
            games = self.Teams[team].Games
            for game in games:
                inst = self.Teams[team].Games[game]                    
                if inst not in game_list: game_list.append(inst)
        
        for game in game_list:
            date = game.date
            time = game.time
            team1 = game.home_team
            team1ID = game.home_team_id
            team2 = game.away_team 
            team2ID = game.away_team_id
            
            game_date = dt.strptime(game.date, "%m/%d/%y").date()
            now = dt.today().date()
            delta = game_date-now
            if delta.days > days_ahead:
                pass
            else:
                game_tup=(team1,team1ID,team2,team2ID,date,time)
                data_out.append(game_tup)
       
        #data_out.sort(key= lambda set: datetime.datetime.strptime(set[2], '%m/%d/%y'))
        return data_out

    def return_schedules(self):
    
        data_out = []
        for div in self.Divisions:
            game_sched = self.return_upcoming_games(self.Divisions[div],20)
            data_out.append([div,game_sched])
        
        return data_out

    def name_to_id(self, name):
        """
        Loops through each team to look for a matching name. 
        If one is found, then the id is returned as an int.
        """
 
        #loop through teams and find a match:
        teams = self.Teams

        for ID, team_inst in teams.items():
            AUDL_name = team_inst.City + " " + team_inst.Name
            if AUDL_name in name.rstrip(): return ID
        # false case is a corner case until 2014 games begin
        return 0
class Team():
    """
    This class keeps all of the statistical information 
    for a given team in the league. (player info, statistics,
    game schedules, etc.)
    """
    def __init__(self, League, ID, Name, City, Coach ):
         # The team's ultimate-numbers ID. This is how we recognize this team on the 
         # ultimate numbers server. It is also our way of giving each team a 
         # unique identifier.
         self.ID = ID
         # A string containing the team's current win or 
         # loss streak.
         self.Streak = ''
         # An attribute containing the League isntance the team belongs to
         self.League = League
         # A string containing the Team's Name
         self.Name = Name
         # A string containing the Team's City
         self.City = City
         # A string containing the Team's Coach name
         self.Coach = Coach



    def add_players(self):
        """
        Adds players to the Team class attribute 'Players' from the ultimate-numbers
        server.
        """

        # A dictionary containing a set of Player class
        # instances pertaining to this team.
        self.Players = {}

        # Get information from ultimate-numbers server
        base_url = 'http://www.ultimate-numbers.com/rest/view'
        req = urllib2.Request(base_url + '/team/' + str(self.ID) + '/stats/player')
        response =  urllib2.urlopen(req)
        page = response.read()
        # Decode json string as python dict
        data = json.loads(page)

        # For every player in the data, 
        # create a new player
        

        for player in data:
            #Add player to team's Players dictionary
            self.Players[player['playerName']] = Player()
            self.add_player_info(player)

    def add_player_info(self, player_info):
        """
        Adds player name, number, stats, etc. to a player class. 

        Assumes the ultimate-numbers info has already been loaded.
        """
        
        #Add player's info to new Player class instance
        self.Players[player_info['playerName']].First_name = player_info['playerName']
        self.Players[player_info['playerName']].Stats['Assists']  = player_info['assists']
        self.Players[player_info['playerName']].Stats['Goals']  = player_info['goals']
        self.Players[player_info['playerName']].Stats['PMC']  = player_info['plusMinusCount']
        self.Players[player_info['playerName']].Stats['Drops']  = player_info['drops']
        self.Players[player_info['playerName']].Stats['Throwaways']  = player_info['throwaways']
        self.Players[player_info['playerName']].Stats['Ds'] = player_info['ds']
        # Check the ultimate-numbers server to see if they have a player number
        # that matches this player. 
        self.add_player_number(self.Players[player_info['playerName']])

    def add_player_number(self,player_class):
        """
        Grabs a different player info endpoint from the ultimate-numbers server
        to match player numbers to name
        """
        # Get data from the appropriate ultimate-numbers 
        # endpoint
        base_url = 'http://www.ultimate-numbers.com/rest/view'
        req = urllib2.Request(base_url+"/team/"+str(self.ID)+"/players/")
        response = urllib2.urlopen(req)
        data = json.loads(response.read())
        
        # Check each player in the Team instance for a name that matches
        # a player in this endpoint (by name). If they exist, then add 
        # the player's number to their Player class instance.
        for player in data:
            if player['name'] == player_class.First_name:
               try:
                   player_class.Number = player['number']
               except:
                   print "Could not match player number for", player['name'],
                   print "on the", self.City, self.Name
                   pass
            
    def top_five(self, stat):
        """
        Generates a list of tuples for the a given *stat*. 
        Each tuple contains a player name and value of their 
        statistic. Tuples are sorted before being returned.
        """
        # Make sure the team has the information needed to get
        # the stats 
        if not hasattr(self, "City"): self.get_info()
        if not hasattr(self, "Players"): self.add_players()
        # Establish list of players on the team
        Players = self.Players
        # init sorted stat list
        player_stat_list = []
        # Get the name and stat for each player and add the tuple to the list
        for player in self.Players:
            player_name = Players[player].First_name
            player_stat = Players[player].Stats[stat]
            player_stat_list.append((player_name, player_stat))
        # sort the list of tuples by the stat value
        # reverse=True means sort highest to lowest
        player_stat_list.sort(key= lambda set: int(set[1]), reverse=True)
        # return the top 5 tuples from the list.
        return player_stat_list[0:5]

    
    def roster(self):
        """
        Generates a tuple for each player in the Team.Players dict 
        containing their name and number. 

        Also tacks on a team city and name at the front. 
        """
        # init the list of return info
        # Add the city and name as the first entry
        if not hasattr(self, 'City'): self.get_info()
        rost = []
        # Loop through players, create tuple and add to list
        for player in self.Players: 
            p = self.Players[player]
            if "Anon" not in p.First_name:
                rost.append((p.First_name,p.Number))
        # sort the list by player number
        rost.sort(key=lambda set: int(set[1]))
        rost=[(self.City, self.Name, self.ID)]+rost 
        # return the list
        return rost

    def add_games(self, filename="2014_AUDL_Schedule.json"):
        """
        Adds any games for the team from a given file containing the League
        or team schedule for the current season.
        """
        # create a name that will match one in the json doc
        AUDL_Name = self.City + " " + self.Name

        # open the json schedule doc
        schedule = open(filename, 'r')
        # convert the file data into a python object
        data = json.loads(schedule.read())
        self.Games={}
 
        team_games = []
        # if the game belongs to the current team, add it
        # to a list of essential game data
        for game in data:
            if AUDL_Name in game['team']:
                d = game['date']
                t = game['time']
                y = game['Year']
                opp = game['opponent']
                if game['home/away'] == 'Home':
                    ht = game['team'].rstrip()
                    ht_ID = self.League.name_to_id(ht)
                    at = game['opponent'].rstrip()
                    at_ID = self.League.name_to_id(at)
                else:
                    at = game['team'].rstrip()
                    at_ID = self.League.name_to_id(at)
                    ht = game['opponent'].rstrip()
                    ht_ID = self.League.name_to_id(ht)
                team_games.append((d,t,y,ht,ht_ID,at,at_ID,opp))

        #Check to see if the team belongs to a league
        if self.League != None:
            # If yes, check to see if this game already exists
            # in the league
            for game in team_games:
                
                exists,existing_game = self.League.league_game_exist(game[-1], game[0])
                self.Games[game[0]] = existing_game if exists else Game(game[0],game[1],game[2],game[3],game[4],game[5],game[6])
        # If no, then just add a new game class for this team.
        else: 
            for game in team_games:
                self.Games[game[0]] = Game(game[0],game[1],game[2],game[3],game[4])
            
        
                #self.Games[game['date']] = Game(d,t,y,ht,at)
    def populate_team_stats(self):
       """
       Gets the top five players for each stat in stat_list (hardcoded)
       and returns the players and their corresponding values into a tuple. 

       Tuples are appended into a list and returned to the Team class's 
       Top_Fives attribute.
       """
       if not hasattr(self,"Players"): self.add_players()
       stat_list=["Goals","Assists","Drops","Throwaways", "PMC", "Ds"]

       if not hasattr(self, 'City'): self.get_info()
       stat_out = [(self.City, self.Name, self.ID)]
       for stat in stat_list:
           stat_tup = (stat, self.top_five(stat))
           stat_out.append(stat_tup)
       
       # A dictionary containing the top five players for 
       # a given statistic (key) whose value is a tuple
       # containing the name of the player and their 
       # in sorted order. 
       self.Top_Fives = stat_out

    def return_schedule(self): 
        """
        Returns the team's schedule with the team's city+name and ID as the first two
        values of the list. 
        """
        AUDL_Name = self.City+ " " + self.Name

        sched = []
        for game in self.Games:
            if AUDL_Name in self.Games[game].home_team:
                opponent = self.Games[game].away_team
            else:
                opponent = self.Games[game].home_team
            game_tup = (self.Games[game].date, self.Games[game].time, opponent)
            sched.append(game_tup)

        sched.sort(key= lambda set: dt.strptime(set[0], '%m/%d/%y'))
        sched = [AUDL_Name, self.ID ]+sched
        return sched

    def return_scores(self):
        """
        Returns the game scores for all games that belong to the team 
        beginning with entries for the team city and name.
        Includes the Date, Opponent, and Score. 
        """
        # set the Team's games to a shorter variable
        AUDL_Name = self.City+ " " + self.Name
        games = self.Games
        scores_list=[self.City + " " + self.Name]
        for game in games:
            # set game score. if the game hasn't started yet, default to 0-0
            score = '0-0' if games[game].Score == [] else games[game].Score
            # set oppponent name to whichever team doesn't match the team for which we're 
            # returning score info
            opp = games[game].home_team if games[game].away_team == AUDL_Name else games[game].away_team
            # create a tuple for this information
            game_tup = (games[game].date, opp, score)
            # add the tuple to the scores list for the current team
            scores_list.append(game_tup)
        return scores_list

    def game_exist(self, date):
        """
        Returns whether or not the team currently has a game with the input date
        in the form of a boolean. 

        If the game does exist, it will return the game class instance for that date
        """
        if hasattr(self, 'Games'):
            return (True, self.Games[date]) if date in self.Games.keys() else (False, None)
        else:
            return False, None


class Player():
    """
    A class for containing information about a player.
    """
    def __init__(self):
        # A dictionary containing the players stats.
        # Keys: stat names Values: player's statistic 
        self.Stats = {}
        # String containing the player's first name
        self.First_name = ''
        # String containing the player's last name
        self.Last_name = ''
        # Intger of the players number
        self.Number = 0
        # string containing the player's height (in ft. & in.)
        self.Height = ''
        # string containing the player's weight (in lbs) 
        self.Weight = ''
        # string containing the player's age
        self.Age = 0

class Game():
    """
    A class for information about a given game in the AUDL
    """
    def __init__(self, date, time, year, home_team, home_team_id, away_team, away_team_id):
        # a string containing a has that uniquely identifies a game on the 
        # ultimate numbers server
        self.ID = ''    
        # a string containing the year of the season
        self.year = year
        # a string containing the date of the game
        self.date = date
        # a string containing a scheduled beginning time of the game
        self.time = time
        # a boolean declaring whether or not a game is over
        self.Finished = False
        # a list containing two tuples. 
        #each tuple contains a team name and their current score
        self.Score = []
        # a string containing the location of the game
        self.Location =''
        # a string containing the name of the away_team
        self.away_team = away_team
        # an int containing the id of the away_team
        self.away_team_id = away_team_id
        # a string containing the name of the home_team
        self.home_team = home_team
        # an int containing the id of the home_team
        self.home_team_id = home_team_id
        # a dictionary containing the home team's leader in a set of stats for this game
        # Keys: Statistic names Values: Tuple of a player name and their statistic
        self.Home_stats = {}
        # a dictionary containing the home team's leader in a set of stats for this game
        # Keys: Statistic names Values: Tuple of a player name and their statistic
        self.Away_stats = {}
        # a dictionary containing information about who scored each goal for each point
        # in the game
        self.Goals = {}
        # an int returning the current quarter 
        self.Quarter = 0

 
        
