from app import db, models
import json
import os
import datetime


def reset_db():
    db.drop_all()
    db.create_all()


file_dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(file_dir, "demo_dat.json")) as f:
    DAT = json.load(f)


def populate_db(dat):
    for user in dat["users"]:
        user_model = models.User(**user)
        db.session.add(user_model)

    db.session.commit()

    for post in dat["posts"]:
        post_model = models.Post(**post)
        if post_model.approved:
            post_model.last_moderate_time = datetime.datetime.now()
        db.session.add(post_model)

    db.session.commit()

    for comment in dat["comments"]:
        comment_model = models.Comment(**comment)
        db.session.add(comment_model)
        # commit each comment as created because of parent relation to self
        db.session.commit()

    for vote in dat["votes"]:
        vote_model = models.CommentVote(**vote)
        db.session.add(vote_model)
        # commit each comment as created because of parent relation to self
        db.session.commit()


if __name__ == '__main__':
    reset_db()
    populate_db(DAT)
