import pymysql as p
import datetime as dt
from pymysql.cursors import DictCursor

def connect():
    return p.connect(
        host="localhost",
        user="root",
        password="oracle",
        database="study_logger"
    )

def connect2():
    return p.connect(
        host="localhost",
        user="root",
        password="oracle",
        database="study_logger",
        cursorclass=DictCursor
    )


def insert_user(user_data):
    con = connect()
    cur = con.cursor()
    sql = "INSERT INTO users (username, email, password_hash, total_xp, current_streak, last_study_date, preferred_study_time) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cur.execute(sql, user_data)
    con.commit()
    con.close()

def get_all_users():
    con = connect()
    cur = con.cursor()
    sql = "SELECT * FROM users"
    cur.execute(sql)
    data = cur.fetchall()
    con.close()
    return data

def get_user_by_id(email):
    con = connect()
    cur = con.cursor()
    sql = "SELECT * FROM users WHERE user_id=%s"
    cur.execute(sql, (email,))
    data = cur.fetchone()
    con.close()
    return data

def update_user(user_id, user_data):
    con = connect()
    cur = con.cursor()
    sql = "UPDATE users SET username=%s, email=%s, password_hash=%s, total_xp=%s, current_streak=%s, last_study_date=%s, preferred_study_time=%s WHERE user_id=%s"
    cur.execute(sql, (*user_data, user_id))
    con.commit()
    con.close()

def delete_user(user_id):
    con = connect()
    cur = con.cursor()
    sql = "DELETE FROM users WHERE user_id=%s"
    cur.execute(sql, (user_id,))
    con.commit()
    con.close()


def insert_subject(subject_data):
    con = connect()
    cur = con.cursor()
    sql = "INSERT INTO subjects (user_id, name, daily_goal_minutes, total_minutes) VALUES (%s, %s, %s, %s)"
    cur.execute(sql, subject_data)
    con.commit()
    con.close()

def get_all_subjects():
    con = connect()
    cur = con.cursor()
    sql = "SELECT * FROM subjects"
    cur.execute(sql)
    data = cur.fetchall()
    con.close()
    return data

def get_subject_by_id(subject_id):
    con = connect()
    cur = con.cursor()
    sql = "SELECT * FROM subjects WHERE subject_id=%s"
    cur.execute(sql, (subject_id,))
    data = cur.fetchone()
    con.close()
    return data

def update_subject(subject_id, subject_data):
    con = connect()
    cur = con.cursor()
    sql = "UPDATE subjects SET name=%s, daily_goal_minutes=%s, total_minutes=%s WHERE subject_id=%s"
    cur.execute(sql, (*subject_data, subject_id))
    con.commit()
    con.close()

def delete_subject(subject_id):
    con = connect()
    cur = con.cursor()
    sql = "DELETE FROM subjects WHERE subject_id=%s"
    cur.execute(sql, (subject_id,))
    con.commit()
    con.close()


def insert_study_log(log_data):
    con = connect()
    cur = con.cursor()
    sql = "INSERT INTO study_logs (user_id, subject_id, date, study_time) VALUES (%s, %s, %s, %s)"
    cur.execute(sql, log_data)
    con.commit()
    con.close()

def get_all_study_logs():
    con = connect()
    cur = con.cursor()
    sql = "SELECT * FROM study_logs"
    cur.execute(sql)
    data = cur.fetchall()
    con.close()
    return data

def get_study_logs_by_user(user_id):
    con = connect()
    cur = con.cursor()
    sql = "SELECT * FROM study_logs WHERE user_id=%s"
    cur.execute(sql, (user_id,))
    data = cur.fetchall()
    con.close()
    return data

def delete_study_log(log_id):
    con = connect()
    cur = con.cursor()
    sql = "DELETE FROM study_logs WHERE log_id=%s"
    cur.execute(sql, (log_id,))
    con.commit()
    con.close()




def insert_mock_test(test_data):
    con = connect()
    cur = con.cursor()
    sql = "INSERT INTO mock_tests (user_id, subject_id, date, score, total_marks, time_taken) VALUES (%s, %s, %s, %s, %s, %s)"
    cur.execute(sql, test_data)
    con.commit()
    con.close()

def get_all_mock_tests():
    con = connect()
    cur = con.cursor()
    sql = "SELECT * FROM mock_tests"
    cur.execute(sql)
    data = cur.fetchall()
    con.close()
    return data

def get_mock_tests_by_user(user_id):
    con = connect()
    cur = con.cursor()
    sql = "SELECT * FROM mock_tests WHERE user_id=%s"
    cur.execute(sql, (user_id,))
    data = cur.fetchall()
    con.close()
    return data

def delete_mock_test(test_id):
    con = connect()
    cur = con.cursor()
    sql = "DELETE FROM mock_tests WHERE test_id=%s"
    cur.execute(sql, (test_id,))
    con.commit()
    con.close()
def insert_notification(notification_data):
    con = connect()
    cur = con.cursor()
    sql = "INSERT INTO notifications (user_id, type, message, status) VALUES (%s, %s, %s, %s)"
    cur.execute(sql, notification_data)
    con.commit()
    con.close()

def get_all_notifications():
    con = connect()
    cur = con.cursor()
    sql = "SELECT * FROM notifications"
    cur.execute(sql)
    data = cur.fetchall()
    con.close()
    return data

def get_notifications_by_user(user_id):
    con = connect()
    cur = con.cursor()
    sql = "SELECT * FROM notifications WHERE user_id=%s"
    cur.execute(sql, (user_id,))
    data = cur.fetchall()
    con.close()
    return data

def mark_notification_as_read(notification_id):
    con = connect()
    cur = con.cursor()
    sql = "UPDATE notifications SET status='read' WHERE notification_id=%s"
    cur.execute(sql, (notification_id,))
    con.commit()
    con.close()

def delete_notification(notification_id):
    con = connect()
    cur = con.cursor()
    sql = "DELETE FROM notifications WHERE notification_id=%s"
    cur.execute(sql, (notification_id,))
    con.commit()
    con.close()



def insert_xp_reward(xp_data):
    con = connect()
    cur = con.cursor()
    sql = "INSERT INTO xp_rewards (user_id, xp_gained, reason) VALUES (%s, %s, %s)"
    cur.execute(sql, xp_data)
    con.commit()
    con.close()

def get_all_xp_rewards():
    con = connect()
    cur = con.cursor()
    sql = "SELECT * FROM xp_rewards"
    cur.execute(sql)
    data = cur.fetchall()
    con.close()
    return data

def get_xp_rewards_by_user(user_id):
    con = connect()
    cur = con.cursor()
    sql = "SELECT * FROM xp_rewards WHERE user_id=%s"
    cur.execute(sql, (user_id,))
    data = cur.fetchall()
    con.close()
    return data

def delete_xp_reward(xp_id):
    con = connect()
    cur = con.cursor()
    sql = "DELETE FROM xp_rewards WHERE xp_id=%s"
    cur.execute(sql, (xp_id,))
    con.commit()
    con.close()


def get_subject_id(user_id, subject_name):
    try:
        db = connect()
        cursor = db.cursor()

        cursor.execute("SELECT subject_id FROM subjects WHERE name = %s AND user_id = %s", (subject_name, user_id))
        result = cursor.fetchone()

        cursor.close()
        db.close()

        if result:
            return result[0]  
        else:
            return None  
    except Exception as e:
        print("Error fetching subject ID:", str(e))
        return None

def insert_study_log(user_id, subject_id, duration):
    try:
        db = connect()
        cursor = db.cursor()

        cursor.execute(
            "INSERT INTO study_logs (user_id, subject_id, date, study_time) VALUES (%s, %s, %s, %s)",
            (user_id, subject_id, dt.date.today(), duration)
        )
        db.commit()

        cursor.close()
        db.close()
        return True, "Study session logged successfully!"
    except Exception as e:
        print("Database Error:", str(e))
        return False, "Database error"
    


def get_today_progress(user_id):
    db = connect()
    cursor = db.cursor()

    cursor.execute("""
        SELECT IFNULL(SUM(study_time), 0) FROM study_logs 
        WHERE user_id = %s AND date = %s
    """, (user_id, dt.date.today()))
    total_minutes = cursor.fetchone()[0]

    
    cursor.execute("""
        SELECT IFNULL(SUM(daily_goal_minutes), 60) FROM subjects 
        WHERE user_id = %s
    """, (user_id,))
    daily_goal = cursor.fetchone()[0]

    db.close()

    
    total_hours = round(total_minutes / 60, 1)
    goal_percentage = min(int((total_minutes / daily_goal) * 100), 100)

    return total_hours, goal_percentage



def get_current_streak(user_id):
    db = connect()
    cursor = db.cursor()

    # Fetch study dates in descending order
    cursor.execute("""
        SELECT date FROM study_logs 
        WHERE user_id = %s 
        ORDER BY date DESC
    """, (user_id,))
    
    study_dates = [row[0] for row in cursor.fetchall()]
    db.close()

    if not study_dates:
        return 0, 15  # No streak, 15 days to milestone

    # Calculate streak
    streak = 0
    today = dt.date.today()

    for date in study_dates:
        if date == today:
            streak += 1
            today -= dt.timedelta(days=1)
        else:
            break  # Break on first non-consecutive date

    # Determine next milestone
    next_milestone = (streak // 15 + 1) * 15  # Dynamic milestone increments
    days_to_milestone = max(0, next_milestone - streak)

    return streak, days_to_milestone

def get_xp_progress(user_id):
    db = connect()
    cursor = db.cursor()

    # Fetch total XP
    cursor.execute("SELECT SUM(xp_gained) FROM xp_rewards WHERE user_id = %s", (user_id,))
    total_xp = cursor.fetchone()[0] or 0
    db.close()


    return total_xp

def get_study_time_distribution(user_id, period="month"):
    db = connect()
    cursor = db.cursor(cursor=p.cursors.DictCursor)

    
    if period == "week":
        cursor.execute("""
            SELECT DATE(date) AS study_date, SUM(study_time) AS total_time 
            FROM study_logs 
            WHERE user_id = %s AND date >= NOW() - INTERVAL 7 DAY 
            GROUP BY study_date ORDER BY study_date
        """, (user_id,))
    else:  
        cursor.execute("""
            SELECT DATE(date) AS study_date, SUM(study_time) AS total_time 
            FROM study_logs 
            WHERE user_id = %s AND date >= NOW() - INTERVAL 30 DAY 
            GROUP BY study_date ORDER BY study_date
        """, (user_id,))

    data = cursor.fetchall()
    db.close()
    return data

def get_subject_distribution(user_id):
    db = connect()
    cursor = db.cursor(cursor=p.cursors.DictCursor)

    cursor.execute("""
        SELECT s.name AS subject, SUM(sl.study_time) AS total_time 
        FROM study_logs sl
        JOIN subjects s ON sl.subject_id = s.subject_id
        WHERE sl.user_id = %s
        GROUP BY s.name
    """, (user_id,))

    data = cursor.fetchall()
    db.close()
    return data

def get_notifications(user_id):
    db = connect()
    cursor = db.cursor(cursor=p.cursors.DictCursor)

    cursor.execute("""
        SELECT type, message, status, created_at
        FROM notifications 
        WHERE user_id = %s ORDER BY created_at DESC LIMIT 5
    """, (user_id,))

    data = cursor.fetchall()
    db.close()
    return data

def get_study_progress(user_id):
    db = connect()
    cursor = db.cursor()

    
    cursor.execute("""
        SELECT s.name, COALESCE(SUM(l.study_time), 0) 
        FROM subjects s 
        LEFT JOIN study_logs l ON s.subject_id = l.subject_id 
        WHERE s.user_id = %s 
        GROUP BY s.subject_id
    """, (user_id,))

    subject_data = cursor.fetchall()
    db.close()

    subjects = []
    
    for subject, hours in subject_data:
        percentage = min(100, (hours / get_goal_subject(user_id, subject)) * 100)
        subjects.append({
            "name": subject,
            "hours": hours,
            "percentage": round(percentage, 2)
        })

    return subjects


def get_goal_subject(user_id, subject_id):
    db = connect()
    cursor = db.cursor()

    cursor.execute("SELECT daily_goal_minutes FROM subjects WHERE user_id = %s and name = %s", (user_id, subject_id))
    goal = cursor.fetchone()[0]
    db.close()
    return goal



def getStudyHoursPerDay(user_id):
    """
    Fetch daily study hours for the last 30 days.
    """
    db = connect()
    cursor = db.cursor()

    cursor.execute("""
        SELECT date, SUM(study_time) 
        FROM study_logs 
        WHERE user_id = %s AND date >= %s 
        GROUP BY date 
        ORDER BY date ASC
    """, (user_id, dt.date.today() - dt.timedelta(days=30)))

    data = cursor.fetchall()
    db.close()

    study_hours = {str(row[0]): row[1] / 60 for row in data}  
    return study_hours


def mock_test_scores(user_id):
    """
    Fetch mock test scores for the last 30 days.
    """
    db = connect()
    cursor = db.cursor()

    cursor.execute("""
        SELECT date, score, total_marks 
        FROM mock_tests 
        WHERE user_id = %s AND date >= %s 
        ORDER BY date ASC
    """, (user_id, dt.date.today() - dt.timedelta(days=30)))

    data = cursor.fetchall()
    db.close()

    scores = [{"date": str(row[0]), "score": row[1], "total_marks": row[2]} for row in data]
    return scores

def log_mock_test(user_id, subject_name, score, total_marks, time_taken):
    try:
        db = connect()
        cursor = db.cursor()

        cursor.execute("SELECT subject_id FROM subjects WHERE name = %s AND user_id = %s", (subject_name, user_id))
        result = cursor.fetchone()

        if not result:
            return False, "Subject not found"

        subject_id = result[0]

        cursor.execute("""
            INSERT INTO mock_tests (user_id, subject_id, date, score, total_marks, time_taken) 
            VALUES (%s, %s, CURDATE(), %s, %s, %s)
        """, (user_id, subject_id, score, total_marks, time_taken))

        db.commit()
        return True, "Mock test logged successfully!"
    except Exception as e:
        print("Database Error:", str(e))  
        return False, f"Database error: {str(e)}"
    finally:
        cursor.close()
        db.close()


# def get_study_time():
#     conn = connect()
#     cursor = conn.cursor()

#     query = """
#     SELECT date, study_hours FROM study_log 
#     WHERE date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY) 
#     ORDER BY date;
#     """
#     cursor.execute(query)
#     data = cursor.fetchall()

#     cursor.close()
#     conn.close()

#     return jsonify(data)

from dbm import connect
import datetime

def get_study_logs_last_7_days(user_id):
    try:
        db = connect()
        cursor = db.cursor()

        today = datetime.date.today()
        start_date = today - datetime.timedelta(days=6)

        
        query = """
        SELECT s.name AS subject, sl.date, SUM(sl.study_time) AS total_study_time
        FROM study_logs sl
        JOIN subjects s ON sl.subject_id = s.subject_id
        WHERE sl.user_id = %s AND sl.date BETWEEN %s AND %s
        GROUP BY s.name, sl.date
        ORDER BY sl.date;
        """
        cursor.execute(query, (user_id, start_date, today))
        results = cursor.fetchall()

        # Initialize data in descending order (today to last 7 days)
        data = {str(today - datetime.timedelta(days=i)): {} for i in range(7)}

        for subject, date, total_study_time in results:
            date_str = str(date)
            if date_str not in data:
                data[date_str] = {}
            data[date_str][subject] = total_study_time

        # Ensure all subjects have a default 0 if missing on a particular date
        subjects_query = "SELECT DISTINCT name FROM subjects WHERE user_id = %s"
        cursor.execute(subjects_query, (user_id,))
        subjects = [row[0] for row in cursor.fetchall()]

        for date in data:
            for subject in subjects:
                if subject not in data[date]:
                    data[date][subject] = 0  # Default to 0 minutes if no study time recorded

        return data
    except Exception as e:
        print("Database Error:", e)
        return {}
    finally:
        cursor.close()
        db.close()


def user_exists(email):
    with connect2() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT user_id FROM users WHERE email = %s", (email,))
            return cursor.fetchone() is not None

def create_user(username, email, password_hash):
    with connect2() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
                (username, email, password_hash)
            )
            conn.commit()
            return cursor.lastrowid

def get_user_by_email(email):
    with connect2() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT user_id, username, email, password_hash FROM users WHERE email = %s", (email,))
            return cursor.fetchone()
        
import pymysql

def is_onboarded(user_id):
    """Check if the user has at least one subject. If yes, they are onboarded."""
    db = connect()  # Ensure connect() properly returns a pymysql connection object
    cursor = db.cursor(pymysql.cursors.DictCursor)  # DictCursor to return results as dictionaries

    try:
        query = "SELECT COUNT(*) as subject_count FROM subjects WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()  # Fetch the first row
        
        subject_count = result["subject_count"] if result else 0
        return "yes" if subject_count > 0 else "no"

    except Exception as e:
        print(f"Error in is_onboarded: {str(e)}")  # Log error for debugging
        return "no"
    
    finally:
        cursor.close()
        db.close()

def get_study_data(user_id, days=30):
    db = connect2()
    cursor = db.cursor()
    query = """
    SELECT date, subject_id, SUM(study_time) as total_time
    FROM study_logs
    WHERE user_id = %s AND date >= CURDATE() - INTERVAL %s DAY
    GROUP BY date, subject_id
    ORDER BY date ASC
    """
    cursor.execute(query, (user_id, days))  # ✅ Safe parameterized query
    return cursor.fetchall()
