from ..database import db

class UserProject(db.Model):
    __tablename__ = 'Users_Projects'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('Projects.id'), nullable=False)

