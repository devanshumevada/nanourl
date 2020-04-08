from app import app
from flask import render_template, url_for, request, session, redirect
from db import db_user, db_links
from bson import ObjectId
#from check_url import validate_url
#from generate_short_url_code import generate_short_code

#index and dashboard
@app.route('/')
def index():
        if 'user' not in session:
                return render_template('login.html')
        else:
                return redirect(url_for('dashboard'))
                


@app.route('/dashboard')
def dashboard():
        return render_template('dashboard.html',links=db_links.find({'_id':ObjectId(session['user'])}),user=db_user.find_one({'_id':ObjectId(session['user'])}), url_not_valid=request.args.get('url_not_valid'))

'''
#login, logout and register routes
@app.route('/register',methods=['GET','POST'])
def register():
        if user_logged_in():
                return redirect(url_for('index'))
        if request.method=='POST':
                name,email,password = request.form['name'], request.form['email'], request.form['password']
                if db_user.find({'email':email}).count()>0:
                        return render_template('login.html', user_already_exists=True)
                user=db_user.insert_one({'name':name,'password':password,'email':email})
                return redirect(url_for('index'))
        return render_template('login.html')

@app.route('/login',methods=['GET','POST'])
def login():
        if user_logged_in():
                return redirect(url_for('index'))
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

'''
'''
#routes for adding, deleting a link and incrementing it's count on using it's short version
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
                        return redirect(url_for('index'))
                #On getting a GET request
                return redirect(url_for('index'))
        return redirect(url_for('login'))


@app.route('/<string:id>/delete')
def delete_short_url(id):
        if user_logged_in():
                if request.method=='GET':
                        db_links.delete_one({'_id':ObjectId(id)})
                        return redirect(url_for('index'))
        return redirect(url_for('login'))


@app.route('/<string:short_code>')
def increment_and_go(short_code):
        url_document = db_links.find_one({'short_code':short_code})
        if  url_document is None:
                return '<h4>Not a valid short URL. Please log-in to your account to get a list'
        db_links.update_one({'short_code':short_code},{'$inc':{'count':1}})
        return redirect(url_document['url'])
'''
'''            
#Other supplementary functions
def user_logged_in():
        if 'user' in session:
                return True

'''


        



    