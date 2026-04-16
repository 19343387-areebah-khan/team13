"""
=============================================================
SPRINT 3 - BACKEND UNIT TESTS
=============================================================
Tests for: US18 (Log Status), US14 (Heatmap), US12 (Delete Habit)
 
Functions tested:
  - log_habit_status()    (Areebah) - T18.7
  - get_heatmap_data()    (Hamza)   - T14.6
  - delete_habit()        (Benjy)   - T12.4
  - POST /habits/status   (Areebah) - T18.6
  - DELETE /habits        (Benjy)   - T12.3
  - GET /heatmap          (Hamza)   - T14.5
 
Linked Acceptance Criteria:
  - AC18.5: Invalid status shows error
  - AC18.6: Habit list reflects today's logged status on page load
  - AC14.4: Heatmap data loads automatically
  - AC14.6: Days with no activity default to grey
  - AC12.2: Clicking delete removes habit from UI immediately
  - AC12.3: Deleted habit does not reappear after refresh
  - AC12.4: Deleted habit does not reappear after logging back in
 
Run with:
  cd C:\\Users\\areeb\\Downloads\\team13
  pytest tests/sprint3/test_sprint3_backend.py -v
=============================================================
"""
 
import sys
import os
import sqlite3
import pytest
 
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
 
 
# =============================================================
# NO-CLOSE CONNECTION WRAPPER (same fix as Sprint 2)
# =============================================================
 
class NoCloseConnection:
    def __init__(self, conn):
        self._conn = conn
    def cursor(self):
        return self._conn.cursor()
    def commit(self):
        self._conn.commit()
    def close(self):
        pass
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
    raw_conn.commit()
 
    monkeypatch.setattr("database.db_connections.get_connection", lambda: conn)
    monkeypatch.setattr("database.db_functions.get_connection", lambda: conn)
 
    yield raw_conn
    raw_conn.close()
 
 
# =============================================================
# US18 - LOG HABIT STATUS TESTS (Areebah - T18.7)
# Linked to: AC18.5, AC18.6
# =============================================================
 
class TestLogHabitStatus:
 
    def test_valid_good_status_is_logged(self, test_db):
        """AC18.6 - Good status is saved to habit_logs."""
        from database.db_functions import add_habit, log_habit_status
        habit_id = add_habit(1, "Exercise", "health")
        result = log_habit_status(1, habit_id, "good", "")
        assert result is True
 
        cursor = test_db.cursor()
        cursor.execute("SELECT * FROM habit_logs WHERE habit_id = ?", (habit_id,))
        log = cursor.fetchone()
        assert log["status"] == "good"
 
    def test_valid_partial_status_is_logged(self, test_db):
        """AC18.6 - Partial status is saved correctly."""
        from database.db_functions import add_habit, log_habit_status
        habit_id = add_habit(1, "Exercise", "health")
        result = log_habit_status(1, habit_id, "partial", "")
        assert result is True
 
        cursor = test_db.cursor()
        cursor.execute("SELECT * FROM habit_logs WHERE habit_id = ?", (habit_id,))
        log = cursor.fetchone()
        assert log["status"] == "partial"
 
    def test_valid_not_complete_status_with_note(self, test_db):
        """AC18.6 - Not complete status with note is saved correctly."""
        from database.db_functions import add_habit, log_habit_status
        habit_id = add_habit(1, "Exercise", "health")
        result = log_habit_status(1, habit_id, "not_complete", "Was too tired")
        assert result is True
 
        cursor = test_db.cursor()
        cursor.execute("SELECT * FROM habit_logs WHERE habit_id = ?", (habit_id,))
        log = cursor.fetchone()
        assert log["status"] == "not_complete"
        assert log["note"] == "Was too tired"
 
    def test_wrong_user_cannot_log_status(self, test_db):
        """AC18.5 - A user cannot log status for another user's habit."""
        from database.db_functions import add_habit, log_habit_status
        habit_id = add_habit(1, "Exercise", "health")
        result = log_habit_status(999, habit_id, "good", "")
        assert result is False
 
    def test_status_updates_existing_log(self, test_db):
        """AC18.6 - Logging status twice today updates existing record."""
        from database.db_functions import add_habit, log_habit_status
        habit_id = add_habit(1, "Exercise", "health")
        log_habit_status(1, habit_id, "good", "")
        log_habit_status(1, habit_id, "partial", "Got tired")
 
        cursor = test_db.cursor()
        cursor.execute("SELECT * FROM habit_logs WHERE habit_id = ?", (habit_id,))
        logs = cursor.fetchall()
        assert len(logs) == 1
        assert logs[0]["status"] == "partial"
        assert logs[0]["note"] == "Got tired"
 
 
# =============================================================
# US18 - FLASK API ROUTE TESTS (Areebah - T18.6)
# Linked to: AC18.5
# =============================================================
 
class TestHabitStatusAPI:
 
    @pytest.fixture
    def client(self, test_db):
        import app as flask_app
        flask_app.app.config["TESTING"] = True
        with flask_app.app.test_client() as client:
            yield client
 
    def test_invalid_status_rejected(self, client):
        """AC18.5 - Invalid status value returns error."""
        response = client.post("/habits/status", json={
            "user_id": 1, "habit_id": 1, "status": "invalid_status", "note": ""
        })
        data = response.get_json()
        assert data["success"] is False
        assert "invalid" in data["error"].lower()
 
    def test_missing_user_id_rejected(self, client):
        """AC18.5 - Missing user_id returns error."""
        response = client.post("/habits/status", json={
            "habit_id": 1, "status": "good", "note": ""
        })
        data = response.get_json()
        assert data["success"] is False
 
    def test_missing_habit_id_rejected(self, client):
        """AC18.5 - Missing habit_id returns error."""
        response = client.post("/habits/status", json={
            "user_id": 1, "status": "good", "note": ""
        })
        data = response.get_json()
        assert data["success"] is False
 
    def test_empty_status_rejected(self, client):
        """AC18.5 - Empty status string returns error."""
        response = client.post("/habits/status", json={
            "user_id": 1, "habit_id": 1, "status": "", "note": ""
        })
        data = response.get_json()
        assert data["success"] is False
 
 
# =============================================================
# US14 - HEATMAP DATA TESTS (Hamza - T14.6)
# Linked to: AC14.4, AC14.6
# =============================================================
 
class TestGetHeatmapData:
 
    def test_returns_empty_for_user_with_no_habits(self, test_db):
        """AC14.6 - User with no habits gets empty heatmap data."""
        from database.db_functions import get_heatmap_data
        result = get_heatmap_data(1)
        assert result == []
 
    def test_returns_empty_for_user_with_no_logs(self, test_db):
        """AC14.6 - User with habits but no logs gets empty heatmap data."""
        from database.db_functions import add_habit, get_heatmap_data
        add_habit(1, "Exercise", "health")
        result = get_heatmap_data(1)
        assert result == []
 
    def test_returns_data_after_logging(self, test_db):
        """AC14.4 - After logging a habit, heatmap data is returned."""
        from database.db_functions import add_habit, log_habit_status, get_heatmap_data
        habit_id = add_habit(1, "Exercise", "health")
        log_habit_status(1, habit_id, "good", "")
        result = get_heatmap_data(1)
        assert len(result) > 0
 
    def test_ratio_is_between_0_and_1(self, test_db):
        """AC14.6 - Ratio value is always between 0 and 1."""
        from database.db_functions import add_habit, log_habit_status, get_heatmap_data
        habit_id = add_habit(1, "Exercise", "health")
        log_habit_status(1, habit_id, "good", "")
        result = get_heatmap_data(1)
        for entry in result:
            assert 0 <= entry["ratio"] <= 1
 
    def test_heatmap_missing_user_id(self):
        """AC14.4 - GET /heatmap without user_id returns error."""
        import app as flask_app
        flask_app.app.config["TESTING"] = True
        with flask_app.app.test_client() as client:
            response = client.get("/heatmap")
            assert response.status_code == 400
 
 
# =============================================================
# US12 - DELETE HABIT TESTS (Benjy - T12.3, T12.4)
# Linked to: AC12.2, AC12.3, AC12.4
# =============================================================
 
class TestDeleteHabit:
 
    def test_habit_is_deleted(self, test_db):
        """AC12.3 - Deleting a habit removes it from the database."""
        from database.db_functions import add_habit, delete_habit
        habit_id = add_habit(1, "Exercise", "health")
        result = delete_habit(1, habit_id)
        assert result is True
 
        cursor = test_db.cursor()
        cursor.execute("SELECT * FROM habits WHERE habit_id = ?", (habit_id,))
        habit = cursor.fetchone()
        assert habit is None
 
    def test_deleted_habit_does_not_reappear(self, test_db):
        """AC12.4 - After deletion, habit is not returned in habit list."""
        from database.db_functions import add_habit, delete_habit, get_habits_by_user_id
        habit_id = add_habit(1, "Exercise", "health")
        delete_habit(1, habit_id)
        habits = get_habits_by_user_id(1)
        assert len(habits) == 0
 
    def test_wrong_user_cannot_delete(self, test_db):
        """AC12.3 - A user cannot delete another user's habit."""
        from database.db_functions import add_habit, delete_habit
        habit_id = add_habit(1, "Exercise", "health")
        result = delete_habit(999, habit_id)
        assert result is False
 
    def test_deleting_nonexistent_habit_returns_false(self, test_db):
        """Deleting a habit that doesn't exist returns False."""
        from database.db_functions import delete_habit
        result = delete_habit(1, 9999)
        assert result is False
 
    def test_only_specified_habit_deleted(self, test_db):
        """AC12.3 - Only the specified habit is deleted, others remain."""
        from database.db_functions import add_habit, delete_habit, get_habits_by_user_id
        habit_id_1 = add_habit(1, "Exercise", "health")
        add_habit(1, "Read", "education")
        delete_habit(1, habit_id_1)
        habits = get_habits_by_user_id(1)
        assert len(habits) == 1
        assert habits[0]["name"] == "Read"
        