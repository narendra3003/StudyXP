drop database if exists study_logger;
create database study_logger;
use study_logger;

create table users (
    user_id int auto_increment primary key,
    username varchar(100) not null,
    email varchar(255) unique not null,
    password_hash varchar(255) not null,
    total_xp int default 0,
    current_streak int default 0,
    last_study_date date,
    preferred_study_time time,
    created_at timestamp default current_timestamp
) auto_increment=101;

create table subjects (
    subject_id int auto_increment primary key,
    user_id int,
    name varchar(100) not null,
    daily_goal_minutes int default 60,
    total_minutes int default 0,
    created_at timestamp default current_timestamp,
    foreign key (user_id) references users(user_id) on delete cascade
) auto_increment=101;

create table study_logs (
    log_id int auto_increment primary key,
    user_id int,
    subject_id int,
    date date not null,
    study_time int not null,
    foreign key (user_id) references users(user_id) on delete cascade,
    foreign key (subject_id) references subjects(subject_id) on delete cascade
) auto_increment=101;

create table mock_tests (
    test_id int auto_increment primary key,
    user_id int,
    subject_id int,
    date date not null,
    score int not null,
    total_marks int not null,
    time_taken int not null,
    foreign key (user_id) references users(user_id) on delete cascade,
    foreign key (subject_id) references subjects(subject_id) on delete cascade
) auto_increment=101;

create table notifications (
    notification_id int auto_increment primary key,
    user_id int,
    type enum('reminder', 'xp_message', 'recommendation'),
    message text not null,
    status enum('unread', 'read') default 'unread',
    created_at timestamp default current_timestamp,
    foreign key (user_id) references users(user_id) on delete cascade
) auto_increment=101;

create table xp_rewards (
    xp_id int auto_increment primary key,
    user_id int,
    xp_gained int not null,
    reason text not null,
    timestamp timestamp default current_timestamp,
    foreign key (user_id) references users(user_id) on delete cascade
) auto_increment=101;

delimiter //

create trigger after_study_log_insert
after insert on study_logs
for each row
begin
    update subjects 
    set total_minutes = total_minutes + new.study_time
    where subject_id = new.subject_id;

    update users 
    set last_study_date = curdate()
    where user_id = new.user_id;
end;
//

create trigger after_user_update
after update on users
for each row
begin
    if old.last_study_date = date_sub(curdate(), interval 1 day) 
       and new.last_study_date = curdate() then
        update users 
        set current_streak = current_streak + 1 
        where user_id = new.user_id;

        insert into xp_rewards (user_id, xp_gained, reason) 
        values (new.user_id, 2, 'maintained daily study streak');
    end if;
end;
//

create trigger after_subject_update
after update on subjects
for each row
begin
    if old.total_minutes < old.daily_goal_minutes 
       and new.total_minutes >= new.daily_goal_minutes then
        insert into xp_rewards (user_id, xp_gained, reason) 
        values (new.user_id, 10, 'daily study goal achieved');
    end if;
end;
//

create trigger after_xp_insert
after insert on xp_rewards
for each row
begin
    update users 
    set total_xp = total_xp + new.xp_gained 
    where user_id = new.user_id;

    insert into notifications (user_id, type, message, status) 
    values (new.user_id, 'xp_message', concat('you earned ', new.xp_gained, ' xp!'), 'unread');
end;
//

create event daily_reset
on schedule every 1 day 
starts timestamp(curdate() + interval 1 day)
do
begin
    update subjects set total_minutes = 0;

    update users 
    set current_streak = 0, total_xp = greatest(total_xp - 5, 0)
    where last_study_date < date_sub(curdate(), interval 1 day);
end;
//

create trigger after_mock_test_insert
after insert on mock_tests
for each row
begin
    insert into xp_rewards (user_id, xp_gained, reason) 
    values (new.user_id, 20, 'completed a mock test');
end;
//

delimiter ;

insert into users (username, email, password_hash, total_xp, current_streak, last_study_date, preferred_study_time) values
('sanchita warade', 'sanchi@example.com', 'hashedpassword123', 250, 5, '2025-02-25', '18:00:00'),
('sahil', 'sahil@example.com', 'securepassword456', 100, 2, '2025-02-24', '17:30:00'),
('Tanush', 'abc@example.com', 'randompass789', 300, 8, '2025-02-25', '20:00:00');

insert into subjects (user_id, name, daily_goal_minutes) values
(101, 'Chemistry', 60),
(101, 'Mathematics', 60),
(101, 'Physics', 60),
(102, 'Chemistry', 60),
(102, 'Physics', 60);

-- Insert extensive study logs for February (user_id: 101)
INSERT INTO study_logs (user_id, subject_id, date, study_time) VALUES
(101, 101, '2025-02-01', 60), (101, 102, '2025-02-01', 45),
(101, 101, '2025-02-02', 50), (101, 102, '2025-02-02', 40),
(101, 101, '2025-02-03', 70), (101, 102, '2025-02-03', 50),
(101, 101, '2025-02-04', 30), (101, 102, '2025-02-04', 60),
(101, 101, '2025-02-05', 90), (101, 102, '2025-02-05', 60),
(101, 101, '2025-02-06', 55), (101, 102, '2025-02-06', 50),
(101, 101, '2025-02-07', 65), (101, 102, '2025-02-07', 55),
(101, 101, '2025-02-08', 80), (101, 102, '2025-02-08', 40),
(101, 101, '2025-02-09', 75), (101, 102, '2025-02-09', 45),
(101, 101, '2025-02-10', 60), (101, 102, '2025-02-10', 50),
(101, 101, '2025-02-11', 90), (101, 102, '2025-02-11', 60),
(101, 101, '2025-02-12', 85), (101, 102, '2025-02-12', 50),
(101, 101, '2025-02-13', 45), (101, 102, '2025-02-13', 70),
(101, 101, '2025-02-14', 70), (101, 102, '2025-02-14', 60),
(101, 101, '2025-02-15', 65), (101, 102, '2025-02-15', 55),
(101, 101, '2025-02-16', 50), (101, 102, '2025-02-16', 45),
(101, 101, '2025-02-17', 60), (101, 102, '2025-02-17', 50),
(101, 101, '2025-02-18', 55), (101, 102, '2025-02-18', 65),
(101, 101, '2025-02-19', 80), (101, 102, '2025-02-19', 40),
(101, 101, '2025-02-20', 70), (101, 102, '2025-02-20', 50),
(101, 101, '2025-02-21', 60), (101, 102, '2025-02-21', 50),
(101, 101, '2025-02-22', 90), (101, 102, '2025-02-22', 60),
(101, 101, '2025-02-23', 85), (101, 102, '2025-02-23', 50),
(101, 101, '2025-02-24', 55), (101, 102, '2025-02-24', 70),
(101, 101, '2025-02-25', 75), (101, 102, '2025-02-25', 40),
(101, 101, '2025-02-26', 50), (101, 102, '2025-02-26', 60),
(101, 101, '2025-02-27', 60), (101, 102, '2025-02-27', 45),
(101, 101, '2025-02-28', 45), (101, 102, '2025-02-28', 40);

-- Additional small sessions in the mornings or revision times
INSERT INTO study_logs (user_id, subject_id, date, study_time) VALUES
(101, 101, '2025-02-02', 20), (101, 102, '2025-02-05', 30),
(101, 101, '2025-02-08', 15), (101, 102, '2025-02-12', 20),
(101, 101, '2025-02-16', 25), (101, 102, '2025-02-19', 30),
(101, 101, '2025-02-21', 20), (101, 102, '2025-02-24', 35),
(101, 101, '2025-02-27', 30);


-- Insert mock tests every 4-5 days
INSERT INTO mock_tests (user_id, subject_id, date, score, total_marks, time_taken) VALUES
(101, 101, '2025-02-03', 85, 100, 60),
(101, 102, '2025-02-07', 90, 100, 75),
(101, 101, '2025-02-11', 78, 100, 50),
(101, 101, '2025-02-15', 88, 100, 65),
(101, 102, '2025-02-19', 92, 100, 80),
(101, 101, '2025-02-23', 84, 100, 60),
(101, 102, '2025-02-27', 89, 100, 70);

-- Insert notifications for reminders, XP messages, and recommendations
INSERT INTO notifications (user_id, type, message, status) VALUES
(101, 'reminder', 'You haven’t logged any study today! Stay on track!', 'unread'),
(101, 'xp_message', 'You earned 10 XP for completing your study goal!', 'unread'),
(101, 'xp_message', 'You earned 20 XP for completing a mock test!', 'unread'),
(101, 'recommendation', 'Try to revise your weak topics.', 'unread'),
(101, 'reminder', 'Keep up your streak! Log your study time today.', 'unread'),
(101, 'xp_message', 'Streak bonus! You gained extra XP.', 'unread');

insert into xp_rewards (user_id, xp_gained, reason) values
(101, 10, 'daily goal met for mathematics'),
(101, 2, 'maintained daily study streak'),
(102, 20, 'completed a mock test'),
(103, 5, 'good progress in biology');
