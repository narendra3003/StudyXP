
class User:
    def __init__(self, user_id, username, email, password_hash, total_xp=0, current_streak=0, last_study_date=None, preferred_study_time=None):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.total_xp = total_xp
        self.current_streak = current_streak
        self.last_study_date = last_study_date
        self.preferred_study_time = preferred_study_time


    def to_dict(self):
        """Returns user data as a dictionary."""
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "total_xp": self.total_xp,
            "current_streak": self.current_streak,
            "last_study_date": self.last_study_date
        }


class StudySession:
    """Represents a study session log."""
    
    def __init__(self, user_id, subject_id, date, study_time, notes=""):
        self.user_id = user_id
        self.subject_id = subject_id
        self.date = date
        self.study_time = study_time
        self.notes = notes

    def to_dict(self):
        """Returns study session data as a dictionary."""
        return {
            "user_id": self.user_id,
            "subject_id": self.subject_id,
            "date": self.date,
            "study_time": self.study_time,
            "notes": self.notes
        }


class MockTest:
    """Represents a mock test record."""
    
    def __init__(self, user_id, subject_id, date, score, total_marks, time_taken):
        self.user_id = user_id
        self.subject_id = subject_id
        self.date = date
        self.score = score
        self.total_marks = total_marks
        self.time_taken = time_taken

    def to_dict(self):
        """Returns mock test data as a dictionary."""
        return {
            "user_id": self.user_id,
            "subject_id": self.subject_id,
            "date": self.date,
            "score": self.score,
            "total_marks": self.total_marks,
            "time_taken": self.time_taken
        }
