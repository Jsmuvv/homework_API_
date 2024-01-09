from . import app
from fake_data.tasks import tasks_list


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