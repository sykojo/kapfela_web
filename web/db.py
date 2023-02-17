import os
import sqlite3
from time import sleep

class DB:
    sql_selection_table = "CREATE TABLE IF NOT EXISTS selection (id NOT NULL PRIMARY KEY, name text NOT NULL);"
    sql_selection_table_init = "INSERT OR REPLACE INTO selection VALUES (0, '');"
    sql_history_table = "CREATE TABLE IF NOT EXISTS history (name text NOT NULL PRIMARY KEY, counter integer NOT NULL);"

    sql_selection_update = "UPDATE selection SET name=? WHERE id=0;"
    sql_history_increase_replace = "INSERT OR REPLACE INTO history(name, counter) VALUES (?, COALESCE((SELECT counter+1 FROM history WHERE name=:name), 1));"

    sql_selection_select = "select * from selection;"
    sql_history_select_all = "select * from history;"
    sql_history_select = "select * from history where name=?;"

    def __init__(self):
        self.database_name = "static/db/kapfela.sqlite"

        self._create_structure()

    def _conn(self):
        try:
            conn = sqlite3.connect(self.database_name, isolation_level='Exclusive')
            c = conn.cursor()
            c.execute('PRAGMA synchronous = 0')
            c.execute('PRAGMA journal_mode = ON')
            conn.commit()

            return conn
        except sqlite3.Error as e:
            print(e)

    def _create_structure(self):
        if not os.path.exists(self.database_name):
            conn = self._conn()
            c = conn.cursor()

            # structure
            c.execute(self.sql_history_table)
            c.execute(self.sql_selection_table)
            c.execute(self.sql_selection_table_init)
            conn.commit()

    def selection(self):
        try:
            conn = self._conn()
            c = conn.cursor()

            c.execute(self.sql_selection_select)
            rows = c.fetchall()

            if len(rows) == 0:
                return ""
            else:
                return rows[0][1]

        except sqlite3.Error as e:
            print(e)
            sleep(0.005)
    def counter(self, fn):
        try:
            conn = self._conn()
            c = conn.cursor()

            c.execute(self.sql_history_select, [fn])
            rows = c.fetchall()

            if len(rows) == 0:
                return 0
            else:
                return rows[0][1]

        except sqlite3.Error as e:
            print(e)
            sleep(0.005)

    def counter_increase(self, fn):
        try:
            conn = self._conn()
            c = conn.cursor()

            # increase counter
            c.execute(self.sql_history_increase_replace, [fn, fn])
            # select song
            c.execute(self.sql_selection_update, [fn])
            conn.commit()
        except sqlite3.Error as e:
            print(e)
            sleep(0.005)