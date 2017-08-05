"""
This script contatins utilities for the api i.e. general computations
for the API like validate email
"""
from re import search
from flask import g
from flask_httpauth import HTTPTokenAuth

auth = HTTPTokenAuth(scheme='Token')


def validate_email(email):
    """
    Method validates that the email passed is valid
    regular expression used is got from http://emailregex.com
    """
    email_re = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    return True if search(email_re, email) else False


@auth.verify_token
def verify_token(token):
    if g.current_user.verify_authentication_token(token):
        return True
    return False