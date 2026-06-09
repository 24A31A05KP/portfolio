CREATE DATABASE IF NOT EXISTS bharat_portfolio;

USE bharat_portfolio;

CREATE TABLE admin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100),
    password VARCHAR(255)
);

INSERT INTO admin(username, password)
VALUES ('admin', 'admin123');

CREATE TABLE projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    description TEXT,
    tech_stack VARCHAR(255),
    github_link TEXT,
    live_link TEXT
);

INSERT INTO projects
(title, description, tech_stack, github_link, live_link)
VALUES
(
'CitizenShield',
'Women safety platform with SOS alerts and emergency tracking',
'Flask, PostgreSQL, JavaScript',
'https://github.com/24A31A05KP/CitizenSheild',
'https://24a31a05kp.github.io/CitizenSheild/'
),
(
'Faculty Portal Dashboard',
'Faculty management system with authentication',
'Flask, MySQL, HTML, CSS',
'#',
'#'
),
(
'Internship Management Portal',
'Internship tracking system',
'Flask, MySQL, JavaScript',
'#',
'#'
);

CREATE TABLE contacts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);