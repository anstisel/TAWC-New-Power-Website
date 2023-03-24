from flask import jsonify, request, url_for, current_app
from app import db
from app.models import Comment, CommentVote, Post
from app.api import bp
from datetime import datetime
from app.api import auth
# this module provides apis routes for comments, potential routes: search_comment

# route for create a comment, pid, uid, such are expected from request json
# all comments expect author_id, body, post_id as input
# replies expect parent_comment_id as extra input to mount correctly


@bp.route('/comments', methods=['POST'])
@auth.require_jwt
def create_comment(user=""):
    data = request.get_json() or {}
    if 'body' not in data or 'type' not in data or 'post_id' not in data:
        return jsonify({'error': 'must provide valid comment data'})
    data["author_id"] = user.user_id
    comment = Comment(**data)  # Comment()
    db.session.add(comment)
    db.session.commit()
    response = jsonify(comment.to_dict())
    return response


# route for getting all comments for a single post, used testing (admin)
@bp.route('/comments/<int:pid>', methods=['GET'])
def get_comments(pid):
    type = request.args.get("type", "solution", type=str)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get(
        'per_page', current_app.config['POST_PER_PAGE'], type=int), 100)
    resource = Comment.query.filter_by(
        type=type, post_id=pid)
    data = Comment.to_collection_dict(
        # resource, page, per_page, 'api.get_comments', pid=pid)
        resource, page, per_page)
    return jsonify(data)

# route for return commments of a certain user


@bp.route('/comments/user/<int:uid>', methods=['GET'])
def get_user_commments(uid):
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get(
        'per_page', current_app.config['POST_PER_PAGE'], type=int), 100)
    data = Comment.to_collection_dict(Comment.query.filter_by(
        author_id=uid).order_by(Comment.create_time.desc()), page, per_page)
    return jsonify(data)

# route for getting unmoderated comments (admin)
# append ?type=<comment_type> at the end of route to get respective type of comment. Default retrieves solutions.


@bp.route('/comments/unmoderated', methods=['GET'])
def get_unmoderated_comments():
    type = request.args.get("type", "solution", type=str)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get(
        'per_page', current_app.config['POST_PER_PAGE'], type=int), 100)
    resource = Comment.query.filter_by(
        last_moderate_time=None, type=type).order_by(Comment.create_time.asc())
    data = Comment.to_collection_dict(resource, page, per_page)
    return jsonify(data)

# route for getting moderated comments
# ordered by the last_moderate_time in descending order


@bp.route('/comments/moderated', methods=['GET'])
def get_moderated_comments():
    type = request.args.get("type", "solution", type=str)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get(
        'per_page', current_app.config['POST_PER_PAGE'], type=int), 100)
    resource = Comment.query.filter(Comment.last_moderate_time != None, Comment.type == type).order_by(
        Comment.last_moderate_time.desc())
    data = Comment.to_collection_dict(resource, page, per_page)
    return jsonify(data)

# route for getting approved comments for a single post, used for post viewing page (user)
# comments are ordered by vote_counts in descending order


@bp.route('/comments/approved/<int:pid>', methods=['GET'])
def get_approved_comments(pid):
    type = request.args.get("type", "solution", type=str)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get(
        'per_page', current_app.config['POST_PER_PAGE'], type=int), 100)
    resource = Comment.query.filter(Comment.last_moderate_time != None, Comment.approved == True, Comment.type == type, Comment.post_id == pid).order_by(
        Comment.vote_count.desc())
    data = Comment.to_collection_dict(resource, page, per_page)
    return jsonify(data)


# route for getting unapproved comments for a single post, used for admin working mode, so moderated comments only
# pagination depends on solutions. so include 'page':int, 'per_page':int. otherwise set to 1, 50
# this route is useless perhaps
@bp.route('/comments/unapproved/<int:pid>', methods=['GET'])
def get_unapproved_comments(pid):
    type = request.args.get("type", "solution", type=str)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get(
        'per_page', current_app.config['POST_PER_PAGE'], type=int), 100)
    resource = Comment.query.filter(Comment.approved == False, Comment.type == type, Comment.post_id == pid).order_by(
        Comment.last_moderate_time.desc())
    data = Comment.to_collection_dict(resource, page, per_page)
    return jsonify(data)


# route for editing the comment status, for admin usage
# always expects a approved as input to define admin action
# can attach admin_msg as input to store the message admin has
@bp.route('/comments/admin/<int:cid>', methods=['PUT'])
@auth.require_admin
def judge_comment(cid):
    data = request.get_json() or {}
    comment = db.session.query(Comment).get_or_404(cid)
    if 'approved' not in data:
        return jsonify({'errmsg': 'must provide admin action'})
    comment.approved = data['approved']
    for field in ['admin_msg']:
        if field in data:
            setattr(comment, field, data[field])
    comment.last_moderate_time = datetime.utcnow()
    post = Post.query.filter_by(post_id=comment.post_id).first()
    post.last_modify_time = datetime.utcnow()
    db.session.add(post)
    db.session.commit()
    return jsonify(comment.to_dict())


# route for deleting a comment, used by admin
# will delete all votes and child commments related to this comment
@bp.route('/comments/admin/delete/<int:cid>', methods=['PUT'])
@auth.require_admin
def delete_comment(cid):
    comment = Comment.query.filter_by(comment_id=cid).first()
    for item in Comment.query.filter(Comment.parent_comment_id == comment.comment_id).all():
        for comment_vote in CommentVote.query.filter(CommentVote.comment_id == item.comment_id).all():
            db.session.delete(comment_vote)
        db.session.delete(item)
    for comment_vote in CommentVote.query.filter(CommentVote.comment_id == comment.comment_id).all():
        db.session.delete(comment_vote)
    db.session.delete(comment)
    db.session.commit()
    return jsonify({'msg': 'comment and its child comments and votes are deleted'})


# route for delecting a comment, used by user, so can only delete own comments.
# will delete all votes and child commments related to this comment
@bp.route('/comments/user/delete/<int:cid>', methods=['PUT'])
@auth.require_jwt
def delete_self_comment(cid, user):
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get(
        'per_page', current_app.config['POST_PER_PAGE'], type=int), 100)
    # for now we accept user_id from url requests, but later will be from current_user.user_id
    user_id = user.user_id
    comment = Comment.query.filter_by(comment_id=cid).first()
    if comment.author_id == user_id:
        for item in Comment.query.filter(Comment.parent_comment_id == comment.comment_id).all():
            for comment_vote in CommentVote.query.filter(CommentVote.comment_id == item.comment_id).all():
                db.session.delete(comment_vote)
            db.session.delete(item)
        for comment_vote in CommentVote.query.filter(CommentVote.comment_id == comment.comment_id).all():
            db.session.delete(comment_vote)
        db.session.delete(comment)
        db.session.commit()
        return jsonify({'msg': 'comment and its child comments and votes are deleted'})
    else:
        return jsonify({'msg': 'current user does not own this comment'})


# route for updating the comment contents, for user usage, will change the status of the comment to 'unapproved'
# expect only body as input, (must)
@bp.route('/comments/user/<int:cid>', methods=['PUT'])
@auth.require_jwt
def update_comment(cid, user):
    data = request.get_json() or {}
    comment = db.session.query(Comment).get_or_404(cid)
    user_id = user.user_id
    if comment.author_id == user_id:
        for field in ['body']:
            if field in data:
                setattr(comment, field, data[field])
        comment.last_modify_time = datetime.utcnow()
        comment.last_moderate_time = None
        comment.approved = False
        comment.admin_msg = None
        db.session.commit()
        return jsonify(comment.to_dict())
    else:
        return jsonify({'msg': 'current user does not own this comment'})


# # route for return list of a user's history comments, used for user profile page
# @bp.route('/comments/user/<int:uid>', methods=['GET'])
# def search_comment(uid):
#     pass
