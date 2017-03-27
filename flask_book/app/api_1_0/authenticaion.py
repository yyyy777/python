# coding=utf-8

from flask_httpauth import HTTPBasicAuth
from flask import g, jsonify
from app.models import User, AnonymousUser
from . import api
from .errors import unauthorized, forbidden
auth = HTTPBasicAuth()


@api.before_request
@auth.login_required
def before_request():
    if not g.current_user.isanonymous and \
            not g.current_user.confirmed:
        return forbidden('Unconfirmed account')


@auth.verify_password
def verify_password(email_or_token, password):
    if email_or_token == '':
        g.current_user = AnonymousUser()
        return True
    if password == '':
        g.current_user = user.verify_auth_token(email_or_token)
        g.token_used = True
        return g.current_user is not None
    user = User.query.filter_by(email=email).first()
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    return user.verify_password(password)


@app.route('/token')
def get_token():
    if g.current_user.is_anonymous or g.token_used:
        return unauthorized('Invalid credentials')
    return jsonify({'token': g.current_user.generate_auth_token(
        expiration=3600), 'expiration': 3600})


@auth.error_handler
def auth_error():
    return unauthofized('Invalid credentials')
