CREATE TABLE IF NOT EXISTS Users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Users_Roles (
    user_id INT,
    role_id INT,
    PRIMARY KEY (user_id, role_id),
    FOREIGN KEY (user_id) REFERENCES Users(id),
    FOREIGN KEY (role_id) REFERENCES Roles(id)
);

CREATE TABLE IF NOT EXISTS Projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    owner INT,
    title VARCHAR(255) NOT NULL,
    description VARCHAR(255),
    priority INT,
    status VARCHAR(255) NOT NULL,
    FOREIGN KEY (owner) REFERENCES Users(id)
);

CREATE TABLE IF NOT EXISTS Tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description VARCHAR(255),
    priority INT,
    assignee INT,
    FOREIGN KEY (assignee) REFERENCES Users(id)
);

CREATE TABLE IF NOT EXISTS Projects_Tasks (
    project_id INT,
    task_id INT,
    PRIMARY KEY (project_id, task_id),
    FOREIGN KEY (project_id) REFERENCES Projects(id),
    FOREIGN KEY (task_id) REFERENCES Tasks(id)
);

INSERT INTO Roles (name) SELECT 'User' WHERE NOT EXISTS (SELECT 1 FROM Roles WHERE name = 'User') LIMIT 1;

INSERT INTO Roles (name) SELECT 'Admin' WHERE NOT EXISTS (SELECT 1 FROM Roles WHERE name = 'Admin') LIMIT 1;
