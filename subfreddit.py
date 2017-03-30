from moderator import moderator
from post import post


class subfreddit:
    @staticmethod
    def create(path, title, creator_id, private, desc, db):
        db.get_cursor().execute("INSERT INTO subfreddits (path, title, creator_id, private, description) "
                                "VALUES (%s, %s, %s, %s, %s) RETURNING id",
                                (path, title, creator_id, private, desc))

        generated = db.get_cursor().fetchone()[0]

        db.commit()

        return generated

    @staticmethod
    def get_path(id, db):
        db.get_cursor().execute("SELECT path FROM subfreddits WHERE id = %s", (id,))

        path = db.get_cursor().fetchone()[0]

        return path

    @staticmethod
    def discover(db, sort=None):
        subs = []
        if sort is None:
            db.get_cursor().execute("SELECT subfreddits.*, COUNT(user_subfreddits.*) AS sub_count "
                                    "FROM subfreddits LEFT JOIN user_subfreddits ON subfreddits.id = user_subfreddits.subfreddit_id "
                                    "GROUP BY subfreddits.id ORDER BY sub_count DESC LIMIT 10")
        else:
            if sort == "new":
                db.get_cursor().execute("SELECT * FROM subfreddits ORDER BY id DESC LIMIT 10")

        rows = db.get_cursor().fetchall()

        for row in rows:
            subs.append(subfreddit(row["id"], db, row["path"], row["title"], row["creator_id"],
                                   row["description"], row["subscriber_name"], row["header_background"],
                                   row["header_text"]))

        return subs

    def __init__(self, id, db, path=None, title=None, creator=None, desc=None, subscriber_name=None, header_background=None, header_text=None):
        self.db = db
        self.moderators = []
        self.moderators_ids = []

        if path is not None and id == 0:
            self.path = path

            self.db.get_cursor().execute("SELECT * FROM subfreddits WHERE path = %s", (path,))

            row = self.db.get_cursor().fetchone()

            if self.db.get_cursor().rowcount == 0:
                return None  ##FIX DIS

            self.id = row["id"]

            self.title = row["title"]
            self.desc = row["description"]

            self.creator_id = row["creator_id"]
            self.subscriber_name = row["subscriber_name"]
            self.header_background = row["header_background"]
            self.header_text = row["header_text"]
        else:
            self.id = id

            if path is None and title is None and creator is None and desc is None:
                self.db.get_cursor().execute("SELECT * FROM subfreddits WHERE id = %s", (self.id,))

                row = self.db.get_cursor().fetchone()

                self.path = row["path"]
                self.title = row["title"]
                self.desc = row["description"]

                self.creator_id = row["creator_id"]
                self.subscriber_name = row["subscriber_name"]
                self.header_background = row["header_background"]
                self.header_text = row["header_text"]
            else:
                self.id = id
                self.path = path
                self.title = title
                self.desc = desc

                self.creator_id = creator
                self.subscriber_name = subscriber_name
                self.header_background = header_background
                self.header_text = header_text

                self.db = db

        if self.header_background is None:
            self.header_background = ""

        if self.header_text is None:
            self.header_text = ""

        self.load_moderators()

    def get_posts(self, sort):
        posts = []

        if sort == "hot":
            self.db.get_cursor().execute("SELECT * FROM posts WHERE soft_deleted = 0 AND sticky = 0 AND subfreddit = %s AND date_posted <= "
                                         "(now()::timestamp + INTERVAL '3 HOURS') LIMIT 20", (self.id, ))

        if sort == "new":
            self.db.get_cursor().execute("SELECT * FROM posts WHERE soft_deleted = 0 AND sticky = 0 AND subfreddit = %s ORDER BY date_posted DESC LIMIT 20", (self.id,))

        if sort == "top":
            self.db.get_cursor().execute("SELECT * FROM posts WHERE soft_deleted = 0 AND sticky = 0 AND subfreddit = %s ORDER BY vote_count DESC LIMIT 20",
                                         (self.id,))

        rows = self.db.get_cursor().fetchall()

        for row in rows:
            posts.append(post(row["id"], self.db, self.id, row["type"], row["vote_count"], row["sticky"], row["title"],
                              row["media_url"], row["post_text"], row["date_posted"], row["user_id"]))

        return posts

    def get_subscribe_count(self):
        self.db.get_cursor().execute("SELECT COUNT(*) FROM user_subfreddits WHERE subfreddit_id = %s", (self.id,))

        count = self.db.get_cursor().fetchone()[0]

        return count

    def is_owner(self, user_id):
        return self.creator_id == user_id

    def get_sticky_post(self):
        self.db.get_cursor().execute("SELECT id FROM posts WHERE soft_deleted = 0 AND subfreddit = %s AND sticky = 1", (self.id,))

        if self.db.get_cursor().rowcount == 1:
            post_id = self.db.get_cursor().fetchone()[0]
            return post(post_id, self.db)

        return None

    def load_moderators(self):
        self.db.get_cursor().execute("SELECT users.id, users.username FROM users "
                                     "JOIN subfreddits_moderators ON subfreddits_moderators.user_id = users.id "
                                     "WHERE subfreddits_moderators.subfreddit_id = %s", (self.id, ))

        rows = self.db.get_cursor().fetchall()

        for row in rows:
            mod = moderator(row["id"], row["username"], self.id, self.db)

            if mod.id not in [s.id for s in self.moderators]:
                self.moderators.append(mod)
                self.moderators_ids.append(mod.id)

    def add_moderator(self, mod):
        if mod.id not in [s.id for s in self.moderators]:
            self.db.get_cursor().execute("INSERT INTO subfreddits_moderators (subfreddit_id, user_id) VALUES (%s, %s)", (self.id, mod.id))
            self.db.commit()

            self.moderators.append(mod)
            self.moderators_ids.append(mod.id)

    def remove_moderator(self, id):
        self.db.get_cursor().execute("DELETE FROM subfreddits_moderators WHERE subfreddit_id = %s AND user_id = %s", (self.id, id))
        self.db.commit()

    def save(self):
        self.db.get_cursor().execute("UPDATE subfreddits SET title = %s, description = %s, header_background = %s, header_text = %s WHERE id = %s",
                                    (self.title, self.desc, self.header_background, self.header_text, self.id))
        self.db.commit()
