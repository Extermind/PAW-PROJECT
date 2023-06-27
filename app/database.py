from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()

def load_sql_file(file_path):
    with open(file_path, 'r') as sql_file:
        statements = sql_file.read()
        db.session.execute(text(statements))
        db.session.commit()