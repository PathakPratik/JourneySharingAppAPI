import imp
import bcrypt
import os
from Models.Users import Users
import re
from setup import url_safe_timed_serializer, mail
from sqlalchemy.exc import IntegrityError
from flask_mail import Message
from flask import url_for, session
from smtplib import SMTPException

def valiadte_login_form(password, email):

    if not email:
        return 'Missing email', False
    
    if not password:
        return 'Missing password', False

    return 'Form is correct', True

def find_user_by_email(email):

    user = Users.query.filter_by(email=email).first()

    if not user:
        return 'User not found', None

    return 'User found', user

def check_password(user, password):
    
    if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return 'User logged in successfully', 200

    return 'Wrong password', 401

def validate_password(password):

    if len(password) < 8:
        return 'Password must be at least 8 chracters', False

    elif re.search('[0-9]',password) is None:
        return 'Password must contain at least one digit', False

    elif re.search('[A-Z]',password) is None: 
        return 'Password must contain at least one capital letter', False

    return 'Password format correct', True

def validate_email(email):

    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$' 

    if re.search(regex, email) is None:   
        return 'Invalid email address', False

    return 'Valid email address', True

def valiadte_register_form(username, password, gender, email, confirmpassword):

    if not username:
        return 'Missing username', False

    elif not password:
        return 'Missing password', False
    
    elif not confirmpassword:
        return 'Missing password confirmation', False

    elif not email:
        return 'Missing email', False
    
    elif not gender:
        return 'Missing gender', False
    
    return 'Form is correct', True
    

def password_match_confrimation(password,password_confirmation):

    if password != password_confirmation:
        return 'Password confirmation incorrect', False

    return 'Password confirmation correct', True


def add_user_to_db(registered_user, db):
    try:
        db.session.add(registered_user)
        db.session.commit()
        return 'User registered successfully', 200
    
    except IntegrityError:
        db.session.rollback()
        return 'User already exists', 400

def update_user_in_db(registered_user, db):

    db.session.add(registered_user)
    db.session.commit()
    return 'User info updated successfully', 200

def send_confirmation_account_email(email):
    print(1)
    token = url_safe_timed_serializer.dumps(email, salt='email-confirm')
    print(2)
    msg = Message('Confirm Email', sender='journeysharingappgroup12@gmail.com', recipients=[email])
    print(3)
    link = url_for('confirm_email.confirm_email', token=token, _external=True)
    print(4)
    msg.body = 'Your link is {}'.format(link)
    print(5)
    try:
        mail.send(msg)
        print(6)
        return 'Confimration email sent successfully', 200
    except SMTPException:
        print(7)
        return 'Unable to send confirmation email', 400

def show_session_ids():
    return str(session)
