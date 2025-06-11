from services.user_operation import UserOperation
import json

#def handle_user_request(method, body=None):
    #if path == "/users" and method == "GET":
    #users = UserOperation.get_all_user()
    #return json.dumps(users)

def handle_user_request():
    users = UserOperation.get_all_user()
    return json.dumps(users)

def handle_user_add(body):
    data = json.loads(body)
    name = data.get("name")
    age = data.get("age")
    new_user = UserOperation.add_user(name,age)
    return json.dumps(new_user)

def handle_user_get_by_name(name):
    #name = data.get("name")
    user = UserOperation.get_user(name)
    return json.dumps(user)    

    #elif path == "/users" and method == "POST":
        #data = json.loads(body)
        #name = data.get("name")
        #age = data.get("age")
        #new_user = UserOperation.add_user(name, age)
        #return json.dumps(new_user)

    #elif path.startswith("/users/") and method == "GET":
        #user_id = int(path.split("/")[-1])
        #user = UserOperation.get_user_by_id(user_id)
        #name = data.get("name")
        #user = UserOperation.get_user(name)
        #return json.dumps(user)

    #return json.dumps({"error": "User route not found"})
