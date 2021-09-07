# manage.py
from flask import Flask, request, jsonify
from flask.json import JSONDecoder, JSONEncoder

app = Flask(__name__)

users = [
    {"id": 1, "name": "Robin", "password": "robin"},
    {"id": 2, "name": "Apo", "password": "apo"},
    {"id": 3, "name": "Dash", "password": "dash"},
]

def _find_next_id():
    return max(user["id"] for user in users) + 1

def _find_user_id(username):
    for one in users:
        if one['name'] == username:
            return one['id']
    return -1

def _remove_user(userid):
    for one in users:
        if one['id'] == userid:
            users.remove(one)
            return 1
    return 0

# @app.get("/login/<name>/<password>")
# def get_user(name, password):
#     for user in users:
#         if user['name'] == name and user['password'] != password:
#             return {"result": "Invalid Password"}
#         elif user['name'] == name and user['password'] == password:
#             return user
#     return {"result": "Invalid User"}

@app.get("/login")
def verify_user():
    if request.is_json:
        req = request.get_json()
        username = req['name']
        userpwd = req['password']
        for one in users:
            if one['name'] == username and one['password'] == userpwd:
                return {"result": "Login successfully!"}, 200
            elif one['name'] == username and one['password'] != userpwd:
                return {"result": "Invalid password!"}
        return {"result": "Invaild user!"}
    return {"error": "Request must be JSON"}, 415

@app.post("/signup")
def signup_newuser():
    if request.is_json:
        user = request.get_json()
        user["id"] = _find_next_id()
        users.append(user)
        return {"result": "Signup Successfully!"}, 201
    return {"error": "Request must be JSON"}, 415

@app.put("/updateuser")
def update_userinfo():
    if request.is_json:
        user = request.get_json()
        is_exist = _find_user_id(user['name'])
        if is_exist != -1:
            _remove_user(is_exist)
            user['id'] = is_exist
            users.append(user)
            return {"result": "Update successfully!"}
        return {"result": "Invalid User!"}
    return {"error": "Request must be JSON"}, 415

@app.delete("/deleteuser")
def delete_user():
    if request.is_json:
        user = request.get_json()
        is_exist = _find_user_id(user['name'])
        if is_exist != -1:
            _remove_user(is_exist)
            return {"result": "Delete successfully!"}
        return {"result": "Invalid User!"}
    return {"error": "Request must be JSON"}, 415