from models.user import User
from models.permission import Permission
from services.user_permission import UserPermission
from services.user_operation import UserOperation
from services.permission_operation import PermissionOperation
from const.db_connection import get_connection
from const.init_db import init_db
import random
import string
from server import run_server

def main():
    init_db()
#USER OPERATIONS
    # Add User
    #adduser=UserOperation.add_user("sanil", 20)
    #print(adduser)

    # Add bulk user
    #for x in range(1, 101):
        #adduser=UserOperation.add_user(''.join(random.choices(string.ascii_letters, k=10)), random.randint(18, 60))
        #print(adduser)
    
    # Get User
    #user_in_db = UserOperation.get_user(None)
    #print(user_in_db)

    # Get all
    #all_users = UserOperation.get_all_user()
    #print(all_users)

    # Get users by pagination
    #users = UserOperation.get_users(1, 10)
    #print(users)

#PERMISSION OPERATIONS
    #Add Permission
    #addperm=PermissionOperation.add_permission("Read","Notepad n")
    #print(addperm)

    #Get Permission
    #perm_in_db = PermissionOperation.get_permission("Write")
    #print(perm_in_db)

    #Get All Permission
    #all_perm = PermissionOperation.get_all_permission()
    #print(all_perm)

#USER PERMISSIONS
    #Add Permission to User
    #add_user_perm = UserPermission.add_permission_to_user(2,3)
    #print(add_user_perm)

    #ADD bulk User Permission
    #for x in range(3,101):
        #add_user_perm = UserPermission.add_permission_to_user(x,random.randint(1, 3))
        #print(add_user_perm)

    #Get all User Permission
    #get_u_p = UserPermission.get_all_user_permission()
    #print(get_u_p)

    #get_u_p = UserPermission.get_all_user_permissions()
    #print(get_u_p)
  
    #Get User by Id
    #get_u_id = UserPermission.get_permissions_by_user(2)
    #print(get_u_id)	















    #result = UserOperation.add_user("Pratham")  
    #if "error" in result:
        #print("Something went wrong:", result["error"])
    #else:
        #print("User added:", result)


    #pagination=UserOperation.get_users_paginated(5,5)
    #print(pagination)

    #getuser=UserOperation.get("sanil")
    #print(getuser)
    #getalluser=UserOperation.getall()
    #print(getalluser)
    #getall_loop=UserOperation.getall1()
    #print(getall_loop)


if __name__ == "__main__":
    #main()
    run_server()