from ..database import db

class ProjectTask(db.Model):
    __tablename__ = 'Projects_Tasks'
    project_id = db.Column(db.Integer, db.ForeignKey('Projects.id'), primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('Tasks.id'), primary_key=True)
    # project = db.relationship(Project)
    # task = db.relationship(Task)
