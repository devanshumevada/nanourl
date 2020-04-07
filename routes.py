from app import app
from flask import render_template, url_for, request, session, redirect
from db import db_user, db_links
from bson import ObjectId

@app.route('/')
def index():
        if 'user' not in session:
                return render_template('login.html')
        else:
                return render_template('dashboard.html')



#login, logout and register routes
@app.route('/register',methods=['GET','POST'])
def register(): 
        if request.method=='POST':
                name,email,password = request.form['name'], request.form['email'], request.form['password']
                if db_user.find({'email':email}).count()>0:
                        return render_template('login.html', user_already_exists=True)
                user=db_user.insert_one({'name':name,'password':password,'email':email})
                return redirect(url_for('index'))
        return render_template('login.html')

@app.route('/login',methods=['GET','POST'])
def login():
        if request.method=='POST':
               user=db_user.find_one({'email':request.form['email'],'password':request.form['password']})
               if user is None:
                       return render_template('login.html',user_not_exists=True)
               else:
                        session['user']=str(user['_id'])
                        return redirect(url_for('index'))
        return render_template('login.html')

@app.route('/logout')
def logout():
        session.pop('user',None)
        return redirect(url_for('index'))





        



    