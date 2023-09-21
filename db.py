import sqlite3
from xlsxwriter.workbook import Workbook
import re
_connection = None


def ensure_connection(func):
    def inner(*args, **kwargs):
        with sqlite3.connect('anketa.db') as conn:
            res = func(*args, conn=conn, **kwargs)
        return res

    return inner


@ensure_connection
def get_connection():
    global _connection
    if _connection is None:
        _connection = sqlite3.connect('anketa.db')
    return _connection


@ensure_connection
def init_db(conn, force: bool = False):
    c = conn.cursor()

    if force:
        c.execute('DROP TABLE IF EXISTS user_messages')

    c.execute('''
            CREATE TABLE IF NOT EXISTS user_messages (
                id          INTEGER PRIMARY KEY,
                user_id     INTEGER NOT NULL,
                data        TEXT NOT NULL,
                role        TEXT NOT NULL,
                division    TEXT NOT NULL,
                manager_fio TEXT,
                client_fio  TEXT NOT NULL,
                coop        TEXT NOT NULL,
                city        TEXT NOT NULL,
                region      TEXT NOT NULL,
                phone       INTEGER NOT NULL,
                email       TEXT NOT NULL,
                post        TEXT NOT NULL,
                direction   TEXT NOT NULL,
                field       TEXT NOT NULL,
                offline     TEXT NOT NULL,
                count       INTEGER,
                interest     TEXT NOT NULL,
                com         TEXT NOT NULL,
                comment     TEXT NOT NULL
            )
        ''')

    conn.commit()


@ensure_connection
def add_message(conn, user_id: int, data):
    c = conn.cursor()

    c.execute('INSERT INTO user_messages (user_id, data, role, division, manager_fio, client_fio, coop, city, region, '
              'phone, email, post, direction, field, offline, count, interest, com, comment) VALUES (?, ?, ?, ?, ?, '
              '?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
              (user_id, data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8],
               data[9], data[10], data[11], data[12], data[13], data[14], data[15], data[16], data[17]))
    conn.commit()


def add_excel():
    workbook = Workbook('output.xlsx')
    worksheet = workbook.add_worksheet()
    conn = sqlite3.connect('anketa.db')
    c = conn.cursor()
    c.execute("select * from user_messages")
    mysel = c.execute("select * from user_messages")
    for i, row in enumerate(mysel):
        for j, value in enumerate(row):
            worksheet.write(i,j,row[j])
    workbook.close()

if __name__ == '__main__':
    # rgx_phone = re.compile(r'^(?:\+?44)?[078]\d{9,13}$')
    # rgx_phone = re.compile(r'\+\d{11}')
    # phone_list = ["0412 345 678", "+61412345678", "+61 0412-345-678", "0412345678", "89892835369", "+79892835369", "79892835369"]
    # for x in phone_list:
    print(re.findall(r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?", 'q@1r'))
    if re.findall(r'\+\d{11}', "+79892q35369"):
        print('qwe')

    # init_db()
    # add_message(user_id=123, text='kekf')
    # add_excel()

