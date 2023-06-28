import bcrypt

from .models import User, Project, Task
from .database import db

def demo_init():
    user1 = User.query.filter_by(username='user1').first()

    if user1 is None:
        # Dodaj 3 użytkowników
        user1 = User(username='user1', email='user1@example.com', password=bcrypt.hashpw('password1'.encode("UTF-8"), bcrypt.gensalt()))
        user2 = User(username='user2', email='user2@example.com', password=bcrypt.hashpw('password2'.encode("UTF-8"), bcrypt.gensalt()))
        user3 = User(username='user3', email='user3@example.com', password=bcrypt.hashpw('password3'.encode("UTF-8"), bcrypt.gensalt()))

        db.session.add_all([user1, user2, user3])
        db.session.commit()

        # Dodaj projekty z zadaniami
        project1 = Project(owner=user1.id, title='Project 1', description='Description of Project 1',
                           priority=1, status='In Progress')
        project2 = Project(owner=user2.id, title='Project 2', description='Description of Project 2',
                           priority=2, status='Not Started')
        project3 = Project(owner=user3.id, title='Project 3', description='Description of Project 3',
                           priority=3, status='Completed')

        task1 = Task(title='Task 1', description='Description of Task 1', priority=1, assignee=user2.id)
        task2 = Task(title='Task 2', description='Description of Task 2', priority=2, assignee=user3.id)
        task3 = Task(title='Task 3', description='Description of Task 3', priority=1, assignee=user1.id)
        task4 = Task(title='Task 4', description='Description of Task 4', priority=3, assignee=user2.id)
        task5 = Task(title='Task 5', description='Description of Task 5', priority=2, assignee=user3.id)
        task6 = Task(title='Task 6', description='Description of Task 6', priority=1, assignee=user1.id)

        project1.tasks.extend([task1, task2])
        project2.tasks.extend([task3, task4])
        project3.tasks.extend([task5, task6])

        db.session.add_all([project1, project2, project3])
        db.session.commit()