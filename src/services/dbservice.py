import sqlite3


class DBService:
    def __init__(self, dbName):
        self.name = dbName
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect(f"database/{self.name}")
        self.cursor = self.conn.cursor()
        print(f"connection established for {self.name}")
        return self

    def __exit__(self, exc_type, exc, tb):
        if exc_type:
            self.conn.rollback()  # roll back on error
        else:
            self.conn.commit()    # commit on success
        self.cursor.close()
        self.conn.close()
        

    def getAlltables(self):
        if self.cursor is None:
            return "Internal Error w/ DB missing cursor."
        res = self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        arr = res.fetchall()
        return arr if arr else "no tables found"

    def addTable(self, tableName, params):
        if self.cursor is None:
            return "Internal Error w/ DB missing cursor."
        # basic sanitization
        tableName = tableName.replace(" ", "_")
        safe_params = [p.replace(" ", "_") for p in params]
        
        self.cursor.execute(f"CREATE TABLE {tableName} ({', '.join(safe_params)})")