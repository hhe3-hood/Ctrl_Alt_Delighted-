-- TimePal Database Schema (Secure & Login-Ready)
-- Author: Hannah-Grace & Team
-- Date: 2025-11-05

CREATE DATABASE IF NOT EXISTS timepal;
USE timepal;

-- 1. Users Table
CREATE TABLE Users (
    user_id CHAR(36) PRIMARY KEY,                       
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    email_verified BOOLEAN DEFAULT 0,
    failed_login_attempts INT DEFAULT 0,
    last_failed_login DATETIME DEFAULT NULL,
    last_login DATETIME DEFAULT NULL,
    password_reset_token VARCHAR(255) DEFAULT NULL,
    password_reset_expiry DATETIME DEFAULT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 2. Task_Types Table
CREATE TABLE Task_Types (
    task_type_id INT AUTO_INCREMENT PRIMARY KEY,
    type_name VARCHAR(50) NOT NULL,
    description TEXT
);

-- 3. Color_Schemes Table
CREATE TABLE Color_Schemes (
    color_scheme_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    primary_color VARCHAR(7) NOT NULL,      
    secondary_color VARCHAR(7) DEFAULT NULL
);

-- 4. Tasks Table
CREATE TABLE Tasks (
    task_id CHAR(36) PRIMARY KEY,                    
    user_id CHAR(36) NOT NULL,
    task_type_id INT,
    color_scheme_id INT,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    start_time DATETIME,
    end_time DATETIME,
    reminder_time DATETIME,
    is_completed BOOLEAN DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (task_type_id) REFERENCES Task_Types(task_type_id),
    FOREIGN KEY (color_scheme_id) REFERENCES Color_Schemes(color_scheme_id)
);

-- 5. Comments Table
CREATE TABLE Comments (
    comment_id CHAR(36) PRIMARY KEY,                  
    task_id CHAR(36) NOT NULL,
    user_id CHAR(36) NOT NULL,
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (task_id) REFERENCES Tasks(task_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);


INSERT INTO Task_Types (type_name, description)
VALUES ('Homework', 'Assignments and school work'),
       ('Meeting', 'Study sessions or meetings'),
       ('Exam', 'Test or quiz schedule'),
       ('Class', 'Lecture or course time');


INSERT INTO Color_Schemes (name, primary_color)
VALUES ('Default Blue', '#3B82F6'),
       ('Soft Pink', '#EC4899'),
       ('Mellow Yellow', '#FACC15'),
       ('Cool Green', '#22C55E');


-- Sample Users
INSERT INTO Users (user_id, username, email, password_hash, email_verified)
VALUES
('11111111-1111-1111-1111-111111111111', 'hannahgrace', 'hannah@example.com', '$2b$12$abcdefgh1234567890ABCDEFGHabcdefghijABCDEFGHIJ12', 1);

-- Sample Task Type & Color
INSERT INTO Task_Types (type_name, description)
VALUES ('Homework', 'Assignments and school work');

INSERT INTO Color_Schemes (name, primary_color)
VALUES ('Default Blue', '#3B82F6');

-- Sample Task (belongs to Hannah-Grace)
INSERT INTO Tasks (task_id, user_id, task_type_id, color_scheme_id, title, description, start_time, end_time)
VALUES
('aaaa1111-aaaa-aaaa-aaaa-aaaaaaaaaaaa', '11111111-1111-1111-1111-111111111111', 1, 1, 'Finish SQL', 'Write final DB schema', '2025-11-11 10:00:00', '2025-11-11 12:00:00');

-- Sample Comment (by Hannah-Grace on her task)
INSERT INTO Comments (comment_id, task_id, user_id, content)
VALUES
('cccc3333-cccc-cccc-cccc-cccccccccccc', 'aaaa1111-aaaa-aaaa-aaaa-aaaaaaaaaaaa', '11111111-1111-1111-1111-111111111111', 'Done! Works perfectly.');
