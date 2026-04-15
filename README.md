How to Run the App

Prerequisites: Python 3.10+

1.  Clone the repository:
git clone https://github.com/19343387-areebah-khan/team13.git
cd team13

2.  Install dependencies:
   
pip install

flask

flask-cors

werkzeug

4.  Set up the database (first time only):

python database/setup_db.py

Note: This reads habits.sql and creates the habit_tracker.db database file locally.

6.  Run the Flask server:
  
python app.py

8.  Open the app in a browser:

http://localhost:5000

The login page will load automatically.
