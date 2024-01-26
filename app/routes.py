from flask import request
from datetime import datetime
from app import app,db
from fake_data.tasks import tasks_list
from app.models import User,Task
from app.auth import basic_auth,token_auth


users = []

@app.route('/')
def test():
    return 'Testing to see if this works'

@app.route('/tasks')
def get_tasks():
    tasks = tasks_list
    return tasks

@app.route('/tasks/<int:task_id>')
def get_task(task_id):
    tasks = tasks_list
    for task in tasks:
        if task['id'] == task_id:
            return task
    return {'error':f'Task with the ID {task_id} does not exist'},404

# New Task



@app.route('/tasks',methods=['POST'])
def create_task():
    if not request.is_json:
        return {'error':'Your content-type must be application/json'},400
    data = request.json
    required_fields = ['title',"description"]
    missing_fields = []
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
    if missing_fields:
        return {'error': f"{', '.join(missing_fields)} must be in the request body"}, 400


    title = data.get('title')
    description = data.get("description")
    completed=data.get('completed',False)

    new_task = Task(title=title,description=description,completed=completed)
    return new_task.to_dict(),201

# Update task
@app.route("/tasks/<int:task_id>", methods= ["PUT"])
@token_auth.login_required
def edit_task(task_id):
    if not request.is_json:
        return {"error": "Your content-type is not application/json"},400
    task = db.session.get(task,task_id)
    if task is None:
        return {"error":f"task with the id of {task_id} doesnt exist"},404
    current_task = token_auth.current_task()
    if task.author is not current_task:
        return {"error":"This task cannot be edited"},403
    data = request.json
    task.update(**data)
    return task.to_dict()



#  Create Token

@app.route('/token')
@basic_auth.login_required
def get_token():
    user = basic_auth.current_user()
    token = user.get_token()
    return {"token":token,
            "tokenExpiration":user.token_expiration}




#  Create New User

@app.route('/users',methods = ['POST'])
def create_user():
    if not request.is_json:
        return {'error':'Your content-type is must be appplication/json'},400
    data = request.json
    required_fields = ['username','email','password']
    missing_fields = []
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
        if missing_fields:
            return {'error': f"{', '.join(missing_fields)} must be in the request body"}
        
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        check_users = db.session.execute(db.select(User).where((User.username==username) | (User.email==email) )).scalars().all()

        if check_users:
            return {'error': 'A user with that username and or email already exists'},400 
        
        new_user = User(username=username,email=email,password=password)
        return new_user.to_dict(),201


    new_user = {
        "id" : len(users) + 1,
        "username": username,
        "email": email,
        "password":password
    }

    users.append(new_user) 
    return new_user,201

# Update
@app.route("/users/<intuser_id>",methods=["PUT"])
@token_auth.login_required
def edit_user(user_id):
    if not request.is_json:
        return {"error":"your content type must be application/json"},400
    user = db.session.get(User,user_id)
    if user is None:
        return {"error": f"User with {user_id} does not exist"},404
    current_user = token_auth.current_user()
    if user is not current_user:
        return {"error":"You cannt change this user as you are not them"},403
    data = request.json
    user.update(**data)
    return user.to_dict()

# delete
@app.route("/users/<int:user_id>", methods = ["DELETE"])
@token_auth.login_required
def delete_user(user_id):
    user = db.session.get(User,user_id)
    current_user = token_auth.current_user()
    if user is None:
        return {"error":f"User with {user_id} not found!"},404
    if user is not current_user:
        return {"error": "You cant do that, delete yourself only"},403
    user.delete()
    return {"success":f"{user.username} has been deleted"}

@app.route("/tasks/<int:task_id>", methods = ["DELETE"])
@token_auth.login_required
def delete_task(task_id):
    task = db.session.get(Task,task_id)
    current_task = token_auth.current_task
    if task is None:
        return {"error":f"User with {task_id} not found!"},404
    if task is not current_task:
        return {"error": "You cant do that, delete yourself only"},403
    task.delete()
    return {"success":f"{task.id} has been deleted"}


# retrieve
@app.get("/users/<int:user_id>")
def get_user(user_id):
    user = db.session.get(User,user_id)
    if user:
        return user.to_dict()
    else:
        return {"error":f"user with id:{user_id} not found"},404
