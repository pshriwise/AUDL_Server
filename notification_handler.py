
from apns import APNs, Frame, Payload
from datetime import datetime as dt
from datetime import timedelta

token_hex = '0d4a8842d98d949225f1aeba1782604a8ae6fd9397c448c18ee52cf78933e368'

def register_ios_token(path_entities):
    print("Registering ios token...")
    pass

def register_android_token(path_entities):
    print("Registering Android token...")
    pass


def get_apns_connection(cert_file = "AUDLCert.pem", key_file = "AUDL.pem"):
    return APNs(use_sandbox=True, cert_file = "AUDLCert.pem", key_file="AUDLnopassword.pem")

def send_notification(message, token = token_hex):
    conn = get_apns_connection()
    conn.gateway_server.send_notification(token, Payload(alert = str(message), sound = 'default', badge = 1), expiry = dt.utcnow() + timedelta(150) )

def send_notifications(message, tokens = [token_hex]):
    for token in tokens:
        send_notification(message, token)
