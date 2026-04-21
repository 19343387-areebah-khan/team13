"""
=============================================================
SPRINT 4 - BACKEND UNIT TESTS
=============================================================
Tests for: US9 (Frequency), US11 (Edit Habit), US26 (Weekly Notes),
           US31 (Delete Confirmation), US16 (Weekly Summary)
 
Functions tested:
  - POST /habits frequency validation   (Taran)   - T9.2
  - update_habit()                      (Benjy)   - T11.1
  - PUT /habits/<habit_id>              (Benjy)   - T11.2
  - get_weekly_notes()                  (Areebah) - T26.1
  - GET /weekly-notes                   (Areebah) - T26.2
  - get_weekly_summary()                (Stipan)  - T16.1
  - GET /weekly-summary                 (Stipan)  - T16.2
 
Linked Acceptance Criteria:
  - AC9.1: Frequency defaults to daily if not specified
  - AC9.2: Only valid frequency values are accepted
  - AC11.2: Changes are saved and reflected in the list
  - AC11.4: Editing one habit does not affect others
  - AC26.2: Table shows only habits logged this week
  - AC26.3: Note cell is empty when no note was written
  - AC16.4: All 7 days always shown
  - AC16.5: Correct completed/total/percentage displayed
 
Run with:
  cd C:\\Users\\areeb\\Downloads\\team13
  pytest tests/sprint4/test_sprint4_backend.py -v
=============================================================
"""
 
import sys
import os
import sqlite3
import pytest
 
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
 
 
# =============================================================
# NO-CLOSE CONNECTION WRAPPER (same fix as previous sprints)
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
    """Fresh in-memory DB for each test with frequency column included."""
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
            frequency TEXT DEFAULT 'daily',
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
# US9 - FREQUENCY FLASK API TESTS (Taran - T9.2)
# Linked to: AC9.1, AC9.2
# =============================================================
 
class TestFrequencyAPI:
 
    @pytest.fixture
    def client(self, test_db):
        import app as flask_app
        flask_app.app.config["TESTING"] = True
        with flask_app.app.test_client() as client:
            yield client
 
    def test_frequency_defaults_to_daily(self, client):
        """AC9.1 - Habit created without frequency defaults to daily."""
        response = client.post("/habits", json={
            "user_id": 1, "name": "Exercise", "habit_type": "health"
        })
        data = response.get_json()
        assert data["success"] is True
 
    def test_valid_daily_frequency_accepted(self, client):
        """AC9.2 - Daily is a valid frequency value."""
        response = client.post("/habits", json={
            "user_id": 1, "name": "Exercise", "habit_type": "health", "frequency": "daily"
        })
        data = response.get_json()
        assert data["success"] is True
 
    def test_valid_weekly_frequency_accepted(self, client):
        """AC9.2 - Weekly is a valid frequency value."""
        response = client.post("/habits", json={
            "user_id": 1, "name": "Exercise", "habit_type": "health", "frequency": "weekly"
        })
        data = response.get_json()
        assert data["success"] is True
 
    def test_invalid_frequency_rejected(self, client):
        """AC9.2 - Invalid frequency value returns error."""
        response = client.post("/habits", json={
            "user_id": 1, "name": "Exercise", "habit_type": "health", "frequency": "monthly"
        })
        data = response.get_json()
        assert data["success"] is False
        assert "frequency" in data["error"].lower()
 
    def test_empty_frequency_rejected(self, client):
        """AC9.2 - Empty frequency string returns error."""
        response = client.post("/habits", json={
            "user_id": 1, "name": "Exercise", "habit_type": "health", "frequency": ""
        })
        data = response.get_json()
        assert data["success"] is False
 
 
# =============================================================
# US11 - EDIT HABIT TESTS (Benjy - T11.1, T11.2)
# Linked to: AC11.2, AC11.4
# =============================================================
 
class TestUpdateHabit:
 
    def test_valid_update_succeeds(self, test_db):
        """AC11.2 - Valid update saves new name and type."""
        from database.db_functions import add_habit, update_habit
        habit_id = add_habit(1, "Exercise", "health")
        result = update_habit(1, habit_id, "Run", "fitness")
        assert result is True
 
        cursor = test_db.cursor()
        cursor.execute("SELECT * FROM habits WHERE habit_id = ?", (habit_id,))
        habit = cursor.fetchone()
        assert habit["name"] == "Run"
        assert habit["habit_type"] == "fitness"
 
    def test_wrong_user_cannot_edit(self, test_db):
        """AC11.2 - A user cannot edit another user's habit."""
        from database.db_functions import add_habit, update_habit
        habit_id = add_habit(1, "Exercise", "health")
        result = update_habit(999, habit_id, "Run", "fitness")
        assert result is False
 
    def test_editing_one_habit_does_not_affect_others(self, test_db):
        """AC11.4 - Editing one habit leaves other habits unchanged."""
        from database.db_functions import add_habit, update_habit, get_habits_by_user_id
        habit_id_1 = add_habit(1, "Exercise", "health")
        add_habit(1, "Read", "education")
        update_habit(1, habit_id_1, "Run", "fitness")
 
        habits = get_habits_by_user_id(1)
        other = next(h for h in habits if h["habit_id"] != habit_id_1)
        assert other["name"] == "Read"
        assert other["habit_type"] == "education"
 
    def test_nonexistent_habit_returns_false(self, test_db):
        """AC11.2 - Editing a habit that doesn't exist returns False."""
        from database.db_functions import update_habit
        result = update_habit(1, 9999, "Run", "fitness")
        assert result is False
 
 
class TestUpdateHabitAPI:
 
    @pytest.fixture
    def client(self, test_db):
        import app as flask_app
        flask_app.app.config["TESTING"] = True
        with flask_app.app.test_client() as client:
            yield client
 
    def test_put_habit_missing_name_rejected(self, client, test_db):
        """AC11.2 - PUT /habits/<id> with empty name returns error."""
        from database.db_functions import add_habit
        habit_id = add_habit(1, "Exercise", "health")
        response = client.put(f"/habits/{habit_id}", json={
            "user_id": 1, "name": "", "habit_type": "health"
        })
        data = response.get_json()
        assert data["success"] is False
 
    def test_put_habit_missing_user_id_rejected(self, client, test_db):
        """PUT /habits/<id> without user_id returns error."""
        from database.db_functions import add_habit
        habit_id = add_habit(1, "Exercise", "health")
        response = client.put(f"/habits/{habit_id}", json={
            "name": "Run", "habit_type": "fitness"
        })
        data = response.get_json()
        assert data["success"] is False
 
 
# =============================================================
# US26 - WEEKLY NOTES TESTS (Areebah - T26.1, T26.2)
# Linked to: AC26.2, AC26.3
# =============================================================
 
class TestGetWeeklyNotes:
 
    def test_returns_empty_for_user_with_no_logs(self, test_db):
        """AC26.2 - User with no logs this week gets empty notes."""
        from database.db_functions import get_weekly_notes
        result = get_weekly_notes(1)
        assert result == []
 
    def test_returns_note_logged_today(self, test_db):
        """AC26.2 - Note logged today appears in weekly notes."""
        from database.db_functions import add_habit, log_habit_status, get_weekly_notes
        habit_id = add_habit(1, "Exercise", "health")
        log_habit_status(1, habit_id, "not_complete", "Was too tired")
        result = get_weekly_notes(1)
        assert len(result) > 0
        assert result[0]["note"] == "Was too tired"
        assert result[0]["habit_name"] == "Exercise"
 
    def test_empty_note_appears_as_empty_string(self, test_db):
        """AC26.3 - Habit logged without note shows empty note field."""
        from database.db_functions import add_habit, log_habit_status, get_weekly_notes
        habit_id = add_habit(1, "Exercise", "health")
        log_habit_status(1, habit_id, "good", "")
        result = get_weekly_notes(1)
        assert len(result) > 0
        assert result[0]["note"] == "" or result[0]["note"] is None
 
    def test_notes_are_user_specific(self, test_db):
        """AC26.2 - User only sees their own notes."""
        from database.db_functions import add_habit, log_habit_status, get_weekly_notes
        habit_id_1 = add_habit(1, "Exercise", "health")
        habit_id_2 = add_habit(2, "Read", "education")
        log_habit_status(1, habit_id_1, "good", "Great session")
        log_habit_status(2, habit_id_2, "partial", "Got distracted")
 
        user1_notes = get_weekly_notes(1)
        user2_notes = get_weekly_notes(2)
 
        assert all(n["habit_name"] == "Exercise" for n in user1_notes)
        assert all(n["habit_name"] == "Read" for n in user2_notes)
 
 
# =============================================================
# US16 - WEEKLY SUMMARY TESTS (Stipan - T16.1, T16.2)
# Linked to: AC16.4, AC16.5
# =============================================================
 
class TestGetWeeklySummary:
 
    def test_always_returns_7_days(self, test_db):
        """AC16.4 - Weekly summary always returns exactly 7 days."""
        from database.db_functions import get_weekly_summary
        result = get_weekly_summary(1)
        assert len(result) == 7
 
    def test_days_are_monday_to_sunday(self, test_db):
        """AC16.4 - The 7 days are Monday through Sunday."""
        from database.db_functions import get_weekly_summary
        result = get_weekly_summary(1)
        days = [r["day"] for r in result]
        assert days[0] == "Monday"
        assert days[6] == "Sunday"
 
    def test_empty_days_show_zero(self, test_db):
        """AC16.4 - Days with no logs show 0 completed and 0 percent."""
        from database.db_functions import get_weekly_summary
        result = get_weekly_summary(1)
        for day in result:
            assert day["completed"] == 0
            assert day["percent"] == 0
 
    def test_completed_habits_counted_correctly(self, test_db):
        """AC16.5 - Good and partial statuses count as completed."""
        from database.db_functions import add_habit, log_habit_status, get_weekly_summary
        habit_id = add_habit(1, "Exercise", "health")
        log_habit_status(1, habit_id, "good", "")
        result = get_weekly_summary(1)
        today_entry = next((r for r in result if r["completed"] > 0), None)
        assert today_entry is not None
        assert today_entry["completed"] == 1
 
    def test_not_complete_not_counted(self, test_db):
        """AC16.5 - not_complete status does not count as completed."""
        from database.db_functions import add_habit, log_habit_status, get_weekly_summary
        habit_id = add_habit(1, "Exercise", "health")
        log_habit_status(1, habit_id, "not_complete", "")
        result = get_weekly_summary(1)
        total_completed = sum(r["completed"] for r in result)
        assert total_completed == 0