import os

from flask import Flask


def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")

    # Config Section
    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/paw'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'PAW'
    app.config['JWT_SECRET_KEY'] = 'PAW'
    app.config['DB_SCHEMA'] = 'schema.sql'

    from app.jwt import jwt
    jwt.init_app(app)

    # Database section
    from app.database import db, load_sql_file
    db.init_app(app)
    # End Database section

    # Database migration section
    with app.app_context():
        db.create_all()  # it would create all schema with Model classes
        load_sql_file(app.config['DB_SCHEMA'])  # insert all tables if exists and add 2 roles ADMIN and USER
    # End Database migration section

    # Demo section
    if False:
        from app.demo import demo_init
        with app.app_context():
            demo_init()
    # End Demo section

    # Blueprint import section
    from app.swagger import swagger_bp
    from app.auth import auth as auth_bp
    from app.project import project as project_bp
    from app.task import task as task_bp
    from app.user import user as user_bp
    # End Blueprint import section

    # Blueprint register section
    app.register_blueprint(auth_bp, url_prefix="/")
    app.register_blueprint(project_bp, url_prefix="/")
    app.register_blueprint(task_bp, url_prefix="/")
    app.register_blueprint(user_bp, url_prefix="/")
    app.register_blueprint(swagger_bp)
    # End Blueprint register section

    return app


app = create_app()
