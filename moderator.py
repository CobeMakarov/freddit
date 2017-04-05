from flair import flair

class moderator:

    def __init__(self, id, username, sub_id, db):
        self.id = id
        self.username = username
        self.sub_id = sub_id
        self.db = db

        self.flair = self.get_flair()

    def get_flair(self):
        self.db.get_cursor().execute("SELECT subfreddit_flairs.* FROM subfreddit_flairs "
                                     "JOIN user_flairs ON user_flairs.flair_id = subfreddit_flairs.id "
                                     "WHERE user_flairs.subfreddit_id = %s AND user_flairs.user_id = %s",
                                     (self.sub_id, self.id))

        fl = self.db.get_cursor().fetchone()

        if self.db.get_cursor().rowcount == 0:
            return None

        return flair(fl["id"], fl["text"], fl["label_type"], fl["subfreddit_id"])

    def html(self):
        return '<div style="padding-bottom: 3%">' + self.username + ' <button type="button" class="btn btn-link remove_mod" user_id="' + str(self.id) + '" id="' + str(self.sub_id) + '" style="padding: 0;">remove</button></div>'
