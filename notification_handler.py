import csv
from apns import APNs, Frame, Payload
from datetime import datetime as dt
from datetime import timedelta

import boto.dynamodb2
from boto.dynamodb2.table import Table
from boto.dynamodb2.items import Item

token_hex = '0d4a8842d98d949225f1aeba1782604a8ae6fd9397c448c18ee52cf78933e368'
ios_table = "ios_device_tokens"

def register_ios_token(path_entities):
    print("Registering ios token...")
    token = path_entities[-1]
    #determine what type of notification is being registered
    if "general" in path_entities:
        register_token(ios_table,"general",token)
    else:
        abbreviation = path_entities[-2]
        register_token(ios_table,abbreviation,token)
    pass

def register_android_token(path_entities):
    print("Registering Android token...")
    pass

def register_token(table_name, notification_type, token):
    #read our aws key values for access to the server
    reader = csv.reader(open("rootkey.csv",'rb'),delimiter = '=')
    access_key = reader.next()[1]
    secret_key = reader.next()[1]
    #establish a connection to the dynamodb server
    conn = boto.dynamodb2.connect_to_region("us-east-1", aws_access_key_id = access_key, aws_secret_access_key = secret_key)
    #make sure this table exists
    if any(table_name is table for table in conn.list_tables()):
        print("Could not find ios table on db server")
        return False
    token_table = Table(table_name,connection=conn)
    #make sure there is an item for the notification_type in that table
    item_data = { "notification_type" : notification_type, "token" : token }
    token_table.put_item(data=item_data, overwrite = True)
    return True

def get_apns_connection(cert_file = "AUDLCert.pem", key_file = "AUDL.pem"):
    return APNs(use_sandbox=True, cert_file = "AUDLCert.pem", key_file="AUDLnopassword.pem")

def send_notification(message, token = token_hex):
    conn = get_apns_connection()
    conn.gateway_server.send_notification(token, Payload(alert = str(message), sound = 'default', badge = 1), expiry = dt.utcnow() + timedelta(150) )

def send_notifications(message, tokens = [token_hex]):
    for token in tokens:
        send_notification(message, token)
