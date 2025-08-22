#!/usr/bin/env python3
from config import DATABASE_URL, DEBUG_MODE, CACHE_SIZE
import sqlite3


class DatabaseServer:
    def __init__(self):
        self.connection_pool = []
        self.cache_size = CACHE_SIZE  # This will fail if CACHE_SIZE is invalid

    def connect(self):
        try:
            conn = sqlite3.connect(DATABASE_URL)
            self.connection_pool.append(conn)
            return conn
        except Exception as e:
            print(f"Connection failed: {e}")
            return None
