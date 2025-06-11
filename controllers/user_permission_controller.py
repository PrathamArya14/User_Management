import json
from services.user_permission import UserPermission

def handle_user_permission_get_all():
    result = UserPermission.get_all_user_permissions()
    return json.dumps(result)

def handle_user_permission_get_by_user(user_id):
    result = UserPermission.get_permissions_by_user(user_id)
    return json.dumps(result)

def handle_user_permission_add(body):
    data = json.loads(body)
    user_id = data.get("user_id")
    permission_ids = data.get("permission_ids")
    result = UserPermission.add_permission_to_user(user_id, permission_ids)
    return json.dumps(result)

