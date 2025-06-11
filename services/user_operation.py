import sqlite3
from models.user import User
from const.db_connection import get_connection
 
class UserOperation:

    def add_user(name: str, age: int):
        try:
            db = get_connection()
          
            con = db['con']
            cursor = db['cursor']
            cursor.execute("INSERT INTO user (name, age) VALUES (?, ?)", (name, age))
            con.commit()
            inserted_id = cursor.lastrowid
            return {
            "user_id": inserted_id,
            "name": name,
            "age": age
            }
        except sqlite3.Error as e:
            print(f"Failed to add user: error: {e}")
            return None
        finally:
            con.close()
        

    def get_user(name: str):
        db = get_connection()
        con = db['con']
        cursor = db['cursor']
        cursor.execute("SELECT * FROM user where name = ?", (name,))
        con.commit()
        row = cursor.fetchone()
        if row:
            return dict(row)
        else:
            return None      
        con.close()  
    
    def get_all_user():
        db = get_connection()
        con = db['con']
        cursor = db['cursor']
        cursor.execute("SELECT * FROM user")
        con.commit()
        users = cursor.fetchall()
        if users:
            return [dict(row) for row in users]
        else:
            return None
        con.close()

    def validate_page_size(page_size):
        if page_size < 1:
            raise TypeError(f"page_size should be greater then 0")

    def get_users(page_number: int, page_size: int):
        try:
            UserOperation.validate_page_size(page_size)
            db = get_connection()
            con = db['con']
            cursor = db['cursor']

            offset = (page_number - 1) * page_size
            cursor.execute("SELECT * FROM user ORDER BY user_id ASC LIMIT ? OFFSET ?", (page_size, offset))
            con.commit()
            users = cursor.fetchall()
            if users:
                return [dict(row) for row in users]
            else:
                return None

        except Exception as e:
            print(f"Failed to fetch paginated users: error: {e}")
            return None

        finally:
            con.close()