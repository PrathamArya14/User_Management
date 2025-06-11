from services.permission_operation import PermissionOperation
import json

def handle_permission_request():
    permissions = PermissionOperation.get_all_permission()
    return json.dumps(permissions)

def handle_permission_add(body):
    data   = json.loads(body)
    name = data.get("name")
    desc = data.get("description")
    new_permission = PermissionOperation.add_permission(name,desc)
    return json.dumps(new_permission)

def handle_permission_get_by_name(name):
    #name = json.loads("name")
    permission = PermissionOperation.get_permission(name)
    return json.dumps(permission)




#def handle_permission_request(path, method, body=None):
    #if path == "/permissions" and method == "POST":
        #data = json.loads(body)
        #name = data.get("name")
        #desc = data.get("description")
        #new_permission = PermissionOperation.add_permission(name, desc)
        #return json.dumps(new_permission)

    #elif path == "/permissions" and method == "GET":
        #permissions = PermissionOperation.get_all_permission()
        #return json.dumps(permissions)

    #return json.dumps({"error": "Permission route not found"})
