from flask import Flask
from config import SECRET_KEY

app = Flask(__name__)
app.secret_key=SECRET_KEY

from user_routes import *
from link_routes import *
from general_routes import *
from api_routes import *

if __name__=='__main__':
    app.run()