"""
=============================================================
SPRINT 2 - BACKEND UNIT TESTS
=============================================================
Tests for: Habit Creation (US6) & Mark Complete (US10)
Functions tested:
  - add_habit()              (Hamza)
  - get_habits_by_user_id()  (Hamza)
  - log_habit_completion()   (Hamza)
  - Flask route POST /habits (Areebah)
  - Flask route GET /habits  (Areebah)
  - Flask route POST /habits/complete (Hamza)
 
Linked Acceptance Criteria:
  - AC6.4 : Empty or invalid habit input triggers error
  - AC6.5 : Valid habit is saved to database
  - AC6.6 : Habits load from database on page load
  - AC6.7 : Habits are user-specific
  - AC10.3: Completion is saved to the database
  - AC10.4: Completion status persists after page reload
  - AC10.5: Completion is date-specific
 
Run with:
  cd C:\\Users\\areeb\\Downloads\\team13
  pytest tests/sprint2/test_habits_backend.py -v
=============================================================
"""
 
import sys
import os
import sqlite3
import pytest
 
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
 
 
# =============================================================
# TEST DATABASE SETUP
# We create one connection and patch conn.close() to do nothing
# so db_functions can't accidentally kill our test connection
# =============================================================
 
class NoCloseConnection:
    """Wraps a sqlite3 connection and makes close() a no-op."""
    def __init__(self, conn):
        self._conn = conn
 
    def cursor(self):
        return self._conn.cursor()
 
    def commit(self):
        self._conn.commit()
 
    def close(self):
        pass  # do nothing - keep connection alive
 
    def execute(self, *args, **kwargs):
        return self._conn.execute(*args, **kwargs)
 
    @property
    def row_factory(self):
        return self._conn.row_factory
 
    @row_factory.setter
    def row_factory(self, value):
        self._conn.row_factory = value
 
 
@pytest.fixture(autouse=True)
def test_db(monkeypatch):
    """Fresh in-memory DB for each test with close() disabled."""
    raw_conn = sqlite3.connect(":memory:")
    raw_conn.row_factory = sqlite3.Row
    conn = NoCloseConnection(raw_conn)
 
    cursor = raw_conn.cursor()
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            failed_attempts INTEGER DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS habits (
            habit_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            habit_type TEXT DEFAULT 'other',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        );
        CREATE TABLE IF NOT EXISTS habit_logs (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            status TEXT,
            note TEXT,
            FOREIGN KEY (habit_id) REFERENCES habits(habit_id)
        );
    """)
    cursor.execute(
        "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
        ("testuser", "test@test.com", "hashed")
    )
    cursor.execute(
        "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
        ("otheruser", "other@test.com", "hashed")
    )
    raw_conn.commit()
 
    monkeypatch.setattr("database.db_connections.get_connection", lambda: conn)
    monkeypatch.setattr("database.db_functions.get_connection", lambda: conn)
 
    yield raw_conn
    raw_conn.close()
 
 
# =============================================================
# ADD HABIT TESTS (Hamza)
# Linked to: AC6.5, AC6.7
# =============================================================
 
class TestAddHabit:
 
    def test_valid_habit_is_saved(self, test_db):
        """AC6.5 - A valid habit is inserted and returns a habit_id."""
        from database.db_functions import add_habit
        habit_id = add_habit(1, "Exercise", "health")
        assert habit_id is not None
        assert habit_id > 0
 
    def test_habit_appears_in_database(self, test_db):
        """AC6.5 - After adding, the habit can be retrieved from the database."""
        from database.db_functions import add_habit
        add_habit(1, "Read", "education")
        cursor = test_db.cursor()
        cursor.execute("SELECT * FROM habits WHERE user_id = 1")
        habits = cursor.fetchall()
        assert len(habits) == 1
        assert habits[0]["name"] == "Read"
 
    def test_multiple_habits_saved(self, test_db):
        """AC6.5 - Multiple habits can be added for the same user."""
        from database.db_functions import add_habit
        add_habit(1, "Exercise", "health")
        add_habit(1, "Read", "education")
        cursor = test_db.cursor()
        cursor.execute("SELECT * FROM habits WHERE user_id = 1")
        habits = cursor.fetchall()
        assert len(habits) == 2
 
 
# =============================================================
# GET HABITS TESTS (Hamza)
# Linked to: AC6.6, AC6.7
# =============================================================
 
class TestGetHabitsByUserId:
 
    def test_returns_empty_list_for_new_user(self, test_db):
        """AC6.6 - A user with no habits gets an empty list."""
        from database.db_functions import get_habits_by_user_id
        habits = get_habits_by_user_id(1)
        assert habits == []
 
    def test_returns_correct_habits_for_user(self, test_db):
        """AC6.6 - Returns only the habits belonging to the requested user."""
        from database.db_functions import add_habit, get_habits_by_user_id
        add_habit(1, "Exercise", "health")
        habits = get_habits_by_user_id(1)
        assert len(habits) == 1
        assert habits[0]["name"] == "Exercise"
 
    def test_habits_are_user_specific(self, test_db):
        """AC6.7 - User 1 and User 2 only see their own habits."""
        from database.db_functions import add_habit, get_habits_by_user_id
        add_habit(1, "User1 Habit", "health")
        add_habit(2, "User2 Habit", "health")
 
        user1_habits = get_habits_by_user_id(1)
        user2_habits = get_habits_by_user_id(2)
 
        assert len(user1_habits) == 1
        assert user1_habits[0]["name"] == "User1 Habit"
        assert len(user2_habits) == 1
        assert user2_habits[0]["name"] == "User2 Habit"
 
 
# =============================================================
# LOG HABIT COMPLETION TESTS (Hamza)
# Linked to: AC10.3, AC10.4, AC10.5
# =============================================================
 
class TestLogHabitCompletion:
 
    def test_completion_is_logged(self, test_db):
        """AC10.3 - Completing a habit inserts a record into habit_logs."""
        from database.db_functions import add_habit, log_habit_completion
        habit_id = add_habit(1, "Exercise", "health")
        result = log_habit_completion(1, habit_id, completed=True)
        assert result is True
 
        cursor = test_db.cursor()
        cursor.execute("SELECT * FROM habit_logs WHERE habit_id = ?", (habit_id,))
        log = cursor.fetchone()
        assert log is not None
        assert log["status"] == "complete"
 
    def test_wrong_user_cannot_log_completion(self, test_db):
        """AC10.3 - A user cannot log completion for another user's habit."""
        from database.db_functions import add_habit, log_habit_completion
        habit_id = add_habit(1, "Exercise", "health")
        result = log_habit_completion(999, habit_id, completed=True)
        assert result is False
 
    def test_completion_updates_existing_log(self, test_db):
        """AC10.4 - Logging completion twice today updates existing record."""
        from database.db_functions import add_habit, log_habit_completion
        habit_id = add_habit(1, "Exercise", "health")
        log_habit_completion(1, habit_id, completed=True)
        log_habit_completion(1, habit_id, completed=False)
 
        cursor = test_db.cursor()
        cursor.execute("SELECT * FROM habit_logs WHERE habit_id = ?", (habit_id,))
        logs = cursor.fetchall()
        assert len(logs) == 1
        assert logs[0]["status"] == "incomplete"
 
 
# =============================================================
# FLASK API ROUTE TESTS (Areebah)
# Linked to: AC6.4, AC6.5, AC6.6, AC10.3
# =============================================================
 
class TestHabitAPIRoutes:
 
    @pytest.fixture
    def client(self, test_db):
        import app as flask_app
        flask_app.app.config["TESTING"] = True
        with flask_app.app.test_client() as client:
            yield client
 
    def test_create_habit_missing_name(self, client):
        """AC6.4 - POST /habits with empty name returns error."""
        response = client.post("/habits", json={"user_id": 1, "name": "", "habit_type": "health"})
        data = response.get_json()
        assert data["success"] is False
        assert "name" in data["error"].lower()
 
    def test_create_habit_missing_user_id(self, client):
        """POST /habits without user_id returns error."""
        response = client.post("/habits", json={"name": "Exercise", "habit_type": "health"})
        data = response.get_json()
        assert data["success"] is False
        assert "user" in data["error"].lower()
 
    def test_create_habit_missing_type(self, client):
        """POST /habits without habit_type returns error."""
        response = client.post("/habits", json={"user_id": 1, "name": "Exercise", "habit_type": ""})
        data = response.get_json()
        assert data["success"] is False
 
    def test_get_habits_missing_user_id(self, client):
        """AC6.6 - GET /habits without user_id returns error."""
        response = client.get("/habits")
        data = response.get_json()
        assert data["success"] is False
        assert "user" in data["error"].lower()
 
    def test_complete_habit_missing_user_id(self, client):
        """POST /habits/complete without user_id returns error."""
        response = client.post("/habits/complete", json={"habit_id": 1, "completed": True})
        data = response.get_json()
        assert data["success"] is False
 
    def test_complete_habit_missing_habit_id(self, client):
        """POST /habits/complete without habit_id returns error."""
        response = client.post("/habits/complete", json={"user_id": 1, "completed": True})
        data = response.get_json()
        assert data["success"] is False
