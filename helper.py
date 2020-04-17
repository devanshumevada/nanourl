from flask import session
from db import db_user, db_links, db_log
from bson import ObjectId
def user_logged_in():
        if 'user' in session:
                return True

def insert_by_key_value(type_,**kwargs):
        data={}
        for key,value in kwargs.items():
                data[key]=value
        if type_=='user':
                user=db_user.insert_one(data)
                return user
        elif type_=='logs':
                log=db_log.insert_one(data)
                return log
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
        else:
                return db_links.find_one(target)

def update_by_key_value(type_,**kwargs):
        data=dict()
        for key,value in kwargs.items():
                if key == 'target':
                        data['target'] = value
                else:
                        data['to_update_data']=value
        
        if type_=='user':
                db_user.update_one(data['target'],{'$set':data['to_update_data']})
        else:
                db_links.update_one(data['target'],{'$set':data['to_update_data']})


def get_current_user():
        return db_user.find_one({'_id':ObjectId(session['user'])})

def get_current_user_links():
        return db_links.find({'user':session['user']})
