from ..database import db


class UserRole(db.Model):
    __tablename__ = 'Users_Roles'
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('Roles.id'), primary_key=True)
    # user = db.relationship(User)
    # role = db.relationship(Role)