from flask_httpauth import HTTPBasicAuth,HTTPTokenAuth
from app.models import User
from app import db
from datetime import datetime

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()

@basic_auth.verify_password
def verify_password(username,password):
    user = db.session.execute(db.select(User).where(User.username == username)).scalar_one_or_none()
    if user is not None and user.check_password(password):
        return user
    return None


@basic_auth.error_handler
def handle_error(status):
    return {"error":"Incorrect username/password"},status


@token_auth.verify_token
def verify(token):
    user = db.session.execute(db.select(User).where(User.token==token)).scalar_one_or_none()
    return user

@token_auth.error_handler
def handle_error(status):
    return {"error":"Incorrect token"},status