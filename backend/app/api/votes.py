from flask import jsonify, request, url_for, current_app
from app import db
from app.models import Comment, Post, CommentVote
from app.api import bp

# this module provides api routes for voting function. detailed structure is not clear yet, so leave blank for now.


# route for getting voting status of a post for a single user
# expects commment_id as input
@bp.route('/votes/comment/<int:cid>', methods=['GET'])
def view_comment_votes(cid):
    comment = Comment.query.filter_by(comment_id=cid).first()
    # can be replace by current_user.user_id later, marks for Sean
    uid = request.args.get('user_id', 0, type=int)
    voted = uid in [vote.user_id for vote in comment.votes]
    data = {
        'voted_on_this_comment': voted
    }
    return jsonify(data)

# route for getting status of the comments inside a post for a single user
# expects comment_id as input
@bp.route('/votes/comments/<int:pid>', methods=['GET'])
def view_all_vote(pid):
    post = Post.query.filter_by(post_id=pid).first()
    # can be replace by current_user.user_id later, marks for Sean
    uid = request.args.get('user_id', 0, type=int)
    data = dict()
    for comment in post.comments:
        data[comment.comment_id] = uid in [vote.user_id for vote in comment.votes]
    return jsonify(data)


# route for create/canceling vote for a comment
# expects comment_id as input
@bp.route('votes/comment/<int:cid>', methods=['POST'])
def vote(cid):
    # can be replace by current_user.user_id later, marks for Sean
    uid = request.args.get('user_id', 0, type=int)
    old_vote = CommentVote.query.filter_by(comment_id=cid, user_id=uid).first()
    if old_vote:
        Comment.query.filter_by(comment_id=old_vote.comment_id).first().vote_count -= 1
        db.session.delete(old_vote)
        db.session.commit()
        data = old_vote.to_dict()
        data['msg'] = 'old vote deleted!'
        return jsonify(data)
    else:
        new_vote = CommentVote()
        new_vote.comment_id = cid
        new_vote.user_id = uid
        db.session.add(new_vote)
        Comment.query.filter_by(comment_id=new_vote.comment_id).first().vote_count += 1
        db.session.commit()
        data = new_vote.to_dict()
        data['msg'] = 'new vote generated!'
        return jsonify(data)
