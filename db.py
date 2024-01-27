"""DB Helper code"""
import sqlite3


class DB:
    """Database class"""

    def __init__(self, dbname="rashan.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def setup(self):
        """Create tables"""
        stmt = "CREATE TABLE IF NOT EXISTS items (name, price)"
        self.conn.execute(stmt)
        self.conn.commit()
