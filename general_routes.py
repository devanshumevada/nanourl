from app import app
from flask import render_template, url_for, request, session, redirect
from db import db_user, db_links
from bson import ObjectId
from helper import get_current_user, get_current_user_links

@app.route('/')
def index():
        if 'user' not in session:
                return redirect(url_for('login'))
                #return render_template('login.html', email_not_sent=request.args.get('email_not_sent'), email_sent=request.args.get('email_sent'),account_verification=request.args.get('account_verification'))
        else:
                return redirect(url_for('dashboard'))
                

@app.route('/dashboard')
def dashboard():
        return render_template('dashboard.html',links=get_current_user_links(),user=get_current_user(), url_not_valid=request.args.get('url_not_valid'))




    