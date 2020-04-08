#all the routes that are related to operation on links
from app import app
from flask import request, redirect, url_for, render_template, session
from helper import user_logged_in
from check_url import validate_url
from db import db_links, db_user
from generate_short_url_code import generate_short_code
from bson import ObjectId

@app.route('/shorten_url', methods=['POST','GET'])
def shorten_url():
        #Access only if authenticated
        if user_logged_in():
                if request.method=='POST':
                        url = request.form['url']
                        if validate_url(url) is None:
                                return redirect(url_for('dashboard',url_not_valid=True))
                        short_code = generate_short_code()
                        db_links.insert_one({'url':url,'short_code':short_code,'user':session['user'],'count':0})
                        return redirect('/')
                #On getting a GET request
                return redirect('/')
        return redirect('/login')


@app.route('/<string:id>/delete')
def delete_short_url(id):
        if user_logged_in():
                if request.method=='GET':
                        db_links.delete_one({'_id':ObjectId(id)})
                        return redirect('/')
        return redirect('/login')


@app.route('/<string:short_code>')
def increment_and_go(short_code):
        url_document = db_links.find_one({'short_code':short_code})
        if  url_document is None:
                return '<h4>Not a valid short URL. Please log-in to your account to get a list'
        db_links.update_one({'short_code':short_code},{'$inc':{'count':1}})
        return redirect(url_document['url'])