class moderator:

    def __init__(self, id, username, sub_id, db):
        self.id = id
        self.username = username
        self.sub_id = sub_id
        self.db = db

    def html(self):
        return '<div style="padding-bottom: 3%">' + self.username + ' <button type="button" class="btn btn-link remove_mod" user_id="' + str(self.id) + '" id="' + str(self.sub_id) + '" style="padding: 0;">remove</button></div>'
