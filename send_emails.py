from config import SEND_GRID_API_KEY, SEND_GRID_API_LINK, SEND_GRID_API_HEADERS
import requests
import json

def send_account_verification_email(user_email,user_id):
    data = json.dumps({"personalizations": [{"to": [{"email": user_email}]}],"from": {"email": "verify_nanourl@nanourl.xyz"},"subject": "Please verify your user account","content": [{"type": "text/plain", "value": "Please verify your email by going to http://www.nanourl.xyz/"+user_id+"/verify"}]})
    requests.post(url=SEND_GRID_API_LINK, data=data, headers=SEND_GRID_API_HEADERS)

def send_forgot_password_instructions_email(user_email, token):
        data = json.dumps({"personalizations": [{"to": [{"email": user_email}]}],"from": {"email": "forgot_password@nanourl.xyz"},"subject": "Password reset instructions","content": [{"type": "text/plain", "value": "Please go this link to reset your password: http://www.nanourl.xyz/"+token+"/reset_password"}]})
        requests.post(url=SEND_GRID_API_LINK, data=data, headers=SEND_GRID_API_HEADERS)

    

    