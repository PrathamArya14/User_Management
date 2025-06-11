from .db_connection import get_connection

def init_db():
    #con = sqlite3.connect(db_path)
    #cursor = con.cursor()
    db = get_connection()
    con = db['con']
    cursor = db['cursor']

    cursor.execute("PRAGMA foreign_keys = ON;")
    cursor.execute("CREATE TABLE IF NOT EXISTS user (user_id INTEGER PRIMARY KEY AUTOINCREMENT,name varchar NOT NULL,age INTEGER)")
    cursor.execute("CREATE TABLE IF NOT EXISTS permission (permission_id INTEGER PRIMARY KEY AUTOINCREMENT,name varchar NOT NULL UNIQUE,description TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS user_permissions (user_id INTEGER ,permission_id INTEGER , PRIMARY KEY (user_id , permission_id),FOREIGN KEY (user_id) REFERENCES user(user_id), FOREIGN KEY (permission_id) REFERENCES permission(permission_id))")

    con.commit()
    print('Database Initialized')