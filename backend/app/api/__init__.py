# api provides data handshakes, input, output, database actions

from flask import Blueprint

bp = Blueprint('api', __name__)

# load the modules for different apis here, potential extras: token for authentication, error for helping and logging.
from app.api import users, posts, comments, votes, login
# from app.api import tokens, errors
