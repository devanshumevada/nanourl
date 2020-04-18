from app import app
from flask import request, redirect, url_for, session, render_template, flash
from db import db_links, db_user, db_token
from helper import user_logged_in, find_by_key_value, update_by_key_value, get_current_user, insert_by_key_value, generate_forgot_password_token
from send_emails import send_account_verification_email, send_forgot_password_instructions_email
from bson import ObjectId


@app.route('/register',methods=['GET','POST'])
def register():
        if user_logged_in():
                return redirect(url_for('index'))
        if request.method=='POST':
                name,email,password = request.form['name'], request.form['email'], request.form['password']
                if db_user.find({'email':email}).count()>0:
                        flash('User with these credentials already exists!','user_auth')
                        return redirect(url_for('login'))
                user=insert_by_key_value('user',name=name,password=password,email=email,is_verified=0)
                send_account_verification_email(email, str(user.inserted_id))
                flash('A verification email has been sent to your registered email account','email')
                return redirect(url_for('login'))
        return redirect('/login')

@app.route('/login',methods=['GET','POST'])
def login():
        if user_logged_in():
                return redirect('/')
        if request.method=='POST':
               user=find_by_key_value('user',email=request.form['email'],password=request.form['password'])
               if user is None:
                       flash('User with these credentials does not exists!','user_auth')
                       return redirect(url_for('login'))
               if user['is_verified']==0:
                       flash('Your account hasnt been verified!','user_auth')
                       return redirect(url_for('login'))
               else:
                        session['user']=str(user['_id'])
                        return redirect('/')

        return render_template('login.html')
                
@app.route('/logout')
def logout():
        session.pop('user',None)
        return redirect('/')

@app.route('/<string:user_id>/verify')
def verify_user_account(user_id):
        if find_by_key_value('user',_id=ObjectId(user_id))['is_verified']==1:
                return '<h4>Account already verified, please <a href="/login">Log In</a></h4>'
        update_by_key_value('user',target={'_id':ObjectId(user_id)},to_update_data={'is_verified':1})
        return '<h4>Account Verified! <a href="/login">Click Here</a> to log in'

@app.route('/forgot_password', methods=['POST'])
def forgot_password():
        email = request.form['recipient-email']
        user = find_by_key_value('user',email=email)
        if user is None:
                flash('User with this credential does not exists!','user_auth')
                return redirect(url_for('login'))
        token = generate_forgot_password_token()
        insert_by_key_value('tokens',token=token, user=str(user['_id']))
        send_forgot_password_instructions_email(user['email'],token)
        flash('Instructions to reset your password have been sent on your registered email account','email')
        return redirect(url_for('login'))

@app.route('/<string:token>/reset_password',methods=['GET','POST'])
def reset_password(token):
        if request.method=='POST':
                new_password = request.form['password']
                user_id = find_by_key_value('tokens',token=token)['user']
                update_by_key_value('users',target={'_id':ObjectId(user_id)}, to_update_data={'password':new_password})
                db_token.delete_one({'token':token})
                flash('Password updated successfully!','success')
                return redirect(url_for('login'))
        return render_template('reset_password.html',token=token)

@app.route('/edit_profile', methods=['GET','POST'])
def profile():
        if request.method=='POST':
                type_ = request.form['type']
                if type_ == 'password':
                        try:
                                new_password, old_password = request.form['new_password'], request.form['old_password']
                                if find_by_key_value('user',_id=ObjectId(session['user']))['password'] == old_password:
                                        update_by_key_value('user',target={'_id':ObjectId(session['user'])}, to_update_data={'password':new_password})
                                        flash('Password Successfully updated','success')
                                else:
                                        flash('Your old password seems to have been entered incorrectly!','failed')
                        except:
                                flash('Something went wrong, please try again later!','failed')
                elif type_ == 'name':
                        try:
                                name = request.form['name']
                                update_by_key_value('user',target={'_id':ObjectId(session['user'])},to_update_data={'name':name})
                                flash('Name successfully updated','success')
                        except:
                                flash('Something went wrong, please try again later!','failed')
                else:
                        try:
                                email = request.form['email']
                                update_by_key_value('user',target={'_id':ObjectId(session['user'])}, to_update_data={'email':email,'is_verified':0})
                                send_account_verification_email(email,session['user'])
                                flash('Email updated. A verification email has been on your updated email account')
                        except:
                                flash('Something went wrong, please try again later!','failed')
                return redirect(url_for('profile'))
        return render_template('profile.html', user=get_current_user())


