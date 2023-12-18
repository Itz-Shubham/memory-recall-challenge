from flask import current_app
from flask_mail import Message, Mail

def send_forget_password_mail(email:str, token:str) -> bool:
    message = Message(recipients=[email])
    message.subject = 'Memory Recall Challenge: Password Reset'
    # message.body = '' # Either send html or body text
    message.html = f"""
    <h1> Password Reset </h1>
    Here is a link to reset your password click here and change your password. 
    <a href="http://127.0.0.1:5000/change-password?token={token}">Reset Password</a>
    """
    mail = Mail(current_app)
    mail.send(message)
    return True
