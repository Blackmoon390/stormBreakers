import pandas as pd
import sqlite3

# User credentials table
users = pd.DataFrame({
    'name': ['vishnu', 'micheal', 'madhan'],
    'email': ['vishnu@mail.com', 'michel@mail.com',"ms.madhanyt@gmail.com"],
    'phone': ['1234567890', '1234567891', '1234567892']
})




conn = sqlite3.connect("consultant.db")


users.to_sql("doctors", conn, if_exists="replace", index=False)

conn.close()
