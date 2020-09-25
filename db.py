import sqlite3

db = sqlite3.connect("bot.db", check_same_thread=False)
cursor = db.cursor()
cursor.execute("SELECT url FROM urlData WHERE key = ?", ('ojWw',))
data = cursor.fetchone()
print(data[0])
cursor.close()
db.close()