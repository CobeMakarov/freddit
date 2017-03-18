from post import post

class subfreddit:
    id, creator_id = 0, 0
    path, title, desc, subscriber_name, db = "", "", "", "", ""

    moderators = []

    @staticmethod
    def create(path, title, creator_id, private, desc, db):
        db.getCursor().execute("INSERT INTO subfreddits (path, title, creator_id, private, description) "
                               "VALUES (%s, %s, %s, %s, %s) RETURNING id",
                               (path, title, creator_id, private, desc))

        generated = db.getCursor().fetchone()[0]

        db.commit()

        return generated

    @staticmethod
    def get_path(id, db):
        db.getCursor().execute("SELECT path FROM subfreddits WHERE id = %s", (id, ))

        path = db.getCursor().fetchone()[0]

        return path

    @staticmethod
    def discover(db, sort=None):
        subs = []
        if sort is None:
            db.getCursor().execute("SELECT subfreddits.*, COUNT(user_subfreddits.*) AS sub_count "
                                   "FROM subfreddits LEFT JOIN user_subfreddits ON subfreddits.id = user_subfreddits.subfreddit_id "
                                   "GROUP BY subfreddits.id ORDER BY sub_count DESC LIMIT 10")
        else:
            if sort == "new":
                db.getCursor().execute("SELECT * FROM subfreddits ORDER BY id DESC LIMIT 10")

        rows = db.getCursor().fetchall()

        for row in rows:
            subs.append(subfreddit(row["id"], db, row["path"], row["title"], row["creator_id"],
                                   row["description"], row["subscriber_name"]))

        print len(subs)

        return subs

    def __init__(self, id, db, path=None, title=None, creator=None, desc=None, subscriber_name=None):
        self.db = db

        if path is not None and id == 0:
            self.path = path

            self.db.getCursor().execute("SELECT * FROM subfreddits WHERE path = %s", (path,))

            row = self.db.getCursor().fetchone()

            if self.db.getCursor().rowcount == 0:
                return None  ##FIX DIS

            self.id = row["id"]

            self.title = row["title"]
            self.desc = row["description"]

            self.creator_id = row["creator_id"]
            self.subscriber_name = row["subscriber_name"]
        else:
            self.id = id

            if path is None and title is None and creator is None and desc is None:
                self.db.getCursor().execute("SELECT * FROM subfreddits WHERE id = %s", (self.id,))

                row = self.db.getCursor().fetchone()

                self.path = row["path"]
                self.title = row["title"]
                self.desc = row["description"]

                self.creator_id = row["creator_id"]
                self.subscriber_name = row["subscriber_name"]
            else:
                self.id = id
                self.path = path
                self.title = title
                self.desc = desc

                self.creator_id = creator
                self.subscriber_name = subscriber_name

                self.db = db

    def get_posts(self, sort):
        posts = []

        if sort == "hot":
            self.db.getCursor().execute("SELECT * FROM posts WHERE soft_deleted = 0 AND sticky = 0 AND subfreddit = %s AND date_posted <= "
                                        "(now()::timestamp + INTERVAL '3 HOURS') LIMIT 20", (self.id, ))

        if sort == "new":
            self.db.getCursor().execute("SELECT * FROM posts WHERE soft_deleted = 0 AND sticky = 0 AND subfreddit = %s ORDER BY date_posted DESC LIMIT 20", (self.id,))

        if sort == "top":
            self.db.getCursor().execute("SELECT * FROM posts WHERE soft_deleted = 0 AND sticky = 0 AND subfreddit = %s ORDER BY vote_count DESC LIMIT 20",
                                        (self.id,))

        rows = self.db.getCursor().fetchall()

        for row in rows:
            posts.append(post(row["id"], self.db, self.id, row["type"], row["vote_count"], row["sticky"], row["title"],
                              row["media_url"], row["post_text"], row["date_posted"], row["user_id"]))

        return posts

    def get_subscribe_count(self):
        self.db.getCursor().execute("SELECT COUNT(*) FROM user_subfreddits WHERE subfreddit_id = %s", (self.id, ))

        count = self.db.getCursor().fetchone()[0]

        return count

    def is_owner(self, user_id):
        return self.creator_id == user_id

    def get_sticky_post(self):
        self.db.getCursor().execute("SELECT id FROM posts WHERE soft_deleted = 0 AND subfreddit = %s AND sticky = 1", (self.id, ))

        if self.db.getCursor().rowcount == 1:
            post_id = self.db.getCursor().fetchone()[0]
            return post(post_id, self.db)

        return None
