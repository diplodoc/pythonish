import sqlite3

db = sqlite3.connect('habraposts.db')
cursor = db.cursor()
cursor.execute('CREATE TABLE habraposts(id INTEGER PRIMARY KEY, name TEXT, url TEXT)')
db.commit()

