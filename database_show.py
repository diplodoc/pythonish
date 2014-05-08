import sqlite3

db = sqlite3.connect('habraposts.db')
cursor = db.cursor()
cursor.execute('SELECT name, url FROM habraposts')
all_rows = cursor.fetchall()
for row in all_rows:
    print row[0], row[1]
