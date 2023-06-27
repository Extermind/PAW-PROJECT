from ..database import db

class Task(db.Model):
    __tablename__ = 'Tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    priority = db.Column(db.Integer)
    assignee = db.Column(db.Integer, db.ForeignKey('Users.id'))
    projects = db.relationship('Project', secondary='Projects_Tasks', back_populates="tasks")