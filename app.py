from flask import *
import dbm
import models
import datetime as dt
import recomend

from flask import request, jsonify, session
from werkzeug.security import check_password_hash
from flask import request, jsonify
from werkzeug.security import generate_password_hash


app =Flask(__name__)

app.secret_key = "key"

user = models.User(101, "sanchita warade", "sanchi@example.com", "hashedpassword123")
user_id=101

@app.route("/dashboard")
def dashboard():
    total_hours, goal_percentage = dbm.get_today_progress(user_id)
    current_streak, days_to_milestone = dbm.get_current_streak(user_id)
    total_xp = dbm.get_xp_progress(user_id)

    study_time_data = dbm.get_study_time_distribution(user_id, period="month")
    subject_distribution = dbm.get_subject_distribution(user_id)
    notifications = dbm.get_notifications(user_id)
    return render_template("dashboard.html", total_hours=total_hours, goal_percentage=goal_percentage, current_streak=current_streak,days_to_milestone=days_to_milestone, total_xp=total_xp, study_time_data=study_time_data, subject_distribution=subject_distribution, notifications=notifications)

@app.route("/insights")
def insights():
    total_hours, goal_percentage = dbm.get_today_progress(user_id)
    current_streak, days_to_milestone = dbm.get_current_streak(user_id)
    total_xp = dbm.get_xp_progress(user_id)
    return render_template("insights.html", total_hours=total_hours, goal_percentage=goal_percentage, current_streak=current_streak,days_to_milestone=days_to_milestone, total_xp=total_xp)
@app.route("/rewards")
def rewards():
    user_id = 101 
    
    subjects = dbm.get_study_progress(user_id)

    notifications = dbm.get_notifications(user_id)

    total_hours, goal_percentage = dbm.get_today_progress(user_id)
    current_streak, days_to_milestone = dbm.get_current_streak(user_id)
    total_xp = dbm.get_xp_progress(user_id)
    print("Study Hours:", type(dbm.getStudyHoursPerDay(user_id)))
    print("Mock Test Scores:", type(dbm.mock_test_scores(user_id)))


    return render_template("rewards.html", 
                           total_hours=total_hours, 
                           goal_percentage=goal_percentage, 
                           current_streak=current_streak,
                           days_to_milestone=days_to_milestone, 
                           total_xp=total_xp, 
                           subjects=subjects,
                           notifications=notifications,
                           AI_text=recomend.analyze_study_pattern(dbm.getStudyHoursPerDay(user_id), dbm.mock_test_scores(user_id)))  # Pass notifications

@app.route("/study_insights", methods=["GET"])
def study_insights():
    try:
        user_id = 101  # Example: Fetch user from session
        data = dbm.get_study_logs_last_7_days(user_id)

        return jsonify({"success": True, "data": data})
    except Exception as e:
        print("Server Error:", e)
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()

        if not email or not password:
            return jsonify({"success": False, "message": "Email and password are required"}), 400

        conn = dbm.connect()
        cursor = conn.cursor()

        cursor.execute("SELECT user_id, username, email, password_hash FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user and check_password_hash(user[3], password):  # user[3] = password_hash
            session["user_id"] = user[0]  # user[0] = user_id
            return jsonify({"success": True, "message": "Login successful!"}), 200
        else:
            return jsonify({"success": False, "message": "Invalid email or password"}), 401
    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"}), 500


@app.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.json
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()

        if not username or not email or not password:
            return jsonify({"success": False, "message": "All fields are required"}), 400

        hashed_password = generate_password_hash(password)

        # Insert user into database
        conn = dbm.connect()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
            (username, email, hashed_password)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"success": True, "message": "Signup successful! Please log in."}), 201
    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"}), 500


@app.route('/log_study_session', methods=['POST'])
def log_study_session():
    data = request.json
    user_id = 101
    subject_name = data.get('subject')
    duration = int(data.get('duration', 0))

    subject_id = dbm.get_subject_id(user_id, subject_name)
    if not subject_id:
        return jsonify({"success": False, "message": "Subject not found"}), 400

    success, message = dbm.insert_study_log(user_id, subject_id, duration)
    return jsonify({"success": success, "message": message})

@app.route("/log_mock_test", methods=["POST"])
def log_mock():
    try:
        data = request.json
        if not data:
            return jsonify({"success": False, "message": "Invalid JSON data received"}), 400

        user_id = 101  # Example: Fetch from session in real implementation
        subject_name = data.get("subject")
        score = int(data.get("score", 0))
        total_marks = int(data.get("totalMarks", 0))
        time_taken = int(data.get("timeTaken", 0))

        success, message = dbm.log_mock_test(user_id, subject_name, score, total_marks, time_taken)

        return jsonify({"success": success, "message": message})
    except Exception as e:
        print("Server Error:", str(e))
        return jsonify({"success": False, "message": "Internal server error"}), 500


# Render template
@app.route("/")
def index():
    return render_template("index.html")




if __name__=="__main__":
    app.run(debug="True")