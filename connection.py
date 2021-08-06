from typing import List
import sqlite3


class ConnectionManager:

    def __init__(self, pool):
        self.pool = pool

    def __enter__(self):
        self.obj = self.pool.acquire()
        return self.obj

    def __exit__(self, type, value, traceback):
        self.pool.release(self.obj)


class Connection:

    def __init__(self):
        self.connection = None

    def new(self, file_name=None):
        if file_name is None:
            try:
                self.connection = sqlite3.connect('file::memory:?cache=shared')
            except sqlite3.Error as e:
                print(e)
        else:
            try:
                self.connection = sqlite3.connect('file_name')
            except sqlite3.Error as e:
                print(e)
        print(f"Using object {id(self)}")
        return self.connection


class ConnectionPool:

    def __init__(self, size: int = 1):
        self.size = size
        self.free: List[Connection] = []
        self.in_use: List[Connection] = []
        for _ in range(0, size):
            self.free.append(Connection())

    def open(self):
        pass

    def close(self):
        pass

    def acquire(self) -> Connection:
        assert len(self.free) > 0
        r = self.free[0]
        self.free.remove(r)
        self.in_use.append(r)
        return r

    def release(self, r: Connection):
        self.in_use.remove(r)
        self.free.append(r)


# Create Connection pool
pool = ConnectionPool(2)

with ConnectionManager(pool) as r:
    r.test()

with ConnectionManager(pool) as r2:
    r2.test()
