from flask import Flask, request, jsonify, session, render_template, redirect, url_for
import dbm
import models
import recomend
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "key"  # Change this for production security

DEFAULT_TEST_USER_ID = "101"  # Default test user ID

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    user_id = session.get("user_id", DEFAULT_TEST_USER_ID)

    # If the user has no subjects, redirect to onboarding
    if dbm.is_onboarded(user_id) == "no":
        return redirect(url_for('onboarding'))

    total_hours, goal_percentage = dbm.get_today_progress(user_id)
    current_streak, days_to_milestone = dbm.get_current_streak(user_id)
    total_xp = dbm.get_xp_progress(user_id)
    study_time_data = dbm.get_study_time_distribution(user_id, period="month")
    subject_distribution = dbm.get_subject_distribution(user_id)
    notifications = dbm.get_notifications(user_id)
    user = dbm.get_user_by_id(user_id)

    return render_template(
        "dashboard.html", total_hours=total_hours, goal_percentage=goal_percentage,
        current_streak=current_streak, days_to_milestone=days_to_milestone,
        total_xp=total_xp, study_time_data=study_time_data,
        subject_distribution=subject_distribution, notifications=notifications, user=user
    )

@app.route('/onboarding', methods=['GET', 'POST'])
def onboarding():
    user_id = session.get("user_id", DEFAULT_TEST_USER_ID)

    if dbm.is_onboarded(user_id) == "yes":
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        data = request.get_json()
        first_name, last_name, subjects = data.get('firstName'), data.get('lastName'), data.get('subjects')

        if not first_name or not last_name or not subjects:
            return {"error": "Missing data"}, 400

        session['user'] = {'first_name': first_name, 'last_name': last_name}

        # Insert each subject into the database
        for subject in subjects:
            subject_data = (
                user_id,
                subject['name'],
                subject['daily_goal_minutes'],
                0  # Default value for total_minutes
            )
            dbm.insert_subject(subject_data)

        return {"message": "Success"}, 200

    return render_template('onboarding.html')


@app.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()

        # Extract and sanitize inputs
        username = data.get('username', '').strip()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '').strip()

        # Validate inputs
        if not username or not email or not password:
            return jsonify({"success": False, "message": "All fields are required"}), 400

        if "@" not in email or "." not in email:
            return jsonify({"success": False, "message": "Invalid email format"}), 400

        if len(password) < 6:
            return jsonify({"success": False, "message": "Password must be at least 6 characters long"}), 400

        # Check if user already exists
        if dbm.user_exists(email):
            return jsonify({"success": False, "message": "User already exists"}), 409

        # Hash the password securely
        hashed_password = generate_password_hash(password)

        # Create user in the database
        user_id = dbm.create_user(username, email, hashed_password)

        if user_id:
            session["user_id"] = user_id
            return jsonify({"success": True, "message": "Signup successful!", "user_id": user_id}), 201

        return jsonify({"success": False, "message": "Signup failed due to a server error"}), 500

    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"}), 500


@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        email, password = data.get('email', '').strip(), data.get('password', '').strip()

        if not email or not password:
            return jsonify({"success": False, "message": "Email and password are required"}), 400

        user = dbm.get_user_by_email(email)
        if user and check_password_hash(user['password_hash'], password):
            session["user_id"] = user["user_id"]
            return jsonify({"success": True, "message": "Login successful!"}), 200
        
        return jsonify({"success": False, "message": "Invalid email or password"}), 401
    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"}), 500

@app.route("/insights")
def insights():
    user_id = session.get("user_id", DEFAULT_TEST_USER_ID)

    total_hours, goal_percentage = dbm.get_today_progress(user_id)
    current_streak, days_to_milestone = dbm.get_current_streak(user_id)
    total_xp = dbm.get_xp_progress(user_id)

    return render_template("insights.html", total_hours=total_hours, goal_percentage=goal_percentage, 
                           current_streak=current_streak, days_to_milestone=days_to_milestone, total_xp=total_xp)

@app.route("/rewards")
def rewards():
    user_id = session.get("user_id", DEFAULT_TEST_USER_ID)

    subjects = dbm.get_study_progress(user_id)
    notifications = dbm.get_notifications(user_id)
    total_hours, goal_percentage = dbm.get_today_progress(user_id)
    current_streak, days_to_milestone = dbm.get_current_streak(user_id)
    total_xp = dbm.get_xp_progress(user_id)

    return render_template("rewards.html", total_hours=total_hours, goal_percentage=goal_percentage, 
                           current_streak=current_streak, days_to_milestone=days_to_milestone, total_xp=total_xp, 
                           subjects=subjects, notifications=notifications, 
                           AI_text=recomend.analyze_study_pattern(dbm.getStudyHoursPerDay(user_id), 
                                                                  dbm.mock_test_scores(user_id)))

@app.route("/study_insights", methods=["GET"])
def study_insights():
    try:
        user_id = session.get("user_id", DEFAULT_TEST_USER_ID)
        data = dbm.get_study_logs_last_7_days(user_id)
        return jsonify({"success": True, "data": data})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/log_study_session', methods=['POST'])
def log_study_session():
    data = request.json
    user_id = session.get("user_id", DEFAULT_TEST_USER_ID)
    subject_name, duration = data.get('subject'), int(data.get('duration', 0))

    subject_id = dbm.get_subject_id(user_id, subject_name)
    if not subject_id:
        return jsonify({"success": False, "message": "Subject not found"}), 400

    success, message = dbm.insert_study_log(user_id, subject_id, duration)
    return jsonify({"success": success, "message": message})

@app.route("/log_mock_test", methods=["POST"])
def log_mock():
    try:
        data = request.json
        user_id = session.get("user_id", DEFAULT_TEST_USER_ID)
        subject_name, score = data.get("subject"), int(data.get("score", 0))
        total_marks, time_taken = int(data.get("totalMarks", 0)), int(data.get("timeTaken", 0))

        success, message = dbm.log_mock_test(user_id, subject_name, score, total_marks, time_taken)
        return jsonify({"success": success, "message": message})
    except Exception as e:
        return jsonify({"success": False, "message": "Internal server error"}), 500



@app.route('/test')
def test():
    return render_template('test.html')

@app.route("/get_study_data", methods=["GET"])
def get_study_data():
    user_id = request.args.get("user_id", type=int)
    days = request.args.get("days", default=30, type=int)

    # Fetch data from the database
    raw_data = dbm.get_study_data(user_id, days)  # Your DB function

    # Convert dates to string format
    formatted_data = {
        str(row["date"]): {"subject_id": row["subject_id"], "total_time": row["total_time"]}
        for row in raw_data
    }

    return jsonify(formatted_data)  # ✅ Now safe for JSON serialization

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# --- Refined Insights API Endpoints ---
@app.route("/api/study_time_distribution")
def api_study_time_distribution():
    user_id = session.get("user_id", DEFAULT_TEST_USER_ID)
    period = request.args.get("period", "week")
    import datetime as dt
    today = dt.date.today()
    if period == "week":
        start = today - dt.timedelta(days=6)
        end = today
    else:  # month
        start = today - dt.timedelta(days=29)
        end = today
    db = dbm.connect()
    cursor = db.cursor(dbm.p.cursors.DictCursor)
    cursor.execute("""
        SELECT DATE(date) AS study_date, SUM(study_time) AS total_time
        FROM study_logs
        WHERE user_id = %s AND date BETWEEN %s AND %s
        GROUP BY study_date ORDER BY study_date
    """, (user_id, start, end))
    data = cursor.fetchall()
    db.close()
    # Fill missing days with 0
    days = [(start + dt.timedelta(days=i)).isoformat() for i in range((end-start).days+1)]
    date_map = {str(row["study_date"]): float(row["total_time"]) / 60 if row["total_time"] else 0 for row in data}
    hours = [date_map.get(day, 0) for day in days]
    return jsonify({"dates": days, "hours": hours})

@app.route("/api/subject_distribution")
def api_subject_distribution():
    user_id = session.get("user_id", DEFAULT_TEST_USER_ID)
    period = request.args.get("period", "current")
    import datetime as dt
    today = dt.date.today()
    # Get week range
    if period == "current":
        start = today - dt.timedelta(days=today.weekday())
        end = start + dt.timedelta(days=6)
    else:  # previous
        end = today - dt.timedelta(days=today.weekday() + 1)
        start = end - dt.timedelta(days=6)
    db = dbm.connect()
    cursor = db.cursor(dbm.p.cursors.DictCursor)
    cursor.execute("""
        SELECT s.name AS subject, SUM(sl.study_time) AS total_time
        FROM study_logs sl
        JOIN subjects s ON sl.subject_id = s.subject_id
        WHERE sl.user_id = %s AND sl.date BETWEEN %s AND %s
        GROUP BY s.name
    """, (user_id, start, end))
    data = cursor.fetchall()
    db.close()
    result = [{"value": float(row["total_time"]) / 60 if row["total_time"] else 0, "name": row["subject"]} for row in data]
    return jsonify(result)

@app.route("/api/daily_subject_time")
def api_daily_subject_time():
    user_id = session.get("user_id", DEFAULT_TEST_USER_ID)
    period = request.args.get("period", "today")
    import datetime as dt
    today = dt.date.today()
    if period == "today":
        target_date = today
    else:
        target_date = today - dt.timedelta(days=1)
    db = dbm.connect()
    cursor = db.cursor(dbm.p.cursors.DictCursor)
    cursor.execute("""
        SELECT s.name AS subject, SUM(sl.study_time) AS total_time
        FROM study_logs sl
        JOIN subjects s ON sl.subject_id = s.subject_id
        WHERE sl.user_id = %s AND sl.date = %s
        GROUP BY s.name
    """, (user_id, target_date))
    data = cursor.fetchall()
    db.close()
    # Format: list of {subject, hours}
    result = [{"subject": row["subject"], "hours": float(row["total_time"]) / 60 if row["total_time"] else 0} for row in data]
    return jsonify(result)

@app.route("/api/weekly_progress")
def api_weekly_progress():
    user_id = session.get("user_id", DEFAULT_TEST_USER_ID)
    period = request.args.get("period", "current")
    import datetime as dt
    today = dt.date.today()
    # Get start of week (Monday)
    if period == "current":
        start = today - dt.timedelta(days=today.weekday())
        end = start + dt.timedelta(days=6)
    else:
        end = today - dt.timedelta(days=today.weekday() + 1)
        start = end - dt.timedelta(days=6)
    db = dbm.connect()
    cursor = db.cursor(dbm.p.cursors.DictCursor)
    cursor.execute("""
        SELECT s.name AS subject, sl.date, SUM(sl.study_time) AS total_study_time
        FROM study_logs sl
        JOIN subjects s ON sl.subject_id = s.subject_id
        WHERE sl.user_id = %s AND sl.date BETWEEN %s AND %s
        GROUP BY s.name, sl.date
        ORDER BY sl.date
    """, (user_id, start, end))
    results = cursor.fetchall()
    db.close()
    # Build per-day, per-subject dict
    days = [(start + dt.timedelta(days=i)).isoformat() for i in range(7)]
    subjects = list({row["subject"] for row in results})
    # Build {date: {subject: hours}}
    day_subject = {d: {s: 0 for s in subjects} for d in days}
    for row in results:
        d = row["date"].isoformat() if hasattr(row["date"], 'isoformat') else str(row["date"])
        s = row["subject"]
        h = float(row["total_study_time"]) / 60 if row["total_study_time"] else 0
        day_subject[d][s] = h
    # For each day, sum all subjects for 'hours', and set a target (e.g., 5)
    progress = [{"date": d, "hours": sum(day_subject[d].values()), "target": 5} for d in days]
    return jsonify(progress)

if __name__ == "__main__":
    app.run(debug=True)
