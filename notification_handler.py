import csv
from apns import APNs, Frame, Payload
from datetime import datetime as dt
from datetime import timedelta

import boto.dynamodb2
from boto.dynamodb2.table import Table
from boto.dynamodb2.items import Item

token_hex = '0d4a8842d98d949225f1aeba1782604a8ae6fd9397c448c18ee52cf78933e368'
ios_table = "ios_device_tokens"

def dynamo_connection():
    #read our aws key values for access to the server
    reader = csv.reader(open("rootkey.csv",'rb'),delimiter = '=')
    access_key = reader.next()[1]
    secret_key = reader.next()[1]
    #establish a connection to the dynamodb server
    return boto.dynamodb2.connect_to_region("us-east-1", aws_access_key_id = access_key, aws_secret_access_key = secret_key)

def ios_token_table():
    conn = dynamo_connection()
    if ios_table not in conn.list_tables()['TableNames']:
        print "ERROR: Could not retrieve the ios device token table."
        return
    return Table(ios_table, connection = conn)

def register_ios_token(path_entities):
    print("Registering ios token...")
    token = path_entities[-1]
    #determine what type of notification is being registered
    if "general" in path_entities:
        register_general_ios_token(token)
    else:
        abbreviation = path_entities[-2]
        register_team_ios_token(abbreviation,token)
    pass

def register_android_token(path_entities):
    print("Registering Android token...")
    pass


def register_team_token(table_name, abbreviation, token):
  #setup a dynamo db connection                                                                                                                                                    
    conn = dynamo_connection()
    #make sure this table exists                                                                                                                                                     
    if any(table_name is table for table in conn.list_tables()):
        print("Could not find ios table on db server")
        return False
    token_table = Table(table_name,connection=conn)
    #make sure there is an item for the notification_type in that table                                                                                                             

    #get any abbreviation items with this token and
    token_items = list(token_table.scan(token__eq = token))
    items_to_remove = []
    for item in token_items:
        if item["notification_type"] != "general":
            items_to_remove.append(item)

    if len(items_to_remove) > 1 : print "Warning: Had to remove more than one previously existing team based entry for this token:" , token
    [token_table.delete_item(notification_type=item['notification_type'],token=item['token']) for item in items_to_remove]
    if validate_token(token):
        item_data = { "notification_type" : abbreviation, "token" : token }
        token_table.put_item(data=item_data, overwrite = True)
        return True
    else:
        print("Invalid token. Not adding to table.")
        return False

def register_team_ios_token(abbrev, token):
    register_team_token(ios_table,abbrev,token)

def register_general_ios_token(token):
    register_general_token(ios_table, token)


def register_general_token(table_name, token):
    #setup a dynamo db connection
    conn = dynamo_connection()
    #make sure this table exists
    if any(table_name is table for table in conn.list_tables()):
        print("Could not find ios table on db server")
        return False
    token_table = Table(table_name,connection=conn)
    #make sure there is an item for the notification_type in that table
    if validate_token(token):
        register_token(token_table,"general",token) 
        return True
    else:
        print("Invalid token. Not adding to table.")
        return False

def register_token(table, notification_type, token):
    #create data item and put into the table
    item_data = { "notification_type" : notification_type, "token" : token }
    table.put_item(data=item_data, overwrite = True)
    
def validate_token(token):
    try:
        int(token,16)
        return True
    except:
        return False

def send_general_notification(message):
    send_ios_general_notification(message)

def send_ios_general_notification(message):
    ios_device_table = ios_token_table()
    items = list(ios_device_table.query(notification_type__eq = 'general'))
    tokens = [item['token'] for item in items]
    send_ios_notifications(message, tokens)

def send_ios_team_notification(team_abbrev,message):
    ios_device_table = ios_token_table()
    items = list(ios_device_table.query(notification_type__eq = team_abbrev))
    tokens = [item['token'] for item in items]
    send_ios_notifications(message, tokens)

def get_apns_connection(cert_file = "AUDLCert.pem", key_file = "AUDL.pem"):
    return APNs(use_sandbox=True, cert_file = "AUDLCert.pem", key_file="AUDLnopassword.pem")

def send_ios_notification(message, token = token_hex):
    conn = get_apns_connection()
    conn.gateway_server.send_notification(token, Payload(alert = str(message), sound = 'default'), expiry = dt.utcnow() + timedelta(150) )

def send_ios_notifications(message, tokens = [token_hex]):
    for token in tokens:
        send_ios_notification(message, token)
