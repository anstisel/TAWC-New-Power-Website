from flask import jsonify, request, url_for, current_app
from app import db
from app.models import Post, CommentVote, Comment, User
from app.api import bp
from datetime import datetime
from app.api import auth

# route for single post return api
# expect post_id as input


@bp.route('/posts/<int:pid>', methods=['GET'])
def get_post(pid):
    return jsonify(Post.query.get_or_404(pid).to_dict())


# route for post posting
# all posts expect title, body, creator_id as input
@bp.route('/posts', methods=['POST'])
@auth.require_jwt
def create_post(user):
    data = request.get_json() or {}
    if 'body' not in data or 'title' not in data:
        return jsonify({'error': 'must provide creator_id, body,title'})
    data["creator_id"] = user.user_id
    post = Post()
    post.from_dict(data, True)
    db.session.add(post)
    db.session.commit()
    response = jsonify(post.to_dict())
    return response


# route for participation check, return if a user participated in this post.
# expects a post_id as input
@bp.route('/posts/check/<int:pid>', methods=['GET'])
def check_user_participation(pid):
    # can be replace by current_user.user_id later, marks for Sean
    uid = request.args.get('user_id', 0, type=int)
    post = Post.query.filter_by(post_id=pid).first()
    user = User.query.filter_by(user_id=uid).first()
    # surely the owner can pass the check
    if user.admin:
        return jsonify({'participation_check': True})
    if post.creator_id == uid:
        return jsonify({'participation_check': True})
    # check for all comments to see if any one is created by the current user
    for comment in post.comments:
        if comment.author_id == uid:
            if comment.approved:
                return jsonify({'participation_check': True})
    return jsonify({'participation_check': False})


# route for posts return, with predefined pagination parameters, potential replacement: accept inputs for pagination
# these can extend to instant pagination and allows send back in specific order(vote, create_time, last_reply,etc)
# for testing usage, don't request!
@bp.route('/posts', methods=['GET'])
def get_posts():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get(
        'per_page', current_app.config['POST_PER_PAGE'], type=int), 100)
    # data = Post.to_collection_dict(Post.query, page, per_page, 'api.get_posts')
    data = Post.to_collection_dict(Post.query, page, per_page)
    return jsonify(data)


# route for return posts for a certain user
# ordered by posts' create_time
@bp.route('/posts/user/<int:uid>', methods=['GET'])
def get_user_posts(uid):
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get(
        'per_page', current_app.config['POST_PER_PAGE'], type=int), 100)
    data = Post.to_collection_dict(Post.query.filter_by(
        creator_id=uid).order_by(Post.create_time.desc()), page, per_page)
    return jsonify(data)


# route for approved posts return
# use this route for discussion broad, tab: popular
# ordered by last_modify_time which is the last reply time
@bp.route('/posts/approved', methods=['GET'])
def get_approved_posts():
    resource = Post.query.filter_by(approved=True, archived=False).order_by(
        Post.last_modify_time.desc())
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get(
        'per_page', current_app.config['POST_PER_PAGE'], type=int), 100)
    data = Post.to_collection_dict(
        # resource, page, per_page, 'api.get_unapproved_posts')
        resource, page, per_page)
    return jsonify(data)


# route for archived approved posts return
# use this route for discussion broad, tab: archived
# ordered by last_modify_time which is the last reply time
@bp.route('/posts/approved/archived', methods=['GET'])
def get_archived_posts():
    resource = Post.query.filter_by(approved=True, archived=True).order_by(
        Post.last_modify_time.desc())
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get(
        'per_page', current_app.config['POST_PER_PAGE'], type=int), 100)
    data = Post.to_collection_dict(
        # resource, page, per_page, 'api.get_unapproved_posts')
        resource, page, per_page)
    return jsonify(data)


# route for unmoderated posts return
# used by admin, ordered in the create_time
@bp.route('/posts/unmoderated', methods=['GET'])
def get_unmoderated_posts():
    resource = Post.query.filter_by(
        last_moderate_time=None).order_by(Post.create_time.asc())
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get(
        'per_page', current_app.config['POST_PER_PAGE'], type=int), 100)
    data = Post.to_collection_dict(
        # resource, page, per_page, 'api.get_unapproved_posts')
        resource, page, per_page)
    return jsonify(data)

# route for return moderated posts
# used by admin, tab: history


@bp.route('/posts/moderated', methods=['GET'])
def get_moderated_posts():
    resource = Post.query.filter(Post.last_moderate_time != None).order_by(
        Post.last_moderate_time)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get(
        'per_page', current_app.config['POST_PER_PAGE'], type=int), 100)
    print(page, per_page)
    data = Post.to_collection_dict(
        # resource, page, per_page, 'api.get_unapproved_posts')
        resource, page, per_page)
    return jsonify(data)


# route for updating the post, status changing for admin
# provide admin_msg(optional) to give admin's hints on decisions
@bp.route('/posts/admin/<int:pid>', methods=['PUT'])
@auth.require_admin
def judge_post(pid):
    data = request.get_json() or {}
    post = db.session.query(Post).get_or_404(pid)
    if 'approved' not in data:
        return jsonify({'errmsg': 'must provide admin action'})
    post.approved = data['approved']
    for field in ['admin_msg']:
        if field in data:
            setattr(post, field, data[field])
    post.last_moderate_time = datetime.utcnow()
    db.session.commit()
    return jsonify(post.to_dict())

# route for archiving a post, used by admin


@bp.route('/posts/admin/archive/<int:pid>', methods=['PUT'])
@auth.require_admin
def archive_post(pid):
    data = request.get_json() or {}
    post = db.session.query(Post).get_or_404(pid)
    if 'archived' not in data:
        return jsonify({'errmsg': 'must provide archive action'})
    post.archived = data['archived']
    db.session.commit()
    return jsonify(post.to_dict())


# route for deleting a post, used by admin
@bp.route('/posts/admin/delete/<int:pid>', methods=['PUT'])
@auth.require_admin
def delete_post(pid):
    post = Post.query.filter_by(post_id=pid).first()
    for comment in Comment.query.filter(Comment.post_id == post.post_id).all():
        for comment_vote in CommentVote.query.filter(CommentVote.comment_id == comment.comment_id).all():
            db.session.delete(comment_vote)
        db.session.delete(comment)
    db.session.delete(post)
    db.session.commit()
    return jsonify({'msg': 'the post and its comments and votes are deleted'})

# route for deleting a post, used by user, so can only delete own comments.


@bp.route('/posts/user/delete/<int:pid>', methods=['PUT'])
@auth.require_jwt
def delete_self_post(pid, user):
    user_id = user.user_id
    post = Post.query.filter_by(post_id=pid).first()
    if post.creator_id == user_id:
        for comment in Comment.query.filter(Comment.post_id == post.post_id).all():
            for comment_vote in CommentVote.query.filter(CommentVote.comment_id == comment.comment_id).all():
                db.session.delete(comment_vote)
            db.session.delete(comment)
        db.session.delete(post)
        db.session.commit()
        return jsonify({'msg': 'the post and its comments and votes are deleted'})
    else:
        return jsonify({'msg': 'current user does not own this post, can not delete'})


# route for updating the post, post data editing for poster
# post will be updated for moderation again after changing. used by user
@bp.route('/posts/update/<int:pid>', methods=['PUT'])
@auth.require_jwt
def update_post(pid, user):
    data = request.get_json() or {}
    post = db.session.query(Post).get_or_404(pid)
    # can be replace by current_user.user_id later, marks for Sean
    user_id = user.user_id
    if post.creator_id == user_id:
        for field in ['body', 'title']:
            if field in data:
                setattr(post, field, data[field])
        post.last_modify_time = datetime.utcnow()
        post.last_moderate_time = None
        post.approved = False
        post.admin_msg = None
        db.session.commit()
        return jsonify(post.to_dict())
    else:
        return jsonify({'msg': 'current user does not own this post, can not modify'})
