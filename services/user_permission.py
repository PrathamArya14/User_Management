import sqlite3
from models.permission import Permission
from models.user import User
from const.db_connection import get_connection


from const.db_connection import get_connection
import sqlite3

class UserPermission:

    def add_permission_to_user(user_id: int, permission_ids):
        db = get_connection()
        con = db['con']
        cursor = db['cursor']
        try:

            if isinstance(permission_ids, int):
                permission_ids = [permission_ids]

            for pid in permission_ids:
                cursor.execute("INSERT OR IGNORE INTO user_permissions (user_id, permission_id) VALUES (?, ?)", (user_id, pid))

            con.commit()
            return {
                "user_id": user_id,
                "permission_ids": permission_ids
            }

        except Exception as e:
            con.rollback()
            return {"error": f"Failed to assign permissions: {e}"}
    
        finally:
            con.close()


    def get_permissions_by_user(user_id: int):
        try:
            db = get_connection()
            con = db['con']
            cursor = db['cursor']
            cursor.execute("""
                SELECT u.user_id,u.name AS user_name,
                GROUP_CONCAT(p.name, ', ') AS permissions
                FROM user u
                JOIN user_permissions up ON u.user_id = up.user_id
                JOIN permission p ON up.permission_id = p.permission_id
                WHERE u.user_id = ?
                GROUP BY u.user_id, u.name
                """, (user_id,))
            rows = cursor.fetchall()
            permissions = [dict(row) for row in rows]
            return permissions

        except Exception as e:
            return {"error": f"Failed to fetch permissions for user {user_id}: {e}"}

        finally:
            con.close()

    def get_all_user_permissions():
        try:
            db = get_connection()
            con = db['con']
            cursor = db['cursor']
            cursor.execute("""
                SELECT u.user_id, u.name AS user_name, 
                GROUP_CONCAT(p.name) AS permissions
                FROM user u
                JOIN user_permissions up ON u.user_id = up.user_id
                JOIN permission p ON up.permission_id = p.permission_id
                GROUP BY u.user_id, u.name
               ORDER BY u.user_id;
            """)
            rows = cursor.fetchall()
            user_permissions = [dict(row) for row in rows]
            return user_permissions

        except Exception as e:
            return {"error": f"Failed to fetch all user permissions: {e}"}

        finally:
            con.close()







