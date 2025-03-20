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

    # If onboarding is already done, redirect to dashboard
    if dbm.is_onboarded(user_id) == "yes":
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        first_name, last_name = request.form.get('firstName'), request.form.get('lastName')
        subject_name = request.form.get('subjectName')

        # Save user details in session
        session['user'] = {'first_name': first_name, 'last_name': last_name}

        # Add a subject to complete onboarding
        query = "INSERT INTO subjects (user_id, name) VALUES (%s, %s)"
        dbm.execute_query(query, (user_id, subject_name))

        return redirect(url_for('dashboard'))

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

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
