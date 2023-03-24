from app.api import bp

# this module provides api routes for users, potential routes: follower, followed.

# route for return single user, used for user profile page
@bp.route('/users/<int:uid>', methods=['GET'])
def get_user(uid):
    pass

# route for return collection of users, used for post viewing api query, a list of uid is expected from request.
@bp.route('/users', methods=['GET'])
def get_users():
    pass

# route for return unapproved users, used for admin page
@bp.route('/users/unapproved', methods=['GET'])
def get_unapproved_users():
    pass


#route for editing user status, used by admin page
@bp.route('/users/admin/<int:uid>', methods=['PUT'])
def judge_user():
    pass

#route for updating user info, used by user profile page
@bp.route('/users/user/<int:uid>', methods=['PUT'])
def update_user():
    pass

# #route for follower users return
# @bp.route('/users/<int:uid>/follower', methods=['GET'])
# def get_followers(uid):
#     pass
#
# #route for followed users return
# @bp.route('/users/<int:uid>/follwed', methods=['GET'])
# def get_followed(uid):
#     pass
