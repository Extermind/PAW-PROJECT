from flask import jsonify, request
from . import task
from ..database import db
from ..jwt import roles_required
from ..models import Project, Task


@task.route('/project/<int:project_id>/task/add', methods=['POST'])
@roles_required('User')
def add_task(project_id):
    project = Project.query.get(project_id)
    if not project:
        return jsonify(error='Project not found'), 404

    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    priority = data.get('priority')
    assignee_id = data.get('assignee_id')

    # Validate required fields
    if not title:
        return jsonify(error='Missing required fields'), 400

    # Create a new task
    task = Task(title=title, description=description, priority=priority, assignee=assignee_id)
    project.tasks.append(task)
    db.session.commit()

    # Return the newly created task
    return jsonify(task={
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'priority': task.priority,
        'assignee_id': task.assignee
    }), 201


@task.route('/project/<int:project_id>/task/<int:task_id>', methods=['PUT'])
@roles_required('User')
def edit_task(project_id, task_id):
    project = Project.query.get(project_id)
    if not project:
        return jsonify(error='Project not found'), 404

    task = Task.query.filter(Task.id == task_id, Task.projects.contains(project)).first()
    if not task:
        return jsonify(error='Task not found'), 404

    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    priority = data.get('priority')
    assignee_id = data.get('assignee_id')

    # Update the task with new data
    task.title = title
    task.description = description
    task.priority = priority
    task.assignee = assignee_id
    db.session.commit()

    # Return the updated task
    return jsonify(task={
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'priority': task.priority,
        'assignee_id': task.assignee
    }), 200


@task.route('/project/<int:project_id>/task/<int:task_id>', methods=['DELETE'])
@roles_required('User')
def delete_task(project_id, task_id):
    project = Project.query.get(project_id)
    if not project:
        return jsonify(error='Project not found'), 404

    task = Task.query.filter(Task.id == task_id, Task.projects.contains(project)).first()
    if not task:
        return jsonify(error='Task not found'), 404

    # Remove the task from the project and delete it
    project.tasks.remove(task)
    db.session.delete(task)
    db.session.commit()

    return jsonify(message='Task deleted successfully'), 200
