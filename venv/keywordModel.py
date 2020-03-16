# keyword_sqlite_model.py

import sqlite3
import keyword


def with_cursor(original_func):
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('keyword.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        rv = original_func(c, *args, **kwargs)
        conn.commit()
        conn.close()
        return rv
    return wrapper

##삭제 예정
@with_cursor
def create_keyword_table(c):
    try:
        c.execute("SELECT * FROM keyword")
    except:
        c.execute("CREATE TABLE keyword (id integer PRIMARY KEY AUTOINCREMENT, keyword text)")

@with_cursor
def drop_keyword_table(c):
    c.execute("DROP TABLE keyword")
###

@with_cursor
def get_keyword_list(c):
    c.execute("SELECT * FROM keyword")
    return c.fetchall()


@with_cursor
def add_keyword(c, keyword):
    print(keyword)
    c.execute("INSERT INTO keyword (keyword) VALUES ('"+keyword+"')")


@with_cursor
def read_keyword(c, _id):
    c.execute("SELECT * FROM keyword WHERE id=?", (_id,))
    return c.fetchone()

@with_cursor
def remove_keyword(c, _id):
    c.execute("DELETE FROM keyword WHERE id=?", (_id,))