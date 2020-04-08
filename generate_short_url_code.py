import string
import secrets

def generate_short_code():
    return str(''.join(secrets.choice(string.ascii_uppercase + string.digits) for i in range(6)))

