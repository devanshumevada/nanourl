from flask import Flask,session
from config import SECRET_KEY

app = Flask(__name__)
app.secret_key=SECRET_KEY


from routes import *

if __name__=='__main__':
    app.run(debug=True)