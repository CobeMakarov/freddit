
class comment:

    @staticmethod
    def update_vote(post_id, vote, db, jump=False):
        if int(vote) is 1:
            num = 1

            if jump:
                num = 2

            db.get_cursor().execute("UPDATE comments SET vote_count = vote_count + %s WHERE id = %s", (num, post_id))
        else:
            num = 1

            if jump:
                num = 2

            db.get_cursor().execute("UPDATE comments SET vote_count = vote_count - %s WHERE id = %s", (num, post_id))
        db.commit()

    def __init__(self, id, db, post_id=0, parent=0, vote_count=0, user_id=0, text=None, date_posted=None):
        from user import user

        self.id = id
        self.db = db

        if post_id is 0:
            self.db.get_cursor().execute("SELECT * FROM comments WHERE id = %s", (self.id,))

            p = self.db.get_cursor().fetchone()
            count = self.db.get_cursor().rowcount

            if count == 0:
                post_id = 0
            else:
                self.post_id = p["post_id"]
                self.parent = p["parent"]
                self.vote_count = p["vote_count"]

                self.text = p["text"]
                self.date_posted = p["date_posted"]

                self.user = user(p["user_id"], self.db)
        else:
            self.post_id = post_id
            self.parent = parent
            self.vote_count = vote_count

            self.text = text
            self.date_posted = date_posted

            self.user = user(user_id, self.db)

    def update(self):
        self.db.get_cursor().execute("UPDATE comments SET vote_count = %s, text = %s WHERE id = %s",
                                     (self.vote_count, self.text, self.id))

    def get_post_title(self):
        self.db.get_cursor().execute("SELECT title FROM posts WHERE id = %s", (self.post_id, ))

        return self.db.get_cursor().fetchone()[0]

