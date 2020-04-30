from flask import session
from db import db_user, db_links, db_log, db_token
from bson import ObjectId
import secrets
import re
import string
from config import (SEND_GRID_API_KEY, 
                    SEND_GRID_API_LINK, 
                    SEND_GRID_API_HEADERS,
                    SECRET_KEY)
import requests
import json
import jwt

url_re = "^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$"
password_re = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"

# user helper functions
def user_logged_in():
        if 'user' in session:
                return True

def get_current_user():
        return db_user.find_one({'_id':ObjectId(session['user'])})

def get_current_user_links():
        return db_links.find({'user':session['user']})

def generate_forgot_password_token():
        return secrets.token_hex(12)

def check_password(password):
        return re.match(password_re, password)


# Database helper functions
def insert_by_key_value(type_,**kwargs):
        data={}
        for key,value in kwargs.items():
                data[key]=value
        if type_=='user':
                return db_user.insert_one(data)
        elif type_=='logs':
                db_log.insert_one(data)
        elif type_=='tokens':
                db_token.insert_one(data)     
        else:
                link=db_links.insert_one(data)
                return link

def find_by_key_value(type_,**kwargs):
        target=dict()
        for key,value in kwargs.items():
                target[key]=value
        if type_=='user':
                return db_user.find_one(target)
        elif type_=='logs':
                return db_log.find_one(target)
        elif type_=='tokens':
                return db_token.find_one(target)
        else:
                return db_links.find_one(target)

def update_by_key_value(type_,target,to_update_data):
        if type_=='user':
                db_user.update_one(target,{'$set':to_update_data})
        else:
                db_links.update_one(target,{'$set':to_update_data})



# URL/Link helper functions
def validate_url(url):
        return re.match(url_re,url)

def generate_short_code():
        return str(''.join(secrets.choice(string.ascii_uppercase + string.digits) for i in range(6)))



# Email helper functions
def send_account_verification_email(user_email,user_id):
        data = json.dumps({"personalizations": [{"to": [{"email": user_email}]}],"from": {"email": "verify_nanourl@nanourl.xyz"},"subject": "Please verify your user account","content": [{"type": "text/plain", "value": "Please verify your email by going to http://www.nanourl.xyz/"+user_id+"/verify"}]})
        requests.post(url=SEND_GRID_API_LINK, data=data, headers=SEND_GRID_API_HEADERS)

def send_forgot_password_instructions_email(user_email, token):
        data = json.dumps({"personalizations": [{"to": [{"email": user_email}]}],"from": {"email": "forgot_password@nanourl.xyz"},"subject": "Password reset instructions","content": [{"type": "text/plain", "value": "Please go this link to reset your password: http://www.nanourl.xyz/"+token+"/reset_password"}]})
        requests.post(url=SEND_GRID_API_LINK, data=data, headers=SEND_GRID_API_HEADERS)


# Api helper functions
def get_user_api_token():
        return jwt.encode({'identity':session['user']},SECRET_KEY, algorithm='HS256')

