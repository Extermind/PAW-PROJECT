from ..database import db

class Project(db.Model):
    __tablename__ = 'Projects'
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.Integer, db.ForeignKey('Users.id'))
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    priority = db.Column(db.Integer)
    status = db.db.Column(db.db.String(255), nullable=False)
    tasks = db.relationship('Task', secondary='Projects_Tasks', back_populates="projects")

    def __init__(self, owner, title, description=None, priority=None, status=None):
        self.owner = owner
        self.title = title
        self.description = description
        self.priority = priority
        self.status = status


