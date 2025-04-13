import sqlite3

def show_users():
    conn = sqlite3.connect("consultant.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM doctors")
    users = cursor.fetchall()
    conn.close()
    return users 
 
