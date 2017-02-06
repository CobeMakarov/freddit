class post:
    id, subfreddit, type, vote_count, user_id = 0, 0, 0, 0, 0
    title, media_url, post_text, date_posted, db = "", "", "", "", ""

    def __init__(self, id, subfreddit, type, vote_count, title, media_url, post_text, date_posted, user_id, db):
        self.id = id
        self.subfreddit = subfreddit
        self.type = type
        self.vote_count = vote_count
        self.user_id = user_id

        self.title = title
        self.media_url = media_url
        self.post_text = post_text
        self.date_posted = date_posted

        self.db = db

    def vote(self, user_id, type):

        if type == 0:
            self.vote_count -= 1
        elif type == 1:
            self.vote_count += 1

        self.db.getCursor().execute("INSERT INTO user_votes (post_id, user_id, type) VALUES (%s, %s, %s)",
                                    (self.id, self.user_id, type)) #add vote count
        self.update()

    def update(self):
        self.db.getCursor().execute("UPDATE posts SET vote_count = %s, post_text = %s WHERE id = %s",
                                    (self.vote_count, self.post_text, self.id))


