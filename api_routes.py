import jwt
from app import app
from flask import jsonify, request
from db import db_links, db_user
from config import SECRET_KEY
from bson import ObjectId


@app.route('/api/link', methods=['GET','POST'])
def create_or_render_link():
    if request.method=='POST':
        pass
    elif request.method=='GET':
        pass

@app.route('/api/links')
def get_all_links(): 
    if 'Authorization' not in request.headers:
        return jsonify({'message':'Authorization token not found in the headers'})
    token = request.headers['Authorization']
    try:
        payload = jwt.decode(token, 'devanshu', algorithms=['HS256'])
        links = db_links.find({'user':payload['identity']})
        if links.count()==0:
            return jsonify({'message':'This user has not shorted any links'})
        data = []
        for link in links:
            data.append({'url':link['url'],'short_url':'http://www.nanourl.xyz/'+link['short_code'],'usage_count':link['count']})
        return jsonify({'links':data})
    except:
        return {'message':'Please Pass in a valid token'}
       
    
    

