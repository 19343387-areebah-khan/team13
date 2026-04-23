# Bit by Bit Habit Tracker
Team 13 | COMP5046

Google Drive: https://drive.google.com/drive/u/0/folders/1pWCd3y4Lce44kq6CwIw9vEMQLkew4BZq


## How to Run the App

**Prerequisites:** Python 3.10+

### 1. Clone the repository
```bash
git clone https://github.com/19343387-areebah-khan/team13.git
cd team13
```

### 2. Install dependencies
```bash
pip install flask flask-cors werkzeug
```

### 3. Set up the database (first time only)
```bash
python database/setup_db.py
```
This reads `habits.sql` and creates the `habit_tracker.db` database file locally.

### 4. Run the Flask server
```bash
python app.py
```

### 5. Open the app in a browser
