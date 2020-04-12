from app import app
from flask import request, redirect, url_for, session, render_template
from db import db_links, db_user
from helper import user_logged_in
from send_emails import send_account_verification_email, send_forgot_password_instructions_email
from bson import ObjectId


@app.route('/register',methods=['GET','POST'])
def register():
        if user_logged_in():
                return redirect(url_for('index'))
        if request.method=='POST':
                name,email,password = request.form['name'], request.form['email'], request.form['password']
                if db_user.find({'email':email}).count()>0:
                        return redirect(url_for('login',user_already_exists=True))
                user=db_user.insert_one({'name':name,'password':password,'email':email,'is_verified':0})
                send_account_verification_email(email, str(user.inserted_id))
                return redirect(url_for('login',email_sent=True))
        return redirect('/login')

@app.route('/login',methods=['GET','POST'])
def login():
        if user_logged_in():
                return redirect('/')
        if request.method=='POST':
               user=db_user.find_one({'email':request.form['email'],'password':request.form['password']})
               if user is None:
                       return redirect(url_for('login',user_not_exists=True))
               if user['is_verified']==0:
                       return redirect(url_for('login', account_verification=False))
               else:
                        session['user']=str(user['_id'])
                        return redirect('/')

        return render_template('login.html', 
                user_already_exists=request.args.get('user_already_exists'),
                email_sent=request.args.get('email_sent'),
                user_not_exists=request.args.get('user_not_exists'),
                account_verification=request.args.get('account_verification'),
                forgot_password_instructions=request.args.get('forgot_password_instructions')
        )

@app.route('/logout')
def logout():
        session.pop('user',None)
        return redirect('/')

@app.route('/<string:user_id>/verify')
def verify_user_account(user_id):
        if db_user.find_one({'_id':ObjectId(user_id)})['is_verified']==1:
                return '<h4>Account already verified, please <a href="/login">Log In</a></h4>'
        db_user.update_one({'_id':ObjectId(user_id)},{'$set':{'is_verified':1}})
        return '<h4>Account Verified! <a href="/login">Click Here</a> to log in'

@app.route('/forgot_password', methods=['POST'])
def forgot_password():
        email = request.form['recipient-email']
        user = db_user.find_one({'email':email})
        if user is None:
                return redirect(url_for('login',user_not_exists=True))
        send_forgot_password_instructions_email(user['email'],user['password'])
        return redirect(url_for('login', forgot_password_instructions=True))