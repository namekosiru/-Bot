import sys, os
import sqlite3
from datetime import datetime
import pandas as pd

from module import make_word_count, make_git_date
import settings

GAT = os.environ.get('ACCESS_TOKEN')
REPO_NAME = os.environ.get('REPO_NAME')
# example
FILE_NAME = os.environ.get('FILE_NAME')


user_file_dic = {'account name': FILE_NAME}

date = make_git_date(GAT, REPO_NAME)
user_name = date[0]

for user, file in user_file_dic.items():
    if user_name == user:
        count = make_word_count(file)

data = (*date, count)

dbname = 'commit.db'
conn = sqlite3.connect(dbname, isolation_level=None)
cursor = conn.cursor()

sql = """CREATE TABLE IF NOT EXISTS users(
    id integer primary key autoincrement,
    committer_name,
    committer_time,
    message,
    count
    )"""

sql_insert = """INSERT INTO users(
    committer_name,
    committer_time,
    message,
    count) VALUES (?, ?, ?, ?)"""

cursor.execute(sql)
cursor.execute(sql_insert, data)

df = pd.read_sql('SELECT * FROM users', conn)
print(df)

conn.close()
