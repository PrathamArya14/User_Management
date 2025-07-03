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

#     def update_user(user_id, name, age):
#             db = get_connection()
#             con = db['con']
#             cursor = db['cursor']
#             #conn = get_connection()
#             #cursor = conn.cursor()
#             cursor.execute(
#                 "UPDATE user SET name = ?, age = ? WHERE user_id = ?",
#                 (name, age, user_id)
#             )
#             con.commit()
#             con.close()

    def update_user(user_id, name=None, age=None):
        db = get_connection()
        con = db['con']
        cursor = db['cursor']

        fields = []
        values = []

        if name is not None:
            fields.append("name = ?")
            values.append(name)

        if age is not None:
            fields.append("age = ?")
            values.append(age)

        if not fields:
            con.close()
            return  # Nothing to update

        query = f"UPDATE user SET {', '.join(fields)} WHERE user_id = ?"
        values.append(user_id)

        cursor.execute(query, tuple(values))
        con.commit()
        con.close()

    def delete_user(user_id):
            db = get_connection()
            con = db['con']
            cursor = db['cursor']
            #conn = get_connection()
            #cursor = conn.cursor()
            cursor.execute("DELETE FROM user WHERE user_id = ?", (user_id,))
            con.commit()
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