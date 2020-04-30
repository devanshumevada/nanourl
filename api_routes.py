import jwt
from app import app
from flask import jsonify, request, render_template
from db import db_links, db_user
from config import SECRET_KEY
from bson import ObjectId
from helper import (get_user_api_token, 
                    get_current_user, 
                    validate_url, 
                    generate_short_code)

# Resource access and creation routes
@app.route('/api/link', methods=['GET','POST'])
def create_or_render_link():
    if 'Authorization' not in request.headers:
            return jsonify({'message':'Authorization token not found in the headers'}), 401
    token = request.headers['Authorization']
    try:
        payload = jwt.decode(token, SECRET_KEY , algorithms=['HS256'])
        if db_user.find({'_id':ObjectId(payload['identity'])}).count()==0:
            return jsonify({'message':'No such registered user'}), 401   
    except:
            return jsonify({'message':'Please Pass in a valid token'}), 401



    if request.method=='POST':
        #Checking if the data in the body is json
        if not request.is_json:
            return jsonify({'message':'Please pass-in the data in the JSON format'}), 400
        content = request.get_json()

        #checking if 'url' is key is present in the json data
        if 'url' not in content or content['url'] is None:
            return jsonify({'message':'"url" parameter not found in the json data'}), 400
        if validate_url(content['url']) is None:
            return jsonify({'message':'Please pass-in a proper valid URL'}), 400
        short_code = generate_short_code()
        db_links.insert_one({'url':content['url'],'short_code':short_code,'count':0,'user':payload['identity']})
        return jsonify({'message':'Resource successfully created','data':{'url':content['url'], 'short_url':'http://www.nanourl.xyz/'+short_code}}),201 


    elif request.method=='GET':
        # Checking if short_code parameter has been passed or not
        if 'short_code' not in request.args or request.args['short_code']=='':
            return jsonify({'message':'short_code parameter either is not passed or is Null'}), 400
        
        # Checking if entry exists in the database
        data = db_links.find_one({'short_code':request.args['short_code'].upper()})
        if data is None:
            return jsonify({'message':'No such shorted URL exists'}),404
        return jsonify({'url':data['url'],'short_url':'http://www.nanourl.xyz/'+data['short_code'], 'usage_count':data['count']})


@app.route('/api/links')
def get_all_links(): 
    if 'Authorization' not in request.headers:
        return jsonify({'message':'Authorization token not found in the headers'}), 401
    token = request.headers['Authorization']
    try:
        payload = jwt.decode(token, SECRET_KEY , algorithms=['HS256'])
        if db_user.find({'_id':ObjectId(payload['identity'])}).count()==0:
            return jsonify({'message':'No such registered user'}), 401
        links = db_links.find({'user':payload['identity']})
        if links.count()==0:
            return jsonify({'message':'This user has not shorted any links'})
        data = []
        for link in links:
            data.append({'url':link['url'],'short_url':'http://www.nanourl.xyz/'+link['short_code'],'usage_count':link['count']})
        return jsonify({'links':data})
    except:
        return jsonify({'message':'Please Pass in a valid token'}), 401
       
    
    
# Api access information page render route
@app.route('/api_access_information')
def api_access_information():
    return render_template('api_access_info.html', token=get_user_api_token().decode('utf-8'), user=get_current_user())
