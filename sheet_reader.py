

from subprocess import call 
import csv


base_url = 'https://docs.google.com/spreadsheets/d/'

spreadsheet_key = '1Qkup3uHxKgsuLgOJQ-L9S-YoTa5zNp3mu4SPk9abvKY'

Team_Info_gid = '1015881045'

Team_Info_filename =  'Team_Info.csv'


def get_csv_reader( gid, filename):

    #get the csv of the sheet
    call(["wget" , '-O' , filename, base_url+spreadsheet_key+ '/export?format=csv&gid=' + gid])

    #open the csv file

    file = open(filename, 'rb')

    return file

def get_Team_Info_csv_file():
    
    return get_csv_reader( Team_Info_gid, Team_Info_filename)

def id_to_abbrev(file, team_id):
    
    reader = csv.reader(file, delimiter=',')

    for row in reader:
        if str(team_id) == row[2] :
            file.seek(0)
            return row[3]

def name_to_abbrev(file, team_name):

    reader = csv.reader(file, delimiter=',')

    for row in reader:
        if str(team_name) == row[0] :
            file.seek(0)
            return row[3]
