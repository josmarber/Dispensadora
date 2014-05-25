__author__ = 'Chema'

import sqlite3

db = sqlite3.connect('contentDB/bebidas')

cursor = db.cursor()#repasar sql
cursor.execute('''
                   SELECT * FROM bebidas
''')
db.commit()

rows = cursor.fetchall()
for row in rows:
    print (row[2])