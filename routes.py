from app import app
from flask import render_template, url_for, request, session
from db import db_user, db_links

@app.route('/')
def index():
        return render_template('login.html')
    