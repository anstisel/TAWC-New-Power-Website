from tempfile import TemporaryFile
import requests
import jwt
import json
import http.client
from app.models import User
from app import db
from functools import wraps
from flask import request


def require_jwt(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Do something with your request here
        user = validate_user(request.headers["Authorization"])
        return f(*args, **kwargs, user=user)
    return decorated_function


def require_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Do something with your request here
        user = validate_user(request.headers["Authorization"])
        if not user.admin:
            raise ValueError("user is not an admin")
        return f(*args, **kwargs)
    return decorated_function


def fetch_jwks():
    url = "https://dev-7lc6f7vw.us.auth0.com/.well-known/jwks.json"
    jwks = requests.get(url).json()

    public_keys = {}
    for jwk in jwks['keys']:
        kid = jwk['kid']
        public_keys[kid] = jwt.algorithms.RSAAlgorithm.from_jwk(
            json.dumps(jwk))

    return (public_keys)


JWKS = fetch_jwks()


def validate_user(token):
    """Takes a JWT token from the frontend,
    validates it against the auth0
    creates a new user in the db if one doesn't exist
    returns the user object"""

    try:
        decoded_token = decode_token(token, JWKS)
        auth0_id = decoded_token["sub"]
        print("suceeded decode")
    except:
        print("Failed decode")
        user_info = authenticate_token(token)
        auth0_id = user_info["sub"]

    user = User.query.filter_by(auth0_id=auth0_id).first()

    if not user:
        user_info = authenticate_token(token)
        user = create_user(user_info)

    return (user)


def create_user(auth0_user_info):
    """Create a user from the auth0 user info object"""
    proposed_name = auth0_user_info["nickname"]
    if User.query.filter_by(username=proposed_name).first():
        num = 1
        modified_proposal = proposed_name + str(num)
        while User.query.filter_by(username=modified_proposal).first():
            num += 1
            modified_proposal = proposed_name + str(num)
        proposed_name = modified_proposal
    user_dat = {
        "username": proposed_name,
        "auth0_id": auth0_user_info["sub"],
        "avatar": auth0_user_info["picture"]
    }
    print(auth0_user_info)
    user = User(**user_dat)

    db.session.add(user)
    db.session.commit()
    return (user)


def authenticate_token(token):
    a = requests.get('https://dev-7lc6f7vw.us.auth0.com/userinfo',
                     headers={"authorization": "bearer " + token})
    return (a.json())


def decode_token(token, public_keys):

    kid = jwt.get_unverified_header(token)['kid']
    key = public_keys[kid]
    data = jwt.decode(token, key, algorithms=[
                      'RS256'], audience="http://localhost:5000")
    return (data)
