from app import app, db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import url_for
from datetime import datetime
import jwt
import enum
from sqlalchemy.ext.hybrid import hybrid_property

# this is the function used to achieve pagination


class PaginatedAPIMixin(object):
    @staticmethod
    # def to_collection_dict(query, page, per_page, endpoint, **kwargs):
    def to_collection_dict(query, page, per_page):
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            }
            # '_links': {
            #     'self': url_for(endpoint, page=page, per_page=per_page,
            #                     **kwargs),
            #     'next': url_for(endpoint, page=page + 1, per_page=per_page,
            #                     **kwargs) if resources.has_next else None,
            #     'prev': url_for(endpoint, page=page - 1, per_page=per_page,
            #                     **kwargs) if resources.has_prev else None
            # }
        }
        return data


class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String(64), index=True, unique=True)
    auth0_id = db.Column(db.String(64), index=True, unique=True)
    admin = db.Column(db.Boolean, default=False)
    avatar = db.Column(
        db.String(256), default="http://www.gravatar.com/avatar/?d=mp")
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    comments = db.relationship("Comment", backref='author', lazy="dynamic")
    comment_votes = db.relationship(
        'CommentVote', backref='author', lazy='dynamic')

    def to_dict(self):
        return ({
            "user_id": self.user_id,
            "username": self.username,
            "admin": self.admin,
            "avatar": self.avatar
        })

    def __repr__(self):
        return ("<User {}>".format(self.username))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return (check_password_hash(self.password_hash, password))

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'


class Post(PaginatedAPIMixin, db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), index=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    body = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    last_modify_time = db.Column(db.DateTime, default=datetime.utcnow)
    # here last_moderate_time is to indicate admin action, and when that happened, can use this to filter moderated.
    last_moderate_time = db.Column(db.DateTime)
    approved = db.Column(db.Boolean, default=False)
    archived = db.Column(db.Boolean, default=False)
    admin_msg = db.Column(db.Text)
    comments = db.relationship(
        "Comment", backref='parent_post', lazy="dynamic")

    def __repr__(self):
        return ("<Post {}>".format(self.title))

    def to_dict(self):
        data = {
            'post_id': self.post_id,
            'creator_id': self.creator_id,
            'creator_username': self.author.username,
            'creator_avatar': self.author.avatar,
            'title': self.title,
            'body': self.body,
            'create_time': str(self.create_time.date()),
            'last_modify_time': str(self.last_modify_time),
            'last_moderate_time': str(self.last_moderate_time),
            'approved': self.approved,
            'admin_msg': self.admin_msg,
            'archived': self.archived,
            # 'is_archieved': False,
            # 'comments_count': self.comments.count()
        }
        return data

    def from_dict(self, data, new_post=False):
        for field in ['title', 'body']:
            if field in data:
                setattr(self, field, data[field])
        self.approved = False
        if new_post:
            for field in ['creator_id']:
                if field in data:
                    setattr(self, field, data[field])


class Comment(PaginatedAPIMixin, db.Model):
    # type should be solution, clarification, other or reply
    type = db.Column(db.String)
    comment_id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    body = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    last_modify_time = db.Column(db.DateTime, default=datetime.utcnow)
    last_moderate_time = db.Column(db.DateTime)
    approved = db.Column(db.Boolean, default=False)
    admin_msg = db.Column(db.Text)
    votes = db.relationship('CommentVote', backref='comment', lazy='dynamic')
    vote_count = db.Column(db.Integer, default=0)
    parent_comment_id = db.Column(
        db.Integer, db.ForeignKey('comment.comment_id'))
    parent_comment = db.relationship(
        "Comment",
        back_populates='replies',
        remote_side='Comment.comment_id',
        foreign_keys=[parent_comment_id]
    )
    replies = db.relationship(
        "Comment")

    def __repr__(self):
        return ("<Comment {}>".format(self.body))

    def to_dict(self):
        data = {
            'comment_id': self.comment_id,
            'author_id': self.author_id,
            'body': self.body,
            'create_time': str(self.create_time.date()),
            'type': self.type,
            'parent_comment_id': self.parent_comment_id,
            'replies': [reply.to_dict() for reply in self.replies if reply.approved],
            'creator_username': self.author.username,
            'creator_avatar': self.author.avatar,
            'vote_count': self.votes.count(),
            'approved': self.approved,
            'last_moderate_time': self.last_moderate_time,
            'admin_msg': self.admin_msg,
            'post_id': self.post_id
        }
        return data

    def from_dict(self, data, new_comment=False):
        # for solutions: post id will be required to filter

        for field in ['body']:
            if field in data:
                setattr(self, field, data[field])
        self.approved = False
        # for comments: it requires solution id to filter but not post id
        if new_comment:
            if data['type'] == "reply":
                for field in ['author_id', 'parent_solution_id', 'post_id', 'type']:
                    if field in data:
                        setattr(self, field, data[field])
            else:
                for field in ['author_id', 'post_id', 'type']:
                    if field in data:
                        setattr(self, field, data[field])


#  one-to-many relationship with the voting object and user.
class CommentVote(db.Model):
    vote_id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.comment_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

    def to_dict(self):
        data = {
            'vote_id': self.vote_id,
            'comment_id': self.comment_id,
            'user_id': self.user_id
        }
        return data


@ login.user_loader
def load_user(id):
    return User.query.get(int(id))
