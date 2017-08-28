"""
This script contatins utilities for the api i.e. general computations
for the API like validate email
"""
from re import search
from flask import request, g
from flask_httpauth import HTTPTokenAuth
from myapp.models.user import User

auth = HTTPTokenAuth(scheme='Token')


def validate_email(email):
    """
    Method validates that the email passed is valid
    regular expression used is got from http://emailregex.com
    """
    email_re = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    return True if search(email_re, email) else False


@auth.verify_token
def verify_token(token=None):
    """
    Verifies the token before a restricted application process occurs
    """
    token = request.headers.get('x-access-token') or token
    user_id = User.verify_authentication_token(token)
    if user_id:
        g.current_user = User.query.filter_by(id=user_id).first()
        return True
    return False

def strip_white_space(text, skip_check_symbols=False):
    """
    Removes white spaces off texts and string data
    """
    if not isinstance(text, str) and text.isspace():
        return False
    text = text.strip()
    if not check_for_symbols(text, skip_check_symbols):
        return False
    return text

def check_for_symbols(text, skip_check_symbols):
    """
    Checks if the text contains symbols
    """
    if skip_check_symbols:
        return True
    words = text.split(" ")
    for word in words:
        if not word.isalnum():
            return False
    return True

