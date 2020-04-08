#all non-route helping functions
from flask import session
def user_logged_in():
        if 'user' in session:
                return True