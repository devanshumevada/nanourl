from config import SEND_GRID_API_KEY
import requests
import json

def send_account_verification_email(user_email,user_id):
    data = json.dumps({"personalizations": [{"to": [{"email": user_email}]}],"from": {"email": "verify_nanourl@nanourl.xyz"},"subject": "Please verify your user account","content": [{"type": "text/plain", "value": "Please verify your email by going to http://127.0.0.1:5000/"+user_id+"/verify"}]})
    print(data)
    requests.post(url='https://api.sendgrid.com/v3/mail/send', data=data, headers={'Content-Type':'application/json', 'Authorization':'Bearer '+SEND_GRID_API_KEY})

    