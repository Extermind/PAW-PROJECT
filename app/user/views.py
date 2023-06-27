from flask import jsonify, request
from . import user
from ..database import db
from ..jwt import roles_required
from ..models import Project, Task, Log
from flask_jwt_extended import get_jwt


@user.route('/stats', methods=['GET'])
@roles_required('User')
def get_user_stats():
    user_id = get_jwt()['sub']
    methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS', 'CONNECT']
    stats = (
        db.session.query(Log.method, db.func.count())
        .filter(Log.user_id == user_id)
        .group_by(Log.method)
        .all()
    )
    stats_dict = {stat[0]: stat[1] for stat in stats}
    method_stats = {method: stats_dict.get(method, 0) for method in methods}

    return jsonify(methods=method_stats), 200