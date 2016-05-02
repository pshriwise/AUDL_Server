#!/usr/bin/python

import AUDLclasses
import sheet_reader as sr
import MediaClasses
import argparse
import threading
import traceback
import pickle

# Initialize the league class
AUDL = AUDLclasses.League()

# Set default value for the refreshing interval
poll_interval = 600

# Add teams from local files and populate
# their information from the ultimate-numbers 
# server
sr.get_csv( sr.spreadsheet_key, sr.Team_Info_gid, sr.Team_Info_Filename )
sr.get_csv( sr.spreadsheet_key, sr.Schedule_gid, sr.Schedule_Filename )
sr.get_csv( sr.spreadsheet_key, sr.Rosters_gid, sr.Rosters_filename )

def parse_args():
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--refresh-int', dest= 'interval', required=False, type=int, default=600)

    return parser.parse_args()


def refresh():
    print "refreshing server...",
    try: AUDL.update_games() 
    except: traceback.print_exc()
    try: AUDL.get_news() 
    except: traceback.print_exc()
    try: AUDL.update_videos();
    except: traceback.print_exc()

    sr.get_csv( sr.spreadsheet_key, sr.Team_Info_gid, sr.Team_Info_Filename )
    sr.get_csv( sr.spreadsheet_key, sr.Schedule_gid, sr.Schedule_Filename )
    sr.get_csv( sr.spreadsheet_key, sr.Rosters_gid, sr.Rosters_filename )
    for ID,team in AUDL.Teams.items():
        try:
            team.add_player_stats()
            team.populate_team_stats()
        except: 
            traceback.print_exc()

    print "done"
    threading.Timer(poll_interval,refresh).start()
    print "Number of requests: ", AUDLclasses.requests
    print "Next server update will occur in ", poll_interval, " seconds."


def main():
    #Initial operations for the database
    AUDL.add_teams()
    AUDL.update_games()
    # Get news articles for the team
    AUDL.get_news()
    #Start the refreshing process
    refresh()
    #Allow notifications after the initialization and first update are complete
    AUDLclasses.notify = True    

if __name__ == "__main__":
    main()
