from setup import url_safe_timed_serializer, mail
from flask_mail import Message
from flask import url_for

def send_confirmation_account_email(email):
    token = url_safe_timed_serializer.dumps(email, salt='email-confirm')
    msg = Message('Confirm Email', sender='mahdislami1377@gmail.com', recipients=[email])
    link = url_for('confirm_email.confirm_email', token=token, _external=True)
    msg.body = 'Your link is {}'.format(link)
    mail.send(msg)
    return



