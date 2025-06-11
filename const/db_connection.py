import sqlite3



def get_connection():
   con = sqlite3.connect("user.db")
   con.row_factory = sqlite3.Row
   cursor = con.cursor()
   return {"con": con, "cursor": cursor}