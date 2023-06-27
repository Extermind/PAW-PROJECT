from ..database import db


class User(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    roles = db.relationship('Role', secondary='Users_Roles', back_populates="users")

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

