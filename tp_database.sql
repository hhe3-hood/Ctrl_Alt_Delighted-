-- TimePal Database Schema (SQLite-Compatible)
-- Author: Hannah-Grace & Team
-- Date: 2025-11-05

PRAGMA foreign_keys = ON;

-- 1. Users Table
CREATE TABLE IF NOT EXISTS Users (
    user_id TEXT PRIMARY KEY,                       -- UUID stored as TEXT
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    email_verified INTEGER DEFAULT 0,               -- INTEGER as boolean (0/1)
    failed_login_attempts INTEGER DEFAULT 0,
    last_failed_login DATETIME DEFAULT NULL,
    last_login DATETIME DEFAULT NULL,
    password_reset_token TEXT DEFAULT NULL,
    password_reset_expiry DATETIME DEFAULT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP    -- No auto-update, use trigger if needed
);

-- 2. Task_Types Table
CREATE TABLE IF NOT EXISTS Task_Types (
    task_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
    type_name TEXT NOT NULL,
    description TEXT
);

-- 3. Color_Schemes Table
CREATE TABLE IF NOT EXISTS Color_Schemes (
    color_scheme_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    primary_color TEXT NOT NULL,      -- e.g. #FF5733
    secondary_color TEXT DEFAULT NULL
);

-- 4. Tasks Table
CREATE TABLE IF NOT EXISTS Tasks (
    task_id TEXT PRIMARY KEY,                    -- UUID stored as TEXT
    user_id TEXT NOT NULL,
    task_type_id INTEGER,
    color_scheme_id INTEGER,
    title TEXT NOT NULL,
    description TEXT,
    start_time DATETIME,
    end_time DATETIME,
    reminder_time DATETIME,
    is_completed INTEGER DEFAULT 0,              -- INTEGER as boolean (0/1)
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,   -- No auto-update trigger by default
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (task_type_id) REFERENCES Task_Types(task_type_id),
    FOREIGN KEY (color_scheme_id) REFERENCES Color_Schemes(color_scheme_id)
);

-- 5. Comments Table
CREATE TABLE IF NOT EXISTS Comments (
    comment_id TEXT PRIMARY KEY,                  -- UUID stored as TEXT
    task_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,    -- No auto-update
    FOREIGN KEY (task_id) REFERENCES Tasks(task_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);
-- Optional: Preload default Task Types
INSERT INTO Task_Types (type_name, description)
VALUES ('Homework', 'Assignments and school work'),
       ('Meeting', 'Study sessions or meetings'),
       ('Exam', 'Test or quiz schedule'),
       ('Class', 'Lecture or course time');

-- Optional: Preload default Color Schemes
INSERT INTO Color_Schemes (name, primary_color)
VALUES ('Default Blue', '#3B82F6'),
       ('Soft Pink', '#EC4899'),
       ('Mellow Yellow', '#FACC15'),
       ('Cool Green', '#22C55E');

-- Testing Data for Default Tasks
-- -- -- Demo Data userID: c50f6a59-ac8f-49fd-a35a-29c432b5fa4d

INSERT INTO Users (user_id, username, password_hash, email_verified)
VALUES ('c50f6a59-ac8f-49fd-a35a-29c432b5fa4d', 'demo_user', 'some_hash', 1);

INSERT INTO Tasks (
    task_id, user_id, task_type_id, color_scheme_id,
    title, description, start_time, end_time,
    reminder_time, is_completed
) VALUES (
    'task-001', 'c50f6a59-ac8f-49fd-a35a-29c432b5fa4d', 1, 1,
    'Project kickoff meeting',
    'Initial meeting with team to plan December milestones.',
    '2025-12-02 09:00:00', '2025-12-02 10:00:00',
    '2025-12-02 08:45:00', 0
);

INSERT INTO Tasks (
    task_id, user_id, task_type_id, color_scheme_id,
    title, description, start_time, end_time,
    reminder_time, is_completed
) VALUES (
    'task-002', 'c50f6a59-ac8f-49fd-a35a-29c432b5fa4d', 2, 2,
    'Write sprint documentation',
    'Prepare documentation for sprint deliverables.',
    '2025-12-05 14:00:00', '2025-12-05 16:00:00',
    '2025-12-05 13:30:00', 0
);

INSERT INTO Tasks (
    task_id, user_id, task_type_id, color_scheme_id,
    title, description, start_time, end_time,
    reminder_time, is_completed
) VALUES (
    'task-003', 'c50f6a59-ac8f-49fd-a35a-29c432b5fa4d', 3, 3,
    'Code review session',
    'Review pull requests for calendar module.',
    '2025-12-08 11:00:00', '2025-12-08 12:30:00',
    '2025-12-08 10:45:00', 1
);

INSERT INTO Tasks (
    task_id, user_id, task_type_id, color_scheme_id,
    title, description, start_time, end_time,
    reminder_time, is_completed
) VALUES (
    'task-004', 'c50f6a59-ac8f-49fd-a35a-29c432b5fa4d', 1, 4,
    'Database maintenance window',
    'Run migrations and vacuum SQLite database.',
    '2025-12-12 19:00:00', '2025-12-12 21:00:00',
    '2025-12-12 18:30:00', 0
);

INSERT INTO Tasks (
    task_id, user_id, task_type_id, color_scheme_id,
    title, description, start_time, end_time,
    reminder_time, is_completed
) VALUES (
    'task-005', 'c50f6a59-ac8f-49fd-a35a-29c432b5fa4d', 4, 2,
    'Monthly planning review',
    'Review upcoming January features and task backlog.',
    '2025-12-20 15:00:00', '2025-12-20 16:30:00',
    '2025-12-20 14:30:00', 0
);

