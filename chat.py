import datetime

class chat:
    db, last_bulk_save = "", ""

    def __init__(self, database):
        self.db = database

        self.get_last_save()

    def bulk_save(self, messages):
        print("trying.. bulk save chats")

        if (datetime.datetime.now() - self.last_bulk_save).seconds >= 600 and len(messages) > 0:
            for msg in messages:
                self.db.getCursor().execute("INSERT INTO chat_messages(user_id, user_name, message_text, is_admin) VALUES (%s, %s, %s, %s)",
                                       (msg["user"]["id"], msg["user"]["name"], msg["text"], (1 if msg["user"]["is_admin"] else 0)))

            self.db.commit()
            self.update_last_save()

            print("bulk save complete")
            return True
        else:
            print("bulk save skip")
        return False

        # todo: work on cleaning up chat messages table (add permission to rem from user to table chat_messages)

    def get_latest_messages(self):
        messages = []

        self.db.getCursor().execute("SELECT * FROM chat_messages ORDER BY date_posted DESC LIMIT 20")

        rows = self.db.getCursor().fetchall()

        for row in rows:
            temp = {'text': row['message_text'],
                    'user': {
                        'id': row['user_id'],
                        'name': row['user_name'],
                        'is_admin': (int(row['is_admin']) == 1)}}

            messages.append(temp)

        return messages

    def get_last_save(self):
        self.db.getCursor().execute("SELECT last_bulk_save FROM chat_config WHERE id = 1")

        self.last_bulk_save = self.db.getCursor().fetchone()[0]

    def update_last_save(self):
        self.last_bulk_save = datetime.datetime.now()

        self.db.getCursor().execute("UPDATE chat_config SET last_bulk_save = now()::timestamp WHERE id = 1")

        print("updated last bulk_save to " + str(self.last_bulk_save))
