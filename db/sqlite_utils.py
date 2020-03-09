import sqlite3

from db.models import User


def ensure_connection(func):
    def inner(*args, **kwargs):
        with sqlite3.connect('dc_users.db') as conn:
            res = func(conn=conn, *args, **kwargs)
        return res

    return inner


@ensure_connection
def init_db(conn: sqlite3.Connection, force: bool = False):
    c = conn.cursor()
    if force:
        c.execute('DROP TABLE IF EXISTS dc_users')
    c.execute('''
        CREATE TABLE IF NOT EXISTS dc_users (
            user_id    INTEGER,
            username   VARCHAR,
            first_name VARCHAR,
            last_name  VARCHAR,
            is_sudo    INTEGER,
            is_banned  INTEGER,
            warn       INTEGER
        )
    ''')
    print(dir(c))
    conn.commit()


@ensure_connection
def load_warn_ban_users(conn: sqlite3.Connection):
    c = conn.cursor()
    c.execute('SELECT * FROM dc_users WHERE is_banned = 1 OR is_warn = 1')
    res = c.fetchall()
    return res


@ensure_connection
def ban_user_db(conn: sqlite3.Connection, user: User):
    c = conn.cursor()
    user_exists = c.execute('SELECT user_id FROM dc_users WHERE user_id = ?', user.user_id)
    print(user_exists)
    # c.execute(
    #     '''INSERT INTO dc_users (
    #             user_id, username, first_name, last_name, is_sudo, is_banned, warn
    #         ) VALUES (?, ?, ?, ?, ?, ?, ?)''',
    #     (user.user_id, user.username, user.first_name, user.last_name, user.is_sudo, user.is_banned, user.warn)
    # )
    # conn.commit()


@ensure_connection
def count_sudo_users(conn: sqlite3.Connection):
    c = conn.cursor()
    c.execute('SELECT COUNT (*) FROM dc_users WHERE is_sudo = 1')
    res = c.fetchall()
    return res


@ensure_connection
def count_banned_users(conn: sqlite3.Connection):
    c = conn.cursor()
    c.execute('SELECT COUNT (*) FROM dc_users WHERE is_banned = 1')
    res = c.fetchall()
    return res


@ensure_connection
def count_warn_users(conn: sqlite3.Connection):
    c = conn.cursor()
    c.execute('SELECT COUNT (*) FROM dc_users WHERE warn > 0')
    res = c.fetchall()
    return res


@ensure_connection
def update_user(conn: sqlite3.Connection, user_id: int, field: str, value: int):
    c = conn.cursor()
    c.execute('UPDATE dc_users SET ? = ? WHERE user_id = ?', (field, value, user_id))
    res = c.fetchone()
    return res
