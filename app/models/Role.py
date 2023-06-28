from ..database import db


class Role(db.Model):
    __tablename__ = 'Roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    users = db.relationship('User', secondary='Users_Roles', back_populates="roles")


    @staticmethod
    def get_user_role():
        return Role.query.filter_by(name='User').first()