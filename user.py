from collections import OrderedDict

from comment import comment
from misc import misc
from post import post
from subfreddit import subfreddit


class user:
    @staticmethod
    def exists(email, username, db):
        db.get_cursor().execute("SELECT id FROM users WHERE email = %s OR username = %s", (email, username))

        count = db.get_cursor().rowcount

        return count == 1 or count == 2

    @staticmethod
    def create(email, password, username, night, db):
        db.get_cursor().execute(
            "INSERT INTO users (email, password, username, night_mode) VALUES (%s, %s, %s, %s) RETURNING id",
            (email, password, username, night))

        generated = db.get_cursor().fetchone()[0]

        db.commit()

        return generated

    @staticmethod
    def get_id_by_username(username, db):
        db.get_cursor().execute("SELECT id FROM users WHERE username = %s", (username, ))

        if db.get_cursor().rowcount == 0:
            return 0

        user_id = db.get_cursor().fetchone()[0]

        return user_id

    @staticmethod
    def get_karma_by_id(db, id):
        db.get_cursor().execute("SELECT sum(vote_count) FROM "
                                "(SELECT vote_count FROM posts WHERE soft_deleted = 0 AND user_id = %s UNION ALL SELECT vote_count FROM comments WHERE user_id = %s) t",
                                (id, id))

        calculation = db.get_cursor().fetchone()[0]

        if calculation is None:
            calculation = 0
        #ok so we need to get the sum of posts.vote_count + the sum of comments.vote_count and combine them using joins
        return calculation

    def __init__(self, id, db):
        self.db = db

        self.subfreddits = []

        self.db.get_cursor().execute("SELECT * FROM users WHERE id = %s", (id,))

        row = self.db.get_cursor().fetchone()

        self.id = id

        self.username = row["username"]
        self.email = row["email"]
        self.night = (row["night_mode"] == 1)

        self.admin = (row["admin"] == 1)

        self.subfreddits = []

        self.load_subs()
        self.karma = self.calculate_karma()

    def load_subs(self):
        self.db.get_cursor().execute("SELECT subfreddit_id FROM user_subfreddits WHERE user_id = %s", (self.id,))

        rows = self.db.get_cursor().fetchall()

        for row in rows:
            sub_id = row["subfreddit_id"]

            sub = subfreddit(sub_id, self.db)

            if sub.id not in [s.id for s in self.subfreddits]:
                self.subfreddits.append(sub)

    def calculate_karma(self):
        self.db.get_cursor().execute("SELECT sum(vote_count) FROM "
                                     "(SELECT vote_count FROM posts WHERE soft_deleted = 0 AND user_id = %s UNION ALL SELECT vote_count FROM comments WHERE user_id = %s) t",
                                     (self.id, self.id))

        calculation = self.db.get_cursor().fetchone()[0]

        if calculation is None:
            calculation = 0
        #ok so we need to get the sum of posts.vote_count + the sum of comments.vote_count and combine them using joins
        return calculation

    def vote(self, id, vote, is_post):
        if is_post:
            self.db.get_cursor().execute("INSERT INTO user_votes_posts (post_id, user_id, vote) VALUES (%s, %s, %s)",
                                         (id, self.id, vote))  # add vote count
        else:
            self.db.get_cursor().execute("INSERT INTO user_votes_comments (comment_id, user_id, vote) VALUES (%s, %s, %s)",
                                         (id, self.id, vote))  # add vote count
        self.db.commit()

    def has_voted(self, id, is_post):

        if is_post:
            self.db.get_cursor().execute("SELECT vote FROM user_votes_posts WHERE user_id = %s AND post_id = %s",
                                         (self.id, id))
        else:
            self.db.get_cursor().execute("SELECT vote FROM user_votes_comments WHERE user_id = %s AND comment_id = %s",
                                         (self.id, id))

        if self.db.get_cursor().rowcount == 0:
            return -1

        vote = self.db.get_cursor().fetchone()[0]

        return vote

    def update_vote(self, id, vote, is_post):
        if is_post:
            self.db.get_cursor().execute("UPDATE user_votes_posts SET vote = %s WHERE user_id = %s AND post_id = %s",
                                         (vote, self.id, id))
        else:
            self.db.get_cursor().execute("UPDATE user_votes_comments SET vote = %s WHERE user_id = %s AND comment_id = %s",
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

        self.db.get_cursor().execute("SELECT * FROM posts WHERE soft_deleted = 0 AND subfreddit = ANY(%s) AND date_posted <= "
                                    "(now()::timestamp + INTERVAL '24 HOURS')", (id_list,))

        rows = self.db.get_cursor().fetchall()

        for row in rows:
            front_page.append(post(row["id"], self.db, row["subfreddit"], row["type"], row["vote_count"], row["sticky"], row["title"],
                              row["media_url"], row["post_text"], row["date_posted"], row["user_id"]))

        return front_page

    def get_posts(self, sort, limit):
        posts = []

        if sort == "top":
            self.db.get_cursor().execute("SELECT * FROM posts WHERE soft_deleted = 0 AND user_id = %s ORDER BY vote_count DESC LIMIT " + str(limit), (self.id,))
        elif sort == "new":
            self.db.get_cursor().execute("SELECT * FROM posts WHERE soft_deleted = 0 AND user_id = %s ORDER BY id DESC LIMIT " + str(limit), (self.id,))

        rows = self.db.get_cursor().fetchall()

        for row in rows:
            posts.append(post(
                row["id"], self.db, row["subfreddit"], row["type"], row["vote_count"], row["sticky"], row["title"],
                row["media_url"], row["post_text"], row["date_posted"], self.id
            ))

        return posts

    def get_comments(self, sort, limit):
        comments = []

        if sort == "top":
            self.db.get_cursor().execute("SELECT * FROM comments WHERE user_id = %s ORDER BY vote_count DESC LIMIT " + str(limit), (self.id,))
        elif sort == "new":
            self.db.get_cursor().execute("SELECT * FROM comments WHERE user_id = %s ORDER BY id DESC LIMIT " + str(limit), (self.id,))

        rows = self.db.get_cursor().fetchall()

        for row in rows:
            comments.append(comment(
                row["id"], self.db, row["post_id"], row["parent"],
                row["vote_count"], self.id, row["text"], row["date_posted"]
            ))

        return comments

    def get_submission_stats(self):
        statistics_draft = OrderedDict()
        statistics = OrderedDict()

        # set default for every subfreddit subscribed to
        for sub in self.subfreddits:
            statistics_draft[sub.id] = 0
            statistics[sub.path] = 0

        # gather post stats
        self.db.get_cursor().execute("SELECT id, subfreddit FROM posts WHERE soft_deleted = 0 AND user_id = %s", (self.id, ))

        posts = self.db.get_cursor().fetchall()

        for post in posts:
            statistics_draft[post["subfreddit"]] += 1

        # gather comment stats
        self.db.get_cursor().execute("SELECT comments.id, subfreddit FROM posts JOIN comments ON comments.post_id = posts.id WHERE comments.user_id = %s",
                                     (self.id,))

        comments = self.db.get_cursor().fetchall()

        for comment in comments:
            statistics_draft[comment["subfreddit"]] += 1

        # iterate through stat draft and place them into the proper stat dictionary
        for sub_id in statistics_draft.iterkeys():
            sub_it = next((x for x in self.subfreddits if x.id == sub_id), None)

            if sub_it is not None:  ## we found the sub associated with the sub_id, lets move this dictionary over
                statistics[sub_it.path] = statistics_draft[sub_id]

        return OrderedDict(sorted(statistics.items(), key=lambda t: t[1], reverse=True))

    def get_moderated_subs(self):
        moderated = []

        for sub in self.subfreddits:
            if self.id in sub.moderators:
                moderated.append(sub)

        return moderated

    def subscribe(self, id):
        if int(id) not in [s.id for s in self.subfreddits]:
            self.db.get_cursor().execute("INSERT INTO user_subfreddits (user_id, subfreddit_id) VALUES (%s, %s)",
                                         (self.id, id))

            self.db.commit()

            self.subfreddits.append(subfreddit(id, self.db))
            return None

    def unsubscribe(self, id):
        id = int(id)

        if id in [s.id for s in self.subfreddits]:

            unsub = next((x for x in self.subfreddits if x.id == id), None)

            if unsub.creator_id != self.id:

                self.db.get_cursor().execute("DELETE FROM user_subfreddits WHERE user_id = %s AND subfreddit_id = %s", (self.id, id))

                self.db.commit()

                misc.remove_by_key('id', id, self.subfreddits)

    def moderate(self, id):
        self.db.get_cursor().execute("INSERT INTO subfreddits_moderators (user_id, subfreddit_id) VALUES (%s, %s)",
                                     (self.id, id))

        self.db.commit()

    def is_subscribed(self, sub_id):
        return sub_id in [sub.id for sub in self.subfreddits]

    def post(self, sub_id, title, type, text, media):
        self.db.get_cursor().execute("INSERT INTO posts (title, subfreddit, type, post_text, media_url, user_id) "
                                     "VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
                                     (title, sub_id, type, text, media, self.id))

        generated = self.db.get_cursor().fetchone()[0]

        self.db.commit()

        return generated

    def comment(self, post_id, parent, comment):
        self.db.get_cursor().execute("INSERT INTO comments (post_id, parent, text, user_id) "
                                     "VALUES (%s, %s, %s, %s) RETURNING id", (post_id, parent, comment, self.id))

        generated = self.db.get_cursor().fetchone()[0]

        self.db.commit()

        return generated

    def is_mod(self, sub_id):
        self.db.get_cursor().execute("SELECT COUNT(*) FROM subfreddits_moderators WHERE subfreddit_id = %s AND user_id = %s",
                                     (sub_id, self.id))

        count = self.db.get_cursor().fetchone()[0]

        return count > 0

    def flush(self):
        print("[Site Log] " + self.username + " has triggered an account flush")

        self.db.get_cursor().execute("SELECT night_mode, admin FROM users WHERE id = %s", (self.id,))

        row = self.db.get_cursor().fetchone()

        self.night = (row["night_mode"] == 1)

        self.admin = (row["admin"] == 1)

        self.subfreddits = []

        self.load_subs()
        self.karma = self.calculate_karma()



