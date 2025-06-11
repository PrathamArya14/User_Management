import sqlite3
from models.permission import Permission
from const.db_connection import get_connection


class PermissionOperation:
    
    def add_permission(name: str, description: str):
        try:
            db = get_connection()
          
            con = db['con']
            cursor = db['cursor']
            cursor.execute("INSERT INTO permission (name, description) VALUES (?, ?)", (name, description))
            con.commit()
            inserted_id = cursor.lastrowid
            return {
            "permission_id": inserted_id,
            "name": name,
            "description": description
            }
        except sqlite3.Error as e:
            print(f"Failed to add permission: error: {e}")
            return None
        finally:
            con.close()

    def get_permission(name: str):
        db = get_connection()
        con = db['con']
        cursor = db['cursor']
        cursor.execute("SELECT * FROM permission where name = ?", (name,))
        con.commit()
        row = cursor.fetchone()
        if row:
            return dict(row)
        else:
            return None   
        con.close()     
    
    def get_all_permission():
        db = get_connection()
        con = db['con']
        cursor = db['cursor']
        cursor.execute("SELECT * FROM permission")
        con.commit()
        permissions = cursor.fetchall()
        if permissions:
            return [dict(row) for row in permissions]
        else:
            return None
        con.close()