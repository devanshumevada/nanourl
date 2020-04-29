from app import app
from flask import (request, 
                   redirect, 
                   url_for, 
                   render_template, 
                   session)
from helper import (user_logged_in,
                    insert_by_key_value, 
                    find_by_key_value, 
                    get_current_user, 
                    validate_url,
                    generate_short_code)
from db import db_links, db_user, db_log
from bson import ObjectId
from datetime import datetime

@app.route('/shorten_url', methods=['POST','GET'])
def shorten_url():
        #Access only if authenticated
        if user_logged_in():
                if request.method=='POST':
                        url = request.form['url']
                        if validate_url(url) is None:
                                return redirect(url_for('dashboard',url_not_valid=True))
                        short_code = generate_short_code()
                        insert_by_key_value('links',url=url,short_code=short_code,user=session['user'],count=0)
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
        return redirect('/dashboard')


@app.route('/<string:short_code>')
def increment_go_and_log(short_code):
        url_document = find_by_key_value('links',short_code=short_code)
        if  url_document is None:
                return '<h4>Not a valid short URL. Please log-in to your account to get a list'
        db_links.update_one({'short_code':short_code},{'$inc':{'count':1}})
        insert_by_key_value('logs',time_date=str(datetime.now()),platform=request.user_agent.platform, browser=request.user_agent.browser, language=request.user_agent.language, short_code=short_code)
        return redirect(url_document['url'])

@app.route('/<string:short_code>/logs')
def short_link_usage_log(short_code):
        usage_logs = db_log.find({'short_code':short_code})
        return render_template('short_link_log.html',usage_logs=usage_logs,short_code=short_code,user=get_current_user())
