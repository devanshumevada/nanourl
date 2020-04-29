from app import app
from flask import (render_template, 
                   url_for, 
                   request, 
                   session, 
                   redirect)
from db import db_user, db_links
from bson import ObjectId
from helper import (get_current_user, 
                    get_current_user_links, 
                    user_logged_in)

@app.route('/')
def index():
        if not user_logged_in():
                return redirect(url_for('login'))
        else:
                return redirect(url_for('dashboard'))
                

@app.route('/dashboard')
def dashboard():
        if user_logged_in():
                return render_template('dashboard.html',links=get_current_user_links(),user=get_current_user(), url_not_valid=request.args.get('url_not_valid'))
        return redirect(url_for('login'))




    