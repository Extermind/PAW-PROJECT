from datetime import datetime

from ..database import db


class Log(db.Model):
    __tablename__ = 'Logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ip_address = db.Column(db.String(255), nullable=False)
    endpoint = db.Column(db.String(255), nullable=False)
    method = db.Column(db.String(10), nullable=False)
    headers = db.Column(db.JSON, nullable=True)
    body = db.Column(db.JSON, nullable=True)
    response_status_code = db.Column(db.Integer, nullable=False)

    def __init__(self, user_id, ip_address, endpoint, method, headers, body, response_status_code):
        self.user_id = user_id
        self.ip_address = ip_address
        self.endpoint = endpoint
        self.method = method
        self.headers = headers
        self.body = body
        self.response_status_code = response_status_code

    @staticmethod
    def add_log(jwt_data, request, response):
        user_id = jwt_data.get('sub')
        ip_address = request.remote_addr
        endpoint = request.path
        method = request.method
        headers = dict(request.headers)
        body = None
        if request.is_json:
            body = request.get_json()
        response_status_code = response[1]
        login_log = Log(user_id, ip_address, endpoint, method, headers, body, response_status_code)
        db.session.add(login_log)
        db.session.commit()
