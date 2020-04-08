from app import app
from flask import render_template, url_for, request, session, redirect
from db import db_user, db_links
from bson import ObjectId

@app.route('/')
def index():
        if 'user' not in session:
                return render_template('login.html')
        else:
                return redirect(url_for('dashboard'))
                


@app.route('/dashboard')
def dashboard():
        return render_template('dashboard.html',links=db_links.find({'_id':ObjectId(session['user'])}),user=db_user.find_one({'_id':ObjectId(session['user'])}), url_not_valid=request.args.get('url_not_valid'))




    