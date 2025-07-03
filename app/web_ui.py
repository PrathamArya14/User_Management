import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template, request, redirect, url_for
from services.user_operation import UserOperation
from services.permission_operation import PermissionOperation
from services.user_permission import UserPermission

app = Flask(__name__)

@app.route("/")
def index():
    return redirect("/users")

#@app.route("/users")
#def list_userss():
#    users = UserOperation.get_all_user()
#    return render_template("users.html", users=users)
#    print(users[0])

#@app.route("/permissions")
# def list_permissions():
#     permissions = PermissionOperation.get_all_permission()
#     query = request.args.get("query", "").lower()
#
#     if query:
#         permissions = [p for p in permissions if query in p["name"].lower()]
#     return render_template("permissions.html", permissions=permissions)

# @app.route("/permissions")
# def list_permissions():
#     query = request.args.get("query", "").lower()
#     page = int(request.args.get("page", 1))
#     per_page = 10  # You can increase if needed
#
#     all_permissions = PermissionOperation.get_all_permission()
#
#     # Filter by query
#     if query:
#         all_permissions = [p for p in all_permissions if query in p["name"].lower()]
#
#     total_permissions = len(all_permissions)
#     total_pages = (total_permissions + per_page - 1) // per_page
#
#     # Paginate
#     start = (page - 1) * per_page
#     end = start + per_page
#     permissions = all_permissions[start:end]
#
#     return render_template("permissions.html", permissions=permissions, page=page, total_pages=total_pages, query=query)

@app.route("/permissions")
def list_permissions():
    query = request.args.get("query", "").strip().lower()
    try:
        page = int(request.args.get("page") or 1)
    except ValueError:
        page = 1
    try:
        per_page = int(request.args.get("per_page") or 5)
    except ValueError:
        per_page = 5
    edit_id = request.args.get("edit_id")

    all_permissions = PermissionOperation.get_all_permission()
    if query:
        all_permissions = [p for p in all_permissions if query in p["name"].lower()]

    total = len(all_permissions)
    total_pages = (total + per_page - 1) // per_page
    permissions = all_permissions[(page - 1) * per_page : page * per_page]

    return render_template("permissions.html", permissions=permissions, page=page,
                           per_page=per_page, total_pages=total_pages, query=query, edit_id=edit_id)


@app.route("/user/<int:user_id>/permissions")
def view_user_permissions(user_id):
    user = UserOperation.get_user(user_id)
    all_permissions = PermissionOperation.get_all_permission()
    assigned = UserPermission.get_permissions_by_user(user_id)
    assigned_ids = [p['id'] for p in assigned]
    return render_template("assign.html", user=user, permissions=all_permissions, assigned=assigned_ids)

@app.route("/user/<int:user_id>/assign", methods=["POST"])
def assign_permission(user_id):
    selected_ids = request.form.getlist("permissions")
    selected_ids = list(map(int, selected_ids))
    UserPermission.remove_all_permissions_from_user(user_id)
    for pid in selected_ids:
        UserPermission.add_permission_to_user(user_id, pid)
    return redirect(f"/user/{user_id}/permissions")

#@app.route("/users")
#def list_users():
#    users = UserOperation.get_all_user()
#    for user in users:
#        perms = UserPermission.get_permissions_by_user(user['id'])
#        user['permissions'] = perms  # attach permissions list to user
#    return render_template("users.html", users=users)

# @app.route("/users")
# def list_users():
#     users = UserOperation.get_all_user()
#     query = request.args.get("query", "")
#     if query:
#         users = [u for u in users if query.lower() in u['name'].lower()]
#
#     #return render_template("users.html", users=users)
#     for user in users:
#         perms_data = UserPermission.get_permissions_by_user(user["user_id"])
#         if isinstance(perms_data, list) and perms_data:
#             user["permissions"] = perms_data[0].get("permissions", "")
#         else:
#             user["permissions"] = ""
#     return render_template("users.html", users=users)

# @app.route("/users")
# def list_users():
#     query = request.args.get("query", "").lower()
#     page = int(request.args.get("page", 1))  # default to page 1
#     per_page = 10  # ✅ You can change to 10, 20 etc.
#
#     all_users = UserOperation.get_all_user()
#
#     # Filter by query
#     if query:
#         all_users = [u for u in all_users if query in u["name"].lower()]
#
#     total_users = len(all_users)
#     total_pages = (total_users + per_page - 1) // per_page
#
#     # Paginate
#     start = (page - 1) * per_page
#     end = start + per_page
#     users = all_users[start:end]
#
#     # Add permissions to each user
#     for user in users:
#         perms_data = UserPermission.get_permissions_by_user(user["user_id"])
#         if perms_data:
#             user["permissions"] = perms_data[0].get("permissions", "")
#         else:
#             user["permissions"] = ""
#
#     return render_template("users.html", users=users, page=page, total_pages=total_pages, query=query)


# with pagination on page
@app.route("/users")
def list_users():
    query = request.args.get("query", "").lower()
    try:
            page = int(request.args.get("page") or 1)
    except ValueError:
            page = 1

    try:
            per_page = int(request.args.get("per_page") or 5)
    except ValueError:
            per_page = 5
#     page = int(request.args.get("page", 1))
#     per_page = int(request.args.get("per_page", 5))  # default is 5

    all_users = UserOperation.get_all_user()

    # Filter by search
    if query:
        all_users = [u for u in all_users if query in u["name"].lower()]

    total_users = len(all_users)
    total_pages = (total_users + per_page - 1) // per_page

    start = (page - 1) * per_page
    end = start + per_page
    users = all_users[start:end]

    # Get permissions
    for user in users:
        perms_data = UserPermission.get_permissions_by_user(user["user_id"])
        user["permissions"] = perms_data[0].get("permissions", "") if perms_data else ""

    return render_template("users.html", users=users, page=page, total_pages=total_pages,
                           query=query, per_page=per_page)


@app.route("/add-user", methods=["POST"])
def add_user():
    name = request.form.get("name")
    age = request.form.get("age")
    if name and age:
        UserOperation.add_user(name, int(age))
        return redirect("/users?success=1")  # ✅ add URL flag
    return redirect("/users?error=1")
    #return redirect("users")

@app.route("/add-permission", methods=["POST"])
def add_permission():
    name = request.form.get("name")
    description = request.form.get("description")

    if name:
        PermissionOperation.add_permission(name, description)
        return redirect("/permissions?success=1")
    else:
        return redirect("/permissions?error=1")


# @app.route("/edit-user/<int:user_id>", methods=["GET", "POST"])
# def edit_user(user_id):
#     user = UserOperation.get_user(user_id)
#     if request.method == "POST":
#         name = request.form.get("name")
#         age = request.form.get("age")
#         UserOperation.update_user(user_id, name, int(age))
#         return redirect("/users?success=2")
#     return render_template("edit_user.html", user=user)

# @app.route("/edit-user/<int:user_id>", methods=["GET", "POST"])
# def edit_user(user_id):
#     user = UserOperation.get_user(user_id)
#
#     if request.method == "POST":
#         name = request.form.get("name").strip()
#         age = request.form.get("age").strip()
#
#         # Convert only if age is provided and not empty
#         age_value = int(age) if age else None
#         name_value = name if name else None
#
#         UserOperation.update_user(user_id, name=name_value, age=age_value)
#         return redirect("/users?success=2")
#
#     return render_template("edit_user.html", user=user)

@app.route("/update-user/<int:user_id>", methods=["POST"])
def update_user_inline(user_id):
    name = request.form.get("name")
    age = request.form.get("age")

    name = name.strip() if name else None
    age = int(age) if age else None

    UserOperation.update_user(user_id, name=name, age=age)
    # ✅ Read page state from hidden fields
    page = request.form.get("page", 1)
    per_page = request.form.get("per_page", 5)
    query = request.form.get("query", "")

    # ✅ Redirect back to the same page without edit mode
    return redirect(f"/users?page={page}&per_page={per_page}&query={query}&success=2")
#    return redirect("/users?success=2")



@app.route("/delete-user/<int:user_id>")
def delete_user(user_id):
    UserOperation.delete_user(user_id)

    page = request.args.get("page", "1")
    per_page = request.args.get("per_page", "5")
    query = request.args.get("query", "")

    return redirect(url_for('list_users', page=page, per_page=per_page, query=query, deleted=1))
#    return redirect("/users?deleted=1")

# @app.route("/edit-permission/<int:permission_id>", methods=["GET", "POST"])
# def edit_permission(permission_id):
#     permission = PermissionOperation.get_permission(permission_id)
#
#     if request.method == "POST":
#         name = request.form.get("name").strip()
#         description = request.form.get("description").strip()
#
#         name_value = name if name else None
#         desc_value = description if description else None
#
#         PermissionOperation.update_permission(permission_id, name=name_value, description=desc_value)
#         return redirect("/permissions?success=2")
#
#     return render_template("edit_permission.html", permission=permission)

# @app.route("/update-permission/<int:permission_id>", methods=["POST"])
# def update_permission(permission_id):
#     name = request.form.get("name").strip()
#     description = request.form.get("description").strip()
#     PermissionOperation.update_permission(permission_id, name=name, description=description)
#     return redirect("/permissions?success=2")

@app.route("/update-permission/<int:permission_id>", methods=["POST"])
def update_permission(permission_id):
    name = request.form.get("name").strip()
    description = request.form.get("description").strip()
    PermissionOperation.update_permission(permission_id, name=name, description=description)

    page = request.form.get("page", "1")
    per_page = request.form.get("per_page", "5")
    query = request.form.get("query", "")
    return redirect(url_for('permissions', page=page, per_page=per_page, query=query, success=1))

@app.route("/delete-permission/<int:permission_id>")
def delete_permission(permission_id):
    PermissionOperation.delete_permission(permission_id)

    page = request.args.get("page", "1")
    per_page = request.args.get("per_page", "5")
    query = request.args.get("query", "")
    return redirect(url_for('list_permissions', page=page, per_page=per_page, query=query, deleted=1))


# @app.route("/delete-permission/<int:permission_id>")
# def delete_permission(permission_id):
#     PermissionOperation.delete_permission(permission_id)
#     return redirect("/permissions?deleted=1")

# Assign Permission to user
# @app.route("/assign-permissions/<user_name>")
# def assign_permissions(user_name):
#     user = UserOperation.get_user(user_name)
#     all_permissions = PermissionOperation.get_all_permission()
#     user_permissions = UserPermission.get_permissions_by_user(user_name)
#
#     # Page state
#     page = request.args.get("page", "1")
#     per_page = request.args.get("per_page", "5")
#     query = request.args.get("query", "")
#
#     return render_template("assign_permissions.html",
#                            user=user,
#                            all_permissions=all_permissions,
#                            user_permissions=user_permissions,
#                            page=page, per_page=per_page, query=query)
#
# @app.route("/assign-permissions/<user_name>", methods=["POST"])
# def assign_permissions_post(user_name):
#     selected_permission_ids = request.form.getlist("permissions")
#     UserPermission.assign_permissions_to_user(user_id, selected_permission_ids)
#
#     # Preserve page state
#     page = request.form.get("page", "1")
#     per_page = request.form.get("per_page", "5")
#     query = request.form.get("query", "")
#
#     return redirect(url_for("list_users", page=page, per_page=per_page, query=query, success=1))

#Assign NEw permission
@app.route("/assign-permissions/<username>")
def assign_permissions(username):
    user = UserOperation.get_user(username)
    if not user:
        return "User not found", 404

    all_permissions = PermissionOperation.get_all_permission()
    user_perm_data = UserPermission.get_permissions_by_user(user["user_id"])

    user_permissions = []
    if user_perm_data and isinstance(user_perm_data, list):
        perms = user_perm_data[0].get("permissions", "")
        user_permissions = [p.strip() for p in perms.split(",") if p.strip()]

    # Preserve page state
    page = request.args.get("page", "1")
    per_page = request.args.get("per_page", "5")
    query = request.args.get("query", "")

    return render_template("assign_permissions.html",
                           user=user,
                           all_permissions=all_permissions,
                           user_permissions=user_permissions,
                           page=page, per_page=per_page, query=query)

@app.route("/assign-permissions/<username>", methods=["POST"])
def assign_permissions_post(username):
    user = UserOperation.get_user(username)
    if not user:
        return "User not found", 404

    user_id = user["user_id"]
    selected_permission_names = request.form.getlist("permissions")

    current_data = UserPermission.get_permissions_by_user(user_id)
    current_permissions = []
    if current_data and isinstance(current_data, list):
        perms_str = current_data[0].get("permissions", "")
        current_permissions = [p.strip() for p in perms_str.split(",") if p.strip()]

    for name in selected_permission_names:
        if name not in current_permissions:
            permission = PermissionOperation.get_permission(name)
            if permission:
                UserPermission.add_permission_to_user(user_id, permission["permission_id"])

    # Preserve pagination
    page = request.form.get("page", "1")
    per_page = request.form.get("per_page", "5")
    query = request.form.get("query", "")

    return redirect(url_for("list_users", page=page, per_page=per_page, query=query, success=3))




@app.route("/manage-access", methods=["GET", "POST"])
def manage_access():
    if request.method == "POST":
        action = request.form.get("action")

        if action == "add_user":
            name = request.form.get("user_name")
            age = request.form.get("user_age")
            if name and age:
                UserOperation.add_user(name, int(age))

        elif action == "add_permission":
            name = request.form.get("perm_name")
            desc = request.form.get("perm_desc")
            if name:
                PermissionOperation.add_permission(name, desc)

        #elif action == "assign_permission":
        #    user_id = int(request.form.get("assign_user_id"))
        #    selected = request.form.getlist("assign_permissions")
        #    selected_ids = list(map(int, selected))
        #    UserPermission.remove_all_permissions_from_user(user_id)
        #    for pid in selected_ids:
        #        UserPermission.add_permission_to_user(user_id, pid)
#ok code jsdjdnad
#         elif action == "assign_permission":
#             user_id = int(request.form.get("assign_user_id"))
#             selected_ids = list(map(int, request.form.getlist("assign_permissions")))
#
#             for pid in selected_ids:
#                 UserPermission.add_permission_to_user(user_id, pid)  # ✅ no removal


        return redirect("/manage-access")

    users = UserOperation.get_all_user()
    permissions = PermissionOperation.get_all_permission()
    return render_template("manage_access.html", users=users, permissions=permissions)




if __name__ == "__main__":
    app.run(debug=True, port=5000)
