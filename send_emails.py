from config import EMAIL_API_KEY
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_account_verification_email(email,user_id):
    message = Mail(
        from_email='devanshu.mevada@yahoo.com',
        to_emails=email,
        subject='Please Verify your account',
        html_content = "Please verify your account by clicking on this <a href='http://127.0.0.1:500/"+user_id+"/verify"+">link</a>"
    )
    sg=SendGridAPIClient(EMAIL_API_KEY)
    sg.send(message)

