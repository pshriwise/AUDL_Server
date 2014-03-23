#!/usr/bin/python 

def AUDLlogo(team_name):
    
    icon_dict = { 'AlleyCats' : "team_alleycats_on.png",
                  'Breeze' : "team_breeze_on.png", 
                  'Dragons' : "team_dragons_on.png", 
                  'Empire' : "team_empire_on.png", 
                  'Flamethrowers' : "team_flamethrowers_on.png", 
                  'Lions' : "team_lions_on.png", 
                  'Mechanix' : "team_mechanix_on.png",
                  'Phoenix' : "team_phoenix_on.png",
                  'Radicals' : "team_radicals_on.png",
                  'Raptors' : "team_raptors_on.png", 
                  'Revolutuion' : "team_revolution_on.png", 
                  'Riptide' : "team_riptide_on.png", 
                  'Royal' : "team_royal_on.png", 
                  'Rush' : "team_rush_on.png", 
                  'Spiders' : "team_spiders_on.png", 
                  'Wildfire' : "team_wildfire_on.png", 
                  'Wind Chill' : "team_windchill_on.png"
                }

    if team_name in icon_dict.keys():
        f = open("Logos/"+icon_dict[team_name], 'r')
        return f.read()
    else:
        return "Not a valid team name"

