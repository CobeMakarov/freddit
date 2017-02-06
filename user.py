from post import post
from misc import misc
from subfreddit import subfreddit

class user:
    id, karma = 0, 0
    email, username, db = "", "", ""

    night = False

    subfreddits = []

    @staticmethod
    def userExists(email, username, db):
        db.getCursor().execute("SELECT id FROM users WHERE email = %s OR username = %s", (email, username))

        count = db.getCursor().rowcount

        return count == 1

    @staticmethod
    def create(email, password, username, night, db):
        db.getCursor().execute(
            "INSERT INTO users (email, password, username, night_mode) VALUES (%s, %s, %s, %s) RETURNING id",
            (email, password, username, night))

        generated = db.getCursor().fetchone()[0]

        db.commit()

        return generated

    def __init__(self, id, db):
        self.db = db

        self.db.getCursor().execute("SELECT username, email, night_mode FROM users WHERE id = %s", (id,))

        row = self.db.getCursor().fetchone()

        self.id = id

        self.username = row[0]
        self.email = row[1]
        self.night = (row[2] == 1)

        self.loadSubfreddits()

    def loadSubfreddits(self):
        print(len(self.subfreddits))
        self.db.getCursor().execute("SELECT subfreddit_id FROM user_subfreddits WHERE user_id = %s", (self.id,))

        rows = self.db.getCursor().fetchall()

        for row in rows:
            sub_id = row["subfreddit_id"]

            sub = subfreddit(sub_id, self.db)

            if not misc.objinlist("path", sub.path, self.subfreddits):
                self.subfreddits.append(sub)

    def calculateKarma(self):
        self.db.getCursor().execute("SELECT sum(vote_count) FROM posts")
        #ok so we need to get the sum of posts.vote_count + the sum of comments.vote_count and combine them using joins
        return 0

    def hasVoted(self, post_id):
        self.db.getCursor().execute("SELECT COUNT(*) FROM user_votes WHERE user_id = %s AND post_id = %s",
                                    (self.id, post_id))

        count = self.db.getCursor().fetchone()

        return count == 1

    def buildFrontPage(self):
        frontPage = []

    def getLatestPosts(self):
        posts = []

        self.db.getCursor.execute("SELECT * FROM posts WHERE user_id = %s ORDER BY DESC LIMIT 5", (self.id,))

        rows = self.db.getCursor().fetchall()

        for row in rows:
            posts.append(post(
                row["id"], row["subfreddit"], row["type"], row["vote_count"], row["title"],
                row["media_url"], row["post_text"], row["date_posted"], self.id, self.db
            ))

        return posts

    def subscribe(self, id):
        self.db.getCursor().execute("INSERT INTO user_subfreddits (user_id, subfreddit_id) VALUES (%s, %s)", (self.id, id))

        self.db.commit()

        self.subfreddits.append(subfreddit(id, self.db))

    def moderate(self, id):
        self.db.getCursor().execute("INSERT INTO subfreddits_moderators (user_id, subfreddit_id) VALUES (%s, %s)",
                                    (self.id, id))

        self.db.commit()
