from comment import comment
from misc import misc


class post:
    id, subfreddit, type, vote_count, user_id, is_sticky = 0, 0, 0, 0, 0, 0
    title, media_url, post_text, date_posted, db = "", "", "", "", ""

    comments = []

    @staticmethod
    def update_vote(post_id, vote, db, jump=False):
        if int(vote) is 1:
            num = 1

            if jump:
                num = 2

            db.getCursor().execute("UPDATE posts SET vote_count = vote_count + %s WHERE id = %s", (num, post_id))
        else:
            num = 1

            if jump:
                num = 2

            db.getCursor().execute("UPDATE posts SET vote_count = vote_count - %s WHERE id = %s", (num, post_id))
        db.commit()

    def __init__(self, id, db, subfreddit=None, type=0, vote_count=0, sticky=0,
                 title=None, media_url=None, post_text=None, date_posted=None, user_id=0):
        self.id = id
        self.db = db

        if subfreddit is None:
            self.db.getCursor().execute("SELECT * FROM posts WHERE id = %s", (self.id, ))

            p = self.db.getCursor().fetchone()
            count = self.db.getCursor().rowcount

            if count == 0:
                subfreddit = None
            else :
                self.subfreddit = p["subfreddit"]
                self.type = p["type"]
                self.vote_count = p["vote_count"]
                self.user_id = p["user_id"]
                self.is_sticky = p["sticky"]

                self.title = p["title"]
                self.media_url = p["media_url"]
                self.post_text = p["post_text"]
                self.date_posted = p["date_posted"]
        else:
            self.subfreddit = subfreddit
            self.type = type
            self.vote_count = vote_count
            self.user_id = user_id
            self.is_sticky = sticky

            self.title = title
            self.media_url = media_url
            self.post_text = post_text
            self.date_posted = date_posted

        if self.subfreddit is not None:
            self.load_comments("top")

    def load_comments(self, sort):
        self.comments = []

        extra = ""

        if sort is "top":
            extra = " ORDER BY vote_count DESC"

        if sort is "new":
            extra = " ORDER BY date_posted DESC"

        self.db.getCursor().execute("SELECT id FROM comments WHERE post_id = %s" + extra, (self.id,))

        rows = self.db.getCursor().fetchall()

        for row in rows:
            comment_id = row["id"]

            cmt = comment(comment_id, self.db)

            if not misc.obj_exists_key("id", cmt.id, self.comments):  ##lazy fix for .. code
                self.comments.append(cmt)

    def update(self):
        self.db.getCursor().execute("UPDATE posts SET vote_count = %s, post_text = %s, sticky = %s WHERE id = %s",
                                    (self.vote_count, self.post_text, self.is_sticky, self.id))

        self.db.commit()

    def get_subfreddit_path(self):
        self.db.getCursor().execute("SELECT path FROM subfreddits WHERE id = %s", (self.subfreddit,))

        path = self.db.getCursor().fetchone()[0]

        return path

    def get_user_name(self):
        self.db.getCursor().execute("SELECT username FROM users WHERE id = %s", (self.user_id,))

        name = self.db.getCursor().fetchone()[0]

        return name

    def get_comment_count(self):
        self.db.getCursor().execute("SELECT COUNT(*) FROM comments WHERE post_id = %s", (self.id, ))

        count = self.db.getCursor().fetchone()[0]

        return count

    def sticky(self):
        if self.is_sticky == 0:
            self.db.getCursor().execute("UPDATE posts SET sticky = 0 WHERE subfreddit = %s AND sticky = 1", (self.subfreddit,))

            self.db.commit()

            self.is_sticky = 1
            self.update()

    def unsticky(self):
        if self.is_sticky == 1:
            self.is_sticky = 0
            self.update()

    def delete(self):
        self.db.getCursor().execute("UPDATE posts SET soft_deleted = 1 WHERE id = %s", (self.id,))

        self.db.commit()

    def undelete(self):
        self.db.getCursor().execute("UPDATE posts SET soft_deleted = 0 WHERE id = %s", (self.id,))

        self.db.commit()
