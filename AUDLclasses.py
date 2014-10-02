#!/usr/bin/python

import urllib2, json
import feedparser as fp
import MediaClasses
from game_info import game_deets
from game_info import gen_game_graph


# Timestamp imports 
from timestamps import game_ts
from datetime import datetime as dt
from datetime import timedelta
from tzlocal import get_localzone

base_url = 'http://www.ultianalytics.com/rest/view'

class League():
    """  
    Class which acts as a central node for all other classes
    on the AUDL server.
    """ 
    def __init__(self):
        # A Video object containing the list of all the videos
        self.Videos = MediaClasses.Videos();
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
        self.Top_fives = { 'Goals': [], 'Assists': [], 'Drops': [], 'Throwaways': [], 'PMC': [], 'Ds': [] }


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
                       # Create the new team class
                       self.Teams[ID] = Team(self, ID, Name, City)
        if not found: print "No Team with that ID on record"
   
        # Gives each team its ID value so it can grab its own information from the server.
        for team in self.Teams:
            if players: self.Teams[team].add_players()
            if games:   self.Teams[team].add_games(), self.Teams[team].get_games_info()
            if stats:   self.Teams[team].add_player_stats()

            if stats:   self.Teams[team].populate_team_stats()
        teams_info.close()

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
                data_out.sort(key= lambda set: set[0])
                data_out.append(new_tup)
        return data_out

    def news_page_info(self):
        """
        Returns information needed to populate the news page in the app UI
        """
        # Init the output list, add a header
        art_list = []
        # shorten the path to the News dictionary
        News = self.News
        # Get the title and article url for every article
        # create a tuple and append to the output lits
        for art in News:
            #Only show the date on the app
            ts = News[art].Timestamp.encode('ascii', 'ignore')
            #Break by spacing
            ts = ts.split(" ")
            # Join only the day, month, year components
            ts = " ".join(ts[1:4])
            art_tup = (News[art].Title, News[art].url, ts)
            art_list.append(art_tup)
        art_list.sort(key = lambda set: dt.strptime(set[2], "%d %b %Y"), reverse = True)
        art_list=["AUDL News"]+art_list
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
        
    def return_games(self, teams=None, days_ahead=14, days_behind=0, scores=False, now=None,all=False):
        """
        Returns any games occurring within 2 weeks of the current date.

        teams - a list of team ids to check for games
        days_ahead - indicates that games beyond this many days ahead of
                today should not be included. Default is two weeks.

        If no teams are passed to the function, return this information
        for all teams in the league
        """
        # type-check of teams var
        if type(teams) is not list and teams != None:
            return []

        data_out = []
        # If no teams are passed in, add all available teams to the schedule
        if teams == None:
            teams = []
            for ID,team in self.Teams.items():
                teams.append(ID)
   
        game_list = []
        #loop through each team and get their game class instances
        for team in teams:
            games = self.Teams[team].Games
            for game in games:
                inst = self.Teams[team].Games[game]                    
                if inst not in game_list: game_list.append(inst)
        
        
        game_list.sort( key = lambda set: dt.strptime(set.date, '%m/%d/%y'))
        
        for game in game_list:
            game_tup = self.game_tuple(game)

            #use the game date to filter games accordingly
            game_date = dt.strptime(game.date, "%m/%d/%y").date()
            now = dt.today().date() if now == None else now
            delta = game_date-now
            if delta.days > days_ahead:
                pass
            elif not all and delta.days < (-1*days_behind):
                pass
            else:
                data_out.append(game_tup) if scores else data_out.append(game_tup[:-4])
       


        #If there's no data out, then return the last few games for now
        if 0 == len(data_out):
            data_out = [ self.game_tuple(game) if scores else self.game_tuple(game)[:-4] for game in game_list[-5:] ]
        return data_out

    def game_tuple(self, g):
        date = g.date
        time = g.time
        team1 = g.home_team
        team1ID = self.name_to_id(g.home_team)
        team2 = g.away_team 
        team2ID = self.name_to_id(g.away_team)
        
        if hasattr(g, 'home_score') and hasattr(g, 'away_score'):
            hscore = g.home_score
            ascore = g.away_score
        else:
            hscore="0"
            ascore="0"  
        status = 0 if not hasattr(g,'status') else g.status

        game_tuple=(team1,team1ID,team2,team2ID,date,time,hscore,ascore,status,g.tstamp.isoformat())

        return game_tuple
            
    def return_schedules(self):
    
        data_out = []
        for div in self.Divisions:
            game_sched = self.return_games(self.Divisions[div],days_ahead=365,days_behind=0,scores=False)
            data_out.append([div,game_sched])
        
        return data_out

    def return_upcoming(self):
        data_out=[]
                
        game_sched = self.return_games(None,days_ahead=365,days_behind=0,scores=True)
        for item in game_sched: 
           # Use the status enumerator to remove any games that have already begun
           # the list method remove is ok to use here as all games should be unique
           if (item[8] != 0): game_sched.remove(item)
        data_out.append(["All Divs",game_sched])

        return data_out
                

    def top_five_league(self, stat):

        top_player_stat_list = []
        #traverse through all teams to get top 5
        for team in self.Teams:
            #should add a team indicator to this tuple
            team_list = self.Teams[team].top_five(stat)
            '''
            here we pop each player off the list and add them 
            back to the list with a team id
            '''
            for player in team_list:
                playerOne = team_list.pop(0)
                team_list.append( ( playerOne[0], playerOne[1], team ) )
            #add each teams list into a total list
            top_player_stat_list = top_player_stat_list + team_list
        #sort from highest to lowest based on stat quantity
        top_player_stat_list.sort( key = lambda set: set[1], reverse=True )
        #returns the top 5 tuples from the list.
        return top_player_stat_list[0:5]

    def get_stats_league(self):
        #dictionary of stats with formal and informal names as [0][1]
        stat_dic = {'goals':["Goals", "goals"], 'assists':["Assists", "assists"], 'drops':["Drops", "drops"],
                    'throwaways':["Throwaways", "throwaways"], 'plusMinusCount':["PMC", "plusMinusCount"],
                    'ds':["Ds", "ds"]}
        stat_list = [ 'goals', 'assists', 'drops', 'throwaways', 'plusMinusCount', 'ds' ]
        '''
        dummy dict in order to capture the latest top 5's and update the class
        dict with this dummy dict
        '''
        top_fivez = { 'Goals': [], 'Assists': [], 'Drops': [], 'Throwaways': [], 'PMC': [], 'Ds': [] }
        for stat in stat_list:
            formal = stat_dic[stat][0]
            informal = stat_dic[stat][1]
            top_fivez[formal] = self.top_five_league( informal ) 
        self.Top_fives.update(top_fivez)
        
    def get_top_fives(self):
        self.get_stats_league()
        return self.Top_fives

    def get_videos(self):

        '''
        check timestamp to see how out of date we are...currently not implemented
        pseudocode
            check current timestamp to last video class timestamp 
            (timestamp updated only when videos are refreshed, not when accessed)
            
            if time elapsed is greater than some amount of time:
                run a refresh method on vids class
                return refreshed list

            else return our stored list
        
        '''
        return self.Videos.videos

    def name_to_id(self, name):
        """
        Loops through each team to look for a matching name. 
        If one is found, then the id is returned as an int.
        """
 
        #loop through teams and find a match:
        teams = self.Teams

        # Corner case for the Royal
        for ID, team_inst in teams.items():
            AUDL_name = team_inst.City + " " + team_inst.Name
            if AUDL_name in name.rstrip(): return ID
        # false case is a corner case until 2014 games begin
        return 0

    def return_scores_page(self):       
        
        data_out = []
        for div in self.Divisions:
            game_scores = self.return_games(self.Divisions[div],days_ahead=365,days_behind=7,scores=True)
            data_out.append([div,game_scores])
        return data_out

    def standings(self):
       
        standings_list=[]
        for div,teams in self.Divisions.items():
            div_list=[]
            #print teams
            for team in teams:
                t = self.Teams[team]
                rec = t.record()
                team_rec_tup = (t.full_name(),team,rec[0], rec[1], rec[2])
                div_list.append(team_rec_tup)
            div_list.sort(key= lambda set: (float(set[2])/(float(set[2]+set[3])),set[4]), reverse=True)
            div_list.insert(0,div)
            standings_list.append(div_list)

        return standings_list

    def web_standings(self):
       
        standings_dict={}
        for div,teams in self.Divisions.items():
            div_list=[]

            #print teams
            for team in teams:
                t = self.Teams[team]
                rec = t.record()
                team_rec_dict = {"name" : t.full_name(), "id": team, "wins" : rec[0], "losses" : rec[1], "plmn" : rec[2]}
                div_list.append(team_rec_dict)
            div_list.sort(key= lambda set: (float(set["wins"])/(float(set["wins"]+set["losses"])),set["plmn"]), reverse=True)
            #div_list.insert(0,div)
            
            standings_dict[div] = div_list
            

        return standings_dict


    def update_games(self):
        for name,team in self.Teams.items():
            team.get_games_info()

class Team():
    """
    This class keeps all of the statistical information 
    for a given team in the league. (player info, statistics,
    game schedules, etc.)
    """
    def __init__(self, League, ID, Name, City):
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
        
    def add_players(self, filename='2014_players.json',stats=True):
        """
        Adds players to the Team class attribute 'Players' from the json file.
        """

        # A dictionary containing a set of Player class
        # instances pertaining to this team.
        self.Players = {}

        # open the json file
        f = open(filename, 'r')

        players= json.load(f)

        for player in players:
            if self.full_name() in player['Team']:
                fn = player['Player First Name'].strip()
                ln = player['Player Last Name'].strip()
                num = str(player['Jersey #'])
                full_name = fn + " " + ln
                #case for for a player number of 0
                # UN players will have "00" as their number on the site
                if num == "0": num = "00"
                self.Players[full_name]=Player(fn,ln,num)
        f.close()

    def add_player_stats(self):
        """
        Adds player name, number, stats, etc. to a player class. 

        Assumes the ultimate-numbers info has already been loaded.
        """

        # get player summary data

        req1 = urllib2.Request(base_url+"/team/"+str(self.ID)+"/players/")
        # print base_url+"/team/"+str(self.ID)+"/players/"
        response1 = urllib2.urlopen(req1)
        gen_player_data = json.loads(response1.read())

        # get player stat data
        req2 = urllib2.Request(base_url+"/team/"+str(self.ID)+"/stats/player")
        response2 = urllib2.urlopen(req2)
        player_stats_data = json.loads(response2.read())
        
        # match player to their Ultimate-Numbers name by their Jersey number
        for name, player in self.Players.items():
            for data in gen_player_data:
                #print data['number'], player.Number, self.Name, player.full_name()
                if 'number' not in data.keys():
                    continue
                if data['number'] == player.Number:
                    #print data['name']
                    self.Players[name].stat_name = data['name']

        stats = ["assists","goals","plusMinusCount","drops","throwaways","ds"]
        for name,player in self.Players.items():
           for player_stats in player_stats_data:
               if  hasattr(player,'stat_name') and player_stats['playerName'] == player.stat_name:
                   for stat in stats:
                       player.Stats[stat]  = player_stats[stat] if stat in player_stats else 0

    def add_player_number(self,player_class):
        """
        Grabs a different player info endpoint from the ultimate-numbers server
        to match player numbers to name
        """
        # Get data from the appropriate ultimate-numbers 
        # endpoint

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
            player_name = Players[player].full_name()
            player_stat = Players[player].Stats[stat] if stat in Players[player].Stats.keys() else 0
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
                num = str(p.Number) if int(p.Number) != 0 else "00"
                rost.append((p.First_name + " "+ p.Last_name,num))
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
                tstamp = game_ts(d,t)
                opp = game['opponent']
                #debug stuff
                #if game['team'].strip() == "San Jose Spiders": print opp, game['team'], d
                #if opp.strip() == "San Jose Spiders": print opp, game['team'], d
                if game['home/away'] == 'Home':
                    ht = game['team'].strip()
                    at = game['opponent'].strip()
                  
                else:
                    at = game['team'].strip()
                    ht = game['opponent'].strip()
                  
                team_games.append((d,t,tstamp,ht,at,opp))

        #Check to see if the team belongs to a league
        if self.League != None:
            # If yes, check to see if this game already exists
            # in the league
            for game in team_games:
                
                exists,existing_game = self.League.league_game_exist(game[-1], game[0])
                self.Games[game[0]] = existing_game if exists else Game(game[0],game[1],game[2],game[3],game[4])
        # If no, then just add a new game class for this team.
        else: 
            for game in team_games:
                self.Games[game[0]] = Game(game[0],game[1],game[2],game[3],game[4])
            
        
                #self.Games[game['date']] = Game(d,t,y,ht,at)
        schedule.close()

    def populate_team_stats(self):
       """
       Gets the top five players for each stat in stat_list (hardcoded)
       and returns the players and their corresponding values into a tuple. 

       Tuples are appended into a list and returned to the Team class's 
       Top_Fives attribute.
       """
       if not hasattr(self,"Players"): self.add_players()
       stat_list = ["goals","assists","drops","throwaways","plusMinusCount","ds"]
       formal_stat_list = ["Goals","Assists","Drops","Throwaways","+/- Count","Ds"]
       if not hasattr(self, 'City'): self.get_info()
       stat_out = [(self.City, self.Name, self.ID)]
       for i in range(6):
           stat_tup = (formal_stat_list[i], self.top_five(stat_list[i]))
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
            game_tup = (self.Games[game].date, self.Games[game].time, opponent, self.League.name_to_id(opponent))
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
        scores_list = []
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
        scores_list.sort(key = lambda set: dt.strptime(set[0], '%m/%d/%y'))
        scores_list=[self.City + " " + self.Name]+scores_list
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

    def record(self):

        if not hasattr(self,'Games'): return None
        wins = 0
        losses = 0
        point_diff = 0
        #Loop through games and count wins/losses
        games = self.Games
        for key,game in games.items():
            if hasattr(game, 'home_score') and hasattr(game, 'away_score'):
                game_diff = game.home_score-game.away_score
                if self.full_name() in game.home_team:
                   wins = wins+1 if game.home_score > game.away_score else wins
                   losses = losses+1 if game.home_score < game.away_score else losses
                   point_diff = point_diff + game_diff
                else:
                   wins = wins+1 if game.home_score < game.away_score else wins
                   losses = losses+1 if game.home_score > game.away_score else losses
                   point_diff = point_diff - game_diff
        return (wins,losses,point_diff)
 
    def full_name(self):

        return self.City + " " + self.Name

    def get_games_info(self):

        #get the list of games for the team from ultimate-numbers


        full_url = base_url + "/team/" + str(self.ID) + "/games"

        req = urllib2.Request(full_url)

        response = urllib2.urlopen(req)

        data = json.loads(response.read())

        games = self.Games

        for game in games:
            if self.full_name() in games[game].home_team:
               games[game].match_game(data, True)
            elif self.full_name() in games[game].away_team:
               games[game].match_game(data, False)
            else:
               print "GAME DOESN'T BELONG TO THIS TEAM"



class Player():
    """
    A class for containing information about a player.
    """
    def __init__(self,first_name,last_name,number):
        # A dictionary containing the players stats.
        # Keys: stat names Values: player's statistic 
        self.Stats = {}
        # String containing the player's first name
        self.First_name = first_name
        # String containing the player's last name
        self.Last_name = last_name
        # Intger of the players number
        self.Number = number
        # string containing the player's height (in ft. & in.)
        self.Height = ''
        # string containing the player's weight (in lbs) 
        self.Weight = ''
        # string containing the player's age
        self.Age = 0

    def full_name(self):
        """
        Returns the concatenated first and last name of the player.
        """
        return self.First_name + " " + self.Last_name

class Game():
    """
    A class for information about a given game in the AUDL
    """
    def __init__(self, date, time, tstamp, home_team, away_team):
        # a string containing a has that uniquely identifies a game on the 
        # ultimate numbers server
        #self.home_id = ''    
        #self.away_id = ''
        # a datetime object for the game
        self.tstamp = tstamp
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
        # a string containing the name of the home_team
        self.home_team = home_team
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

    def match_game(self, games_dict, home):
        
        game_date = dt.strptime(self.date, "%m/%d/%y")

        for game in games_dict:
            if "timestamp" in game.keys():
                dict_date = dt.strptime(game['timestamp'][:10], "%Y-%m-%d")
                tstamp = game['timestamp']
                new_game = False if hasattr(self,"home_score") or hasattr(self,"away_score") else True
                higher_score = True if new_game or ((self.home_score+self.away_score)<(game['ours']+game['theirs'])) else False
                if (game_date.date()-dict_date.date()) == timedelta(days = 0):
                    if home: 
                        self.home_id = game['teamId']+"/game/"+game['gameId'] 
                    else:
                        self.away_id = game['teamId']+"/game/"+game['gameId']
                    self.timestamp = tstamp
                    if new_game or higher_score:
                        self.home_score = game['ours'] if home else game['theirs']
                        self.away_score = game['theirs'] if home else game['ours']
                    # a string containing a has that uniquely identifies a game on the 
                    # ultimate numbers server
                    
            else:
                pass
        self.set_status()

    def set_status(self):
        """
        This will set the game's status based on the timestamp of the game. 
        Uses the local time on the server for comparison.
        """      
        # create class enum for different allowed statuses
        class statuses:
            UPCOMING = 0 
            ONGOING = 1
            OVER = 2
            # ultimate-numbers declared over
            UN_DEC_OVER =3

        # the string to be sent for a notification
        #note_str = None
        #generate local timestamp w/ timezone
        tz = get_localzone()
        now = tz.localize(dt.now())
        # maximum assumed game length, in hours (this is arbitrary)
        max_game_len = 6
        if not hasattr(self,'status') or (hasattr(self,'tstamp') and self.status != statuses.UN_DEC_OVER):
            delta_hours = (now-self.tstamp).total_seconds()/3600
            sched_date = self.tstamp.date()
        
            if  (now.date()==self.tstamp.date())  and (delta_hours) < 0:
                self.status=statuses.UPCOMING
            elif (now.date()==self.tstamp.date())  and (delta_hours) <= max_game_len:
                #if hasattr(self,'status') and self.status == statuses.UPCOMING: 
                #    note_str = self.home_team +  " vs. " + self.away_team + " has begun!"
                self.status=statuses.ONGOING
            elif (now.date()-self.tstamp.date()) > timedelta(days=0):
                #if hasattr(self,'status') and self.status == statuses.ONGOING: 
                #    note_str = "GAME OVER: " + self.home_team + " " + str(self.home_score) + ", " + self.away_team + " " + str(self.away_score)
                self.status=statuses.OVER
            elif (now.date()==self.tstamp.date()) and (delta_hours) > max_game_len:
                #if hasattr(self,'status') and self.status == statuses.ONGOING:
                    #if not hasattr(self,"home_score"): 
                    #    note_str =  "GAME OVER: " + self.home_team + " vs. " + self.away_team + ". No score reported!"
                    #else:
                    #    note_str = "GAME OVER: " + self.home_team + " " + str(self.home_score) + ", " + self.away_team + " " +str(self.away_score)
                self.status=statuses.OVER
            else:
                self.status=statuses.UPCOMING
        else:
            pass
        # This is where we will actually send the notification
        #if note_str != None: print note_str
        #return note_str

    def stat_info(self):
        # a flag indicating whether or not the game graph was generated using home_team data
        graphed = False
        # a flag to be set by game_deets on whether or not the game has been declared over by UN
        is_over = False
        # Blank data in case there's no game info
        home_deets = [('Goals','N/A',0),('Assists','N/A',0),('Drops','N/A',0),('Throwaways','N/A',0),('Ds','N/A',0)]        
        away_deets = [('Goals','N/A',0),('Assists','N/A',0),('Drops','N/A',0),('Throwaways','N/A',0),('Ds','N/A',0)]        
        #If there's a home_id, open the UN endpoint and generate data
        if hasattr(self, 'home_id'):
            full_url = base_url + "/team/" + self.home_id
            #print full_url
            req = urllib2.Request(full_url)
            response = urllib2.urlopen(req)
            data = json.loads(response.read())
            if 'pointsJson' in data.keys():
                points = json.loads(data['pointsJson'])
                home_deets,is_over = game_deets(points)         
                self.graph_pnts = gen_game_graph(self,points)
                graphed = True
            else:
                print ["No information available"]
        #open home_team endpoint and read json
        #home_info=game_deets(home_team_endpoint)
        #Use the home_info to generate the game_graph
        #game_graph(home_team_endpoint)
        #If there's an away page, open the UN endpoint and generate data
        #open away_team endpoint and read json
        #away_info=game_deets(away_team_info)

        if hasattr(self, 'away_id'):
            full_url = base_url + "/team/" + self.away_id
            #print full_url
            req = urllib2.Request(full_url)
            response = urllib2.urlopen(req)
            data = json.loads(response.read())
            if 'pointsJson' in data.keys():
                points = json.loads(data['pointsJson'])
                away_deets, is_over = game_deets(points)         
                if not graphed: self.graph_pnts=gen_game_graph(self,points,flip=True)
            else:
                print ["No information available"]
        #print home_deets
        #print away_deets
        if is_over: self.status=3
        return [home_deets,away_deets]
