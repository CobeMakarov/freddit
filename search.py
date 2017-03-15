from user import user

class search:

    @staticmethod
    def subfreddits(term, db):
        results = []

        db.getCursor().execute("SELECT * FROM subfreddits WHERE path LIKE %s OR title LIKE %s OR description LIKE %s",
                               ('%' + str(term) + '%', '%' + str(term) + '%', '%' + str(term) + '%'))

        rows = db.getCursor().fetchall()

        for row in rows:
            temp = {'link': '/fr/' + row["path"],
                    'name': row["title"],
                    'extra': '/fr/' + row["path"],
                    'desc': row["description"]}

            results.append(temp)

        return results

    @staticmethod
    def users(term, db):
        results = []

        db.getCursor().execute("SELECT * FROM users WHERE username LIKE %s", ('%' + str(term) + '%', ))

        rows = db.getCursor().fetchall()

        for row in rows:
            karma = user.get_karma_by_id(db, int(row["id"]))

            temp = {'link': '/u/' + str(row["username"]),
                    'name': row["username"],
                    'extra': str(karma),
                    'desc': ""}

            results.append(temp)

        return results

    @staticmethod
    def posts(term, db):
        results = []

        db.getCursor().execute("SELECT * FROM posts WHERE soft_deleted = 0 AND title LIKE %s OR post_text LIKE %s",
                               ('%' + str(term) + '%', '%' + str(term) + '%'))

        rows = db.getCursor().fetchall()

        for row in rows:
            temp = {'link': '/p/' + str(row["id"]),
                    'name': row["title"],
                    'extra': str(row["vote_count"]),
                    'desc': row["post_text"]}

            results.append(temp)

        return results

    @staticmethod
    def posts_in_sub(term, sub, db):
        results = []

        db.getCursor().execute("SELECT * FROM posts WHERE soft_deleted = 0 AND title LIKE %s OR post_text LIKE %s AND subfreddit = %s",
                               ('%' + str(term) + '%', '%' + str(term) + '%', sub))

        rows = db.getCursor().fetchall()

        for row in rows:
            temp = {'link': '/p/' + str(row["id"]),
                    'name': row["title"],
                    'extra': str(row["vote_count"]),
                    'desc': row["post_text"]}

            results.append(temp)

        return results
