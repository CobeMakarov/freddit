import psycopg2, psycopg2.extras
from lib.config import config

class database:
    host, username, password, database = "", "", "", ""
    port = 0

    conn = ""

    cursor = ""

    def __init__(self):
        self.host = config.database["host"]

        self.username = config.database["username"]
        self.password = config.database["password"]

        self.database = config.database["database"]

        self.port = config.database["port"]

        self.connect()

    def connect(self):
        try:
            self.conn = psycopg2.connect(host=self.host, port=self.port,
                                         user=self.username, password=self.password,
                                         database=self.database)

            self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        except:
            print("[DATABASE] Can't Connect!")

    def getCursor(self):
        return self.cursor

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()
