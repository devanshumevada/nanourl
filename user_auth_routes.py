from app import app
from flask import request, redirect, url_for, session, render_template
from db import db_links, db_user
from helper import user_logged_in


@app.route('/register',methods=['GET','POST'])
def register():
        if user_logged_in():
                return redirect(url_for('index'))
        if request.method=='POST':
                name,email,password = request.form['name'], request.form['email'], request.form['password']
                if db_user.find({'email':email}).count()>0:
                        return render_template('login.html', user_already_exists=True)
                user=db_user.insert_one({'name':name,'password':password,'email':email})
                return redirect('/')
        return render_template('login.html')

@app.route('/login',methods=['GET','POST'])
def login():
        if user_logged_in():
                return redirect('/')
        if request.method=='POST':
               user=db_user.find_one({'email':request.form['email'],'password':request.form['password']})
               if user is None:
                       return render_template('login.html',user_not_exists=True)
               else:
                        session['user']=str(user['_id'])
                        return redirect('/')
        return render_template('login.html')

@app.route('/logout')
def logout():
        session.pop('user',None)
        return redirect('/')