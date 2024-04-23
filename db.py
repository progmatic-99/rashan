"""DB Helper code"""

import sqlite3
import threading

from typing import List, Tuple
from config import DB_PATH

BulkItemStructure = List[Tuple[str, str, int]]


class DB:
    """Wrapper for common DB actions"""

    _instance = None
    _lock = threading.Lock()

    def __init__(self, dbname="rashan.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(database=DB_PATH)

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
            raise e

        c.close()

    def add_bulk_items(self, all_items: BulkItemStructure):
        """
        Add items in bulk
        - all_items: List[Tuple[name, quantity, price]]
        """
        stmt = "INSERT INTO items (name, quantity, price) VALUES (?,?,?)"

        c = self.conn.cursor()
        try:
            c.executemany(stmt, all_items)
            self.conn.commit()
        except sqlite3.Error as e:
            raise e

        c.close()

    def delete_item(self, item_text):
        """Delete items"""
        stmt = "DELETE FROM items WHERE description = (?)"
        args = (item_text,)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def recent_items(self):
        """Get recent items"""
        stmt = "SELECT * FROM items ORDER BY created_at DESC LIMIT 5"
        c = self.conn.cursor()
        items = None
        try:
            c.execute(stmt)
            items = c.fetchall()
            c.close()
        except sqlite3.Error as e:
            raise e

        if not items:
            return "No items exists!!"

        return items

    def get_monthly_usage(self, month: str, year: str):
        """Gets monthly quantity used of all items"""
        stmt = """
        SELECT name, sum(quantity), sum(price)
        FROM items
        where strftime('%Y', created_at) = (?)
        and strftime('%m', created_at) = (?)
        GROUP BY name
        """

        c = self.conn.cursor()
        result = None
        args = (year, month)
        try:
            c.execute(stmt, args)
            result = c.fetchall()
            c.close()
        except sqlite3.Error as e:
            raise e

        if not result:
            return f"No items purchased for this {month}."

        return result
