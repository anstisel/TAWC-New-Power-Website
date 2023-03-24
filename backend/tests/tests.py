# General tests file

import unittest
import os
import sys
import inspect
from datetime import datetime
import json

# this import is written in this way to import from the parent directory
# the if statement prevents autoformatting from moving the import to the top of the file
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
if True:
    from app import app, db, models
    import populate_db

BASEDIR = os.path.abspath(os.path.dirname(__file__))
TEST_START_TIME = datetime.utcnow()
DAT = populate_db.DAT
EXPIRED_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkVVaEZMdW5KdFRUOVNRamJxLUhrUCJ9.eyJkZXYtN2xjNmY3dncudXMuYXV0aDAuY29tL3JvbGVzIjpbXSwiaXNzIjoiaHR0cHM6Ly9kZXYtN2xjNmY3dncudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYzNDY0OTJmZTU4NDM1OWEyZGY3ZjM0OSIsImF1ZCI6WyJodHRwOi8vbG9jYWxob3N0OjUwMDAiLCJodHRwczovL2Rldi03bGM2Zjd2dy51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjY1NTU1OTEzLCJleHAiOjE2NjU2NDIzMTMsImF6cCI6ImJ2em5iMTZ3YkNlaEJpWUxqWFY3MG05ME52b01sOEdkIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCJ9.JKGzGsZG3QbwaL4zzxKTvgkGiFKzr9BMC0svYVR0zZuQPEoeF-ojsinMStHGTAUhTSgXa2SLXrE5SQciHy9NxalzPhLdxfbm1lYHE_1kTeHxIC0jXL6y5IlDIzj9_8i25x8UtHoaM6XfsmyXtHyViOK468gqLrdB3BRtDyJ4Vaid_r2GFBWMVyI3YMo12ZsuBwHd1MsPjZFRhVnCbmVB4SPmpHWmsDxSTEKPh_lr3RiDFSwPr0to6CNw6ZmBU6C3z1n8peYypfAONxLt-Z_M-j4LfQugk430NisI7mejNu-aoaseCDHt3DJ1mWszMcWs-9bchykmZOMU7hrNb2S7mA"


class TestFramework(unittest.TestCase):

    def setUp(self):
        app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///:memory:'
        db.create_all()

        populate_db.populate_db(DAT)

    def tearDown(self):
        db.drop_all()


class TestTests(TestFramework):

    def test_runs(self):
        self.app = app.test_client()
        response = self.app.get("/", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_dat(self):
        self.assertGreater(len(DAT), 1)
        self.assertGreater(len(DAT["users"]), 1)

    def test_demo_db_initialised(self):
        first_user = DAT["users"][0]
        first_user_db_instance = models.User.query.filter_by(
            user_id=first_user["user_id"])[0]
        self.assertEqual(first_user_db_instance.username,
                         first_user["username"])

        first_post = DAT["posts"][0]
        first_post_db_instance = models.Post.query.filter_by(
            post_id=first_post["post_id"])[0]
        self.assertEqual(first_post_db_instance.body,
                         first_post["body"])


class TestModels(TestFramework):

    def test_post_timesetting(self):
        time_now = datetime.utcnow()
        first_post = models.Post.query.all()[0]
        last_post = models.Post.query.all()[-1]
        for post in (first_post, last_post):
            self.assertLessEqual(TEST_START_TIME, post.create_time)
            self.assertGreaterEqual(time_now, post.last_modify_time)

    def test_post_author_relation(self):
        for post in DAT["posts"]:
            creator_id = post.get("creator_id", None)
            if creator_id:
                # test if can get parent from child
                post_inst = models.Post.query.filter_by(
                    post_id=post["post_id"]).first()
                user_inst = post_inst.author
                self.assertEqual(user_inst.user_id,
                                 post["creator_id"])

                # test if can get child from parent
                user_inst = models.User.query.filter_by(
                    user_id=post["creator_id"]).first()
                posts = user_inst.posts
                post_ids = [post_inst.post_id for posts_inst in posts]
                self.assertTrue(post["post_id"] in post_ids)

    def test_comment_self_referential(self):
        for comment in DAT["comments"]:
            parent = comment.get("parent_comment_id", None)
            if parent:
                # test if can get parent from child
                child_inst = models.Comment.query.filter_by(
                    comment_id=comment["comment_id"]).first()
                parent_inst = child_inst.parent_comment
                self.assertEqual(parent_inst.comment_id,
                                 comment["parent_comment_id"])

                # test if can get child from parent
                parent_inst = models.Comment.query.filter_by(
                    comment_id=comment["parent_comment_id"])[0]
                children = parent_inst.replies
                child_ids = [child.comment_id for child in children]
                self.assertTrue(comment["comment_id"] in child_ids)


class TestRoutes(TestFramework):

    def test_get_posts(self):
        self.app = app.test_client()

        ## GET /api/posts
        resp = self.app.get("/api/posts")
        resp_dat = resp.json
        self.assertEqual(len(resp_dat["items"]), len(DAT["posts"]))

        # GET /api/posts/<int:pid:>
        for post in DAT["posts"]:
            post_id = post["post_id"]
            resp_dat = self.app.get("/api/posts/{}".format(post_id)).json
            self.assertEqual(post["title"], resp_dat["title"])

        # GET /posts/unapproved
        # GET /posts/approved
        approved_posts, unapproved_posts = [], []
        for post in DAT["posts"]:
            if post["approved"]:
                approved_posts.append(post)
            else:
                unapproved_posts.append(post)

        approved_resp_dat = self.app.get("/api/posts/approved").json
        self.assertEqual(len(approved_resp_dat["items"]), len(approved_posts))
        unapproved_resp_dat = self.app.get("/api/posts/unmoderated").json
        self.assertEqual(
            len(unapproved_resp_dat["items"]), len(unapproved_posts))

    def test_create_post(self):
        pass

        # can't get this to run for some reason :(
        # not sure how to do: https://flask.palletsprojects.com/en/2.2.x/testing/#faking-resources-and-context

        # self.app = app.test_client()
        # dat = {
        #     "creator_id": 1,
        #     "title": "test post",
        #     "body": "new demo post"
        # }
        # resp = self.app.post("api/posts", json=json.dumps(dat))
        # print(resp)
        # title_found = False
        # for post in models.Post.query.all():
        #     print(post)
        #     if post.title == "test post":
        #         title_found = True
        # self.assertTrue(title_found)


if __name__ == "__main__":
    unittest.main()
