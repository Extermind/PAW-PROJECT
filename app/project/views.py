from flask_jwt_extended import get_jwt
from . import project
from flask import jsonify, request
from ..database import db
from ..jwt import roles_required
from ..models import Project


@project.route('/projects', methods=['GET'])
@roles_required('User')
def get_projects():
    projects = Project.query.all()
    project_list = []
    for project in projects:
        project_list.append({
            'id': project.id,
            'title': project.title,
            'description': project.description,
            'status': project.status,
            'priority': project.priority,
            'owner_id': project.owner
        })

    return jsonify(projects=project_list), 200


@project.route('/project/add', methods=['POST'])
@roles_required('User')
def add_project():
    data = request.get_json()
    owner_id = get_jwt()['sub']
    title = data.get('title')
    description = data.get('description')
    priority = data.get('priority')
    status = "TO DO"

    # Validate required fields
    if not title or not description:
        return jsonify(error='Missing required fields'), 400

    # Create a new project
    project = Project(owner_id, title, description, priority, status)

    # Add the project to the database
    db.session.add(project)
    db.session.commit()

    # Return the newly created project
    return jsonify(project={
        'id': project.id,
        'owner': project.owner,
        'title': project.title,
        'description': project.description,
        'priority': project.priority,
        'status': project.status
    }), 201

@project.route('/project/<int:id>', methods=['GET'])
@roles_required('User')
def get_project(id):
    project = Project.query.get(id)
    if not project:
        return jsonify(message='Project not found'), 404

    tasks = project.tasks  # Get the tasks associated with the project

    project_data = {
        'id': project.id,
        'owner': project.owner,
        'title': project.title,
        'description': project.description,
        'priority': project.priority,
        'status': project.status,
        'tasks': []
    }

    for task in tasks:
        task_data = {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'priority': task.priority,
            'assignee': task.assignee
        }
        project_data['tasks'].append(task_data)

    return jsonify(project=project_data), 200



@project.route('/project/delete/<int:id>', methods=['DELETE'])
@roles_required('User')
def delete_project(id):
    project = Project.query.get(id)

    if project:
        jwt_data = get_jwt()
        if jwt_data['sub'] != project.owner:
            return jsonify(message='You do not own this project'), 403
        # Delete the project from the database
        db.session.delete(project)
        db.session.commit()
        return jsonify(message='Project deleted successfully'), 200
    else:
        return jsonify(error='Project not found'), 404
