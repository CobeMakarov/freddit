class subfreddit:
    id, creator_id = 0, 0
    path, title, desc, db = "", "", "", ""

    moderators = []

    @staticmethod
    def create(path, title, creator_id, private, desc, db):
        db.getCursor().execute("INSERT INTO subfreddits (path, title, creator_id, private, description) "
                               "VALUES (%s, %s, %s, %s, %s) RETURNING id",
                               (path, title, creator_id, private, desc))

        generated = db.getCursor().fetchone()[0]

        db.commit()

        return generated

    def __init__(self, id, db, path=None, title=None, creator=None, desc=None):
        self.db = db

        self.id = id

        if path is None and title is None and creator is None and desc is None :
            self.db.getCursor().execute("SELECT * FROM subfreddits WHERE id = %s", (self.id,))

            row = self.db.getCursor().fetchone()

            self.path = row["path"]
            self.title = row["title"]
            self.desc = row["description"]

            self.creator_id = row["creator_id"]
        else:
            self.id = id
            self.path = path
            self.title = title
            self.desc = desc

            self.creator_id = creator

            self.db = db