from app.api import bp
from flask import jsonify
from app.api import auth


@bp.route('/who_am_i', methods=['GET'])
@auth.require_jwt
def who_am_i(user):
    return jsonify(user.to_dict())
