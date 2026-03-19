import sqlite3
import os


class DBService:
    def __init__(self, dbName: str):
        base_name = dbName.replace(".sqlite3", "")
        self.name = base_name + ".sqlite3"
        self.conn: sqlite3.Connection | None = None
        self.cursor: sqlite3.Cursor | None = None

    def __enter__(self):
        db_path = f"database/{self.name}"
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"Database '{self.name}' does not exist.")
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc, tb):
        if self.conn:
            if exc_type:
                self.conn.rollback()
            else:
                self.conn.commit()
            self.conn.close()
    
    @staticmethod
    def create(dbName: str) -> None:
        os.makedirs("database", exist_ok=True)
        base_name = dbName.replace(".sqlite3", "")
        db_path = f"database/{base_name}.sqlite3"
        if not os.path.exists(db_path):
            open(db_path, "a").close()

    def getAlltables(self):
        if self.cursor is None:
            return "Internal Error w/ DB missing cursor."
        res = self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        arr = res.fetchall()
        return arr if arr else ["No tables found."]

    def addTable(self, tableName, params):
        if self.cursor is None:
            return "Internal Error w/ DB missing cursor."
        # basic sanitization
        tableName = tableName.replace(" ", "_")
        safe_params = [p.replace(" ", "_") for p in params]
        self.cursor.execute(f"CREATE TABLE {tableName} ({', '.join(safe_params)})")

    def executeSQL(self, query):
        if self.cursor is None:
            return "Internal Error w/ DB missing cursor."
        print(query)
        res = self.cursor.execute(query)
        arr = res.fetchall()
        print(arr)
        return arr if arr else ["No data to be returned"]
