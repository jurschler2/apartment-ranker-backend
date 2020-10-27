from flask import g, request
from functools import wraps
from jwt import decode, InvalidSignatureError, DecodeError
from project import SECRET_KEY
from project import db
from project.models.models import User


def make_error(message, code):
    return {"errors": message}, code


def put_jwt_into_g():
    """ Function for grabbing the token out of the header,
    for when you don't need to error if the user isn't logged in """
    print(f"These are the request headers: {request.headers}")
    token = request.headers.get("Authorization")
    try:
        decoded = decode(token, SECRET_KEY, algorithms=["HS256"])
        if decoded["user_ip_address"] == request.headers['X-Forwarded-For'][0]:
            g.user = User.query.filter_by(user_ip_address=decoded["user_ip_address"]).first()
        else:
            g.user = None
    except (InvalidSignatureError, DecodeError):
        g.user = None


def jwt_required(fn):
    """
    Decorator to protect any routes that require a valid JWT.
    If valid, attaches current user instance to g.user.
    Otherwise, issues a response with a 401 status code.
    """

    print("Clearly we get in here and it fails on the get for all apartments")

    @wraps(fn)
    def wrapper(*args, **kwargs):
        put_jwt_into_g()
        if g.user is None:
            return make_error("User not found.", 401)
        return fn(*args, **kwargs)

    return wrapper
