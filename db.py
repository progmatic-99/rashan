"""DB Helper code"""
import sqlite3
import threading


class DB:
    """Wrapper for common DB actions"""

    _instance = None
    _lock = threading.Lock()

    def __init__(self, dbname="rashan.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(database=dbname)

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if not cls._instance:
                cls._instance = super().__new__(cls, *args, **kwargs)

        return cls._instance

    def setup(self):
        """DB setup"""
        stmt = """
            CREATE TABLE IF NOT EXISTS items (
                name text NOT NULL,
                quantity text NOT NULL,
                price integer NOT NULL,
                created_at datetime DEFAULT CURRENT_TIMESTAMP
            )
        """
        self.conn.execute(stmt)
        self.conn.commit()

    def add_item(self, item_data):
        """Add items"""
        stmt = "INSERT INTO items (name, quantity, price) VALUES (?,?,?)"
        name = item_data["item"]
        quantity = item_data["quantity"]
        price = item_data["price"]

        args = (name, quantity, price)
        c = self.conn.cursor()
        try:
            c.execute(stmt, args)
            self.conn.commit()
        except sqlite3.Error as e:
            print(e)

    def delete_item(self, item_text):
        """Delete items"""
        stmt = "DELETE FROM items WHERE description = (?)"
        args = (item_text,)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_items(self):
        """Get items"""
        stmt = "SELECT description FROM items"
        return [x[0] for x in self.conn.execute(stmt)]
