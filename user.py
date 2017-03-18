from misc import misc
from post import post
from subfreddit import subfreddit


class user:
    id, karma, admin = 0, 0, 0
    email, username, db = "", "", ""

    night = False

    subfreddits = []

    @staticmethod
    def exists(email, username, db):
        db.getCursor().execute("SELECT id FROM users WHERE email = %s OR username = %s", (email, username))

        count = db.getCursor().rowcount

        return count == 1 or count == 2

    @staticmethod
    def create(email, password, username, night, db):
        db.getCursor().execute(
            "INSERT INTO users (email, password, username, night_mode) VALUES (%s, %s, %s, %s) RETURNING id",
            (email, password, username, night))

        generated = db.getCursor().fetchone()[0]

        db.commit()

        return generated

    @staticmethod
    def get_karma_by_id(db, id):
        db.getCursor().execute("SELECT sum(vote_count) FROM "
                               "(SELECT vote_count FROM posts WHERE soft_deleted = 0 AND user_id = %s UNION ALL SELECT vote_count FROM comments WHERE user_id = %s) t",
                               (id, id))

        calculation = db.getCursor().fetchone()[0]

        if calculation is None:
            calculation = 0
        #ok so we need to get the sum of posts.vote_count + the sum of comments.vote_count and combine them using joins
        return calculation

    def __init__(self, id, db):
        self.db = db

        self.db.getCursor().execute("SELECT * FROM users WHERE id = %s", (id,))

        row = self.db.getCursor().fetchone()

        self.id = id

        self.username = row["username"]
        self.email = row["email"]
        self.night = (row["night_mode"] == 1)

        self.admin = (row["admin"] == 1)

        self.subfreddits = []

        self.load_subs()
        self.karma = self.calculate_karma()

    def load_subs(self):
        self.db.getCursor().execute("SELECT subfreddit_id FROM user_subfreddits WHERE user_id = %s", (self.id,))

        rows = self.db.getCursor().fetchall()

        for row in rows:
            sub_id = row["subfreddit_id"]

            sub = subfreddit(sub_id, self.db)

            if not misc.obj_exists_key("path", sub.path, self.subfreddits):  ##lazy fix for .. code
                self.subfreddits.append(sub)

    def calculate_karma(self):
        self.db.getCursor().execute("SELECT sum(vote_count) FROM "
                                    "(SELECT vote_count FROM posts WHERE soft_deleted = 0 AND user_id = %s UNION ALL SELECT vote_count FROM comments WHERE user_id = %s) t",
                                    (self.id, self.id))

        calculation = self.db.getCursor().fetchone()[0]

        if calculation is None:
            calculation = 0
        #ok so we need to get the sum of posts.vote_count + the sum of comments.vote_count and combine them using joins
        return calculation

    def vote(self, id, vote, is_post):
        if is_post:
            self.db.getCursor().execute("INSERT INTO user_votes_posts (post_id, user_id, vote) VALUES (%s, %s, %s)",
                                    (id, self.id, vote))  # add vote count
        else:
            self.db.getCursor().execute("INSERT INTO user_votes_comments (comment_id, user_id, vote) VALUES (%s, %s, %s)",
                                        (id, self.id, vote))  # add vote count
        self.db.commit()

    def has_voted(self, id, is_post):

        if is_post:
            self.db.getCursor().execute("SELECT vote FROM user_votes_posts WHERE user_id = %s AND post_id = %s",
                                    (self.id, id))
        else:
            self.db.getCursor().execute("SELECT vote FROM user_votes_comments WHERE user_id = %s AND comment_id = %s",
                                        (self.id, id))

        if self.db.getCursor().rowcount == 0:
            return -1

        vote = self.db.getCursor().fetchone()[0]

        return vote

    def update_vote(self, id, vote, is_post):
        if is_post:
            self.db.getCursor().execute("UPDATE user_votes_posts SET vote = %s WHERE user_id = %s AND post_id = %s",
                                        (vote, self.id, id))
        else:
            self.db.getCursor().execute("UPDATE user_votes_comments SET vote = %s WHERE user_id = %s AND comment_id = %s",
                                        (self.id, id))
        self.db.commit()

    def build_frontpage(self):
        #posted in last 3 hours
        #karma > 5
        #max 25 posts
        #sort by random

        id_list = []
        front_page = []

        for subs in self.subfreddits:
            id_list.append(subs.id)

        self.db.getCursor().execute("SELECT * FROM posts WHERE soft_deleted = 0 AND subfreddit = ANY(%s) AND date_posted <= "
                                    "(now()::timestamp + INTERVAL '24 HOURS')", (id_list,))

        rows = self.db.getCursor().fetchall()

        for row in rows:
            front_page.append(post(row["id"], self.db, row["subfreddit"], row["type"], row["vote_count"], row["sticky"], row["title"],
                              row["media_url"], row["post_text"], row["date_posted"], row["user_id"]))

        return front_page

    def get_latestposts(self):
        posts = []

        self.db.getCursor().execute("SELECT * FROM posts WHERE soft_deleted = 0 AND user_id = %s ORDER BY DESC LIMIT 5", (self.id,))

        rows = self.db.getCursor().fetchall()

        for row in rows:
            posts.append(post(
                row["id"], row["subfreddit"], row["type"], row["vote_count"], row["sticky"], row["title"],
                row["media_url"], row["post_text"], row["date_posted"], self.id, self.db
            ))

        return posts

    def subscribe(self, id):
        if not misc.obj_exists_key("id", id, self.subfreddits):
            self.db.getCursor().execute("INSERT INTO user_subfreddits (user_id, subfreddit_id) VALUES (%s, %s)",
                                        (self.id, id))

            self.db.commit()

            self.subfreddits.append(subfreddit(id, self.db))

    def unsubscribe(self, id):
        if misc.obj_exists_key("id", id, self.subfreddits):
            self.db.getCursor().execute("DELETE FROM user_subfreddits WHERE user_id = %s AND subfreddit_id = %s", (self.id, id))

            self.db.commit()

            misc.remove_by_key('id', id, self.subfreddits)

    def moderate(self, id):
        self.db.getCursor().execute("INSERT INTO subfreddits_moderators (user_id, subfreddit_id) VALUES (%s, %s)",
                                    (self.id, id))

        self.db.commit()

    def is_subscribed(self, sub_id):
        return misc.obj_exists_key("id", sub_id, self.subfreddits)

    def post(self, sub_id, title, type, text, media):
        self.db.getCursor().execute("INSERT INTO posts (title, subfreddit, type, post_text, media_url, user_id) "
                                    "VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
                                    (title, sub_id, type, text, media, self.id))

        generated = self.db.getCursor().fetchone()[0]

        self.db.commit()

        return generated

    def comment(self, post_id, parent, comment):
        self.db.getCursor().execute("INSERT INTO comments (post_id, parent, text, user_id) "
                                    "VALUES (%s, %s, %s, %s) RETURNING id", (post_id, parent, comment, self.id))

        generated = self.db.getCursor().fetchone()[0]

        self.db.commit()

        return generated

    def is_mod(self, sub_id):
        self.db.getCursor().execute("SELECT COUNT(*) FROM subfreddits_moderators WHERE subfreddit_id = %s AND user_id = %s",
                                    (sub_id, self.id))

        count = self.db.getCursor().fetchone()[0]

        return count > 0



