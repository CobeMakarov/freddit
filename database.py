import psycopg2, psycopg2.extras


class database:
    host, username, password, database = "", "", "", ""
    port = 0

    conn = ""

    cursor = ""

    def __init__(self, h, u, p, d, port):
        self.host = h;

        self.username = u;
        self.password = p;

        self.database = d;

        self.port = port;

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
