##def handle_register_submit():
##def handle_login_submit():
##def showLoginErrors(errors)
##def showRegisterErrors(errors)
from services.auth_service import register_user, login_user
from database.db_functions import get_user_by_email, get_user_by_username, update_failed_attempts, reset_failed_attempts
from database.db_connections import get_connection

from flask import Flask, request, jsonify, send_from_directory
from services.auth_service import register_user, login_user
from flask_cors import CORS  # <-- import CORS


app = Flask(__name__, static_folder="frontend", static_url_path="")
CORS(app)  # <-- enable CORS for all routes

# --------------------------------------
# Serve HTML files from the frontend folder
# --------------------------------------
@app.route('/<path:filename>')
def serve_file(filename):
    return send_from_directory(app.static_folder, filename)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, "login.html")

# --------------------------------------
# API endpoints for login and register
# --------------------------------------
@app.route('/login', methods=['POST'])
def api_login():
    data = request.get_json()
    result = login_user(data)
    return jsonify(result)

@app.route('/register', methods=['POST'])
def api_register():
    data = request.get_json()
    result = register_user(data)
    return jsonify(result)


# API endpoints for habits Sprint 2 (Areebah)


# T6.5: POST /habits create a new habit
# Receives: { user_id, name, habit_type } from frontend
# Returns: { success: True } or { success: False, error: "..." }
@app.route('/habits', methods=['POST'])
def api_create_habit():
    data = request.get_json()

    # get the fields from the request
    user_id = data.get("user_id")
    name = data.get("name", "").strip()
    habit_type = data.get("habit_type", "").strip()

    # validate: user_id must exist
    if not user_id:
        return jsonify({"success": False, "error": "User ID is required"})

    # validate: habit name cannot be empty
    if not name:
        return jsonify({"success": False, "error": "Habit name is required"})

    # validate: habit type cannot be empty
    if not habit_type:
        return jsonify({"success": False, "error": "Habit type is required"})

    # save to database
    # TODO: REPLACE W STIPAN add_habit(user_id, name, habit_type) from db_functions.py (T6.7)
    # i only did this so i can test my tasks 
    try:
        from database.db_connections import get_connection
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO habits (user_id, name, habit_type) VALUES (?, ?, ?)",
            (user_id, name, habit_type)
        )
        conn.commit()
        habit_id = cursor.lastrowid
        conn.close()
        return jsonify({"success": True, "habit_id": habit_id})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


# T6.6: GET /habits — get all habits for a user
# Receives: user_id as a query parameter e.g. /habits?user_id=1
# Returns: { success: True, habits: [...] }
@app.route('/habits', methods=['GET'])
def api_get_habits():
    user_id = request.args.get("user_id")

    if not user_id:
        return jsonify({"success": False, "error": "User ID is required"})

    try:
        from database.db_functions import get_habits_by_user_id
        habits = get_habits_by_user_id(user_id)
        return jsonify({"success": True, "habits": habits})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# T10.3: POST /habits/complete — log habit completion (Hamza)
# Receives: { user_id, habit_id, completed } from frontend
# Returns: { success: True } or { success: False, error: "..." }
@app.route('/habits/complete', methods=['POST'])
def api_complete_habit():
    data = request.get_json()

    user_id = data.get("user_id")
    habit_id = data.get("habit_id")
    completed = data.get("completed")

    if not user_id:
        return jsonify({"success": False, "error": "User ID is required"})
    if not habit_id:
        return jsonify({"success": False, "error": "Habit ID is required"})
    if completed is None:
        return jsonify({"success": False, "error": "Completed status is required"})

    try:
        from database.db_functions import log_habit_completion
        result = log_habit_completion(int(user_id), int(habit_id), completed)
        if result:
            return jsonify({"success": True})
        else:
            return jsonify({"success": False, "error": "Habit not found or does not belong to user"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# T18.6: POST /habits/status  log habit completion status and note (Areebah)
# Receives: { user_id, habit_id, status, note } from frontend
# Returns: { success: True } or { success: False, error: "..." }
@app.route('/habits/status', methods=['POST'])
def api_habit_status():
    data = request.get_json()

    user_id = data.get("user_id")
    habit_id = data.get("habit_id")
    status = data.get("status", "").strip()
    note = data.get("note", "").strip()

    if not user_id:
        return jsonify({"success": False, "error": "User ID is required"})
    if not habit_id:
        return jsonify({"success": False, "error": "Habit ID is required"})

    # validate status is one of the three allowed values
    valid_statuses = ["good", "partial", "not_complete"]
    if status not in valid_statuses:
        return jsonify({"success": False, "error": "Invalid status value"})

    try:
        from database.db_functions import log_habit_status
        result = log_habit_status(int(user_id), int(habit_id), status, note)
        if result:
            return jsonify({"success": True})
        else:
            return jsonify({"success": False, "error": "Habit not found or does not belong to user"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@app.route("/habits", methods=["DELETE"])
def api_delete_habit():
    data = request.get_json()
    user_id = data.get("user_id")
    habit_id = data.get("habit_id")

    if not user_id:
        return jsonify({"success": False, "error": "User ID is required"})
        
    try:
        from database.db_functions import delete_habit
        result = delete_habit(int(user_id), int(habit_id))

        if result:
            return jsonify({"success": True})
        else:
            return jsonify({"success": False, "error": "Habit not found"})
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})



# --------------------------------------
# Run the app
# --------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
















'''
previous test
def show_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, username, email, failed_attempts FROM users")
    users = cursor.fetchall()

    print("\n--- USERS IN DATABASE ---")
    for user in users:
        print(dict(user))
    print("-------------------------\n")

    conn.close()


def delete_user():
    email = input("Enter email of user to delete: ")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE email = ?", (email,))
    conn.commit()
    conn.close()

    print("User deleted if existed.\n")


def register():
    username = input("Username: ")
    email = input("Email: ")
    password = input("Password: ")

    result = register_user({
        "username": username,
        "email": email,
        "password": password
    })

    print(result)


def login():
    email = input("Email: ")
    password = input("Password: ")

    result = login_user({
        "email": email,
        "password": password
    })

    print(result)


def menu():

    while True:
        print("\n===== HABIT TRACKER AUTH TEST =====")
        print("1 Register User")
        print("2 Login User")
        print("3 Show Users")
        print("4 Delete User")
        print("5 Exit")

        choice = input("Select option: ")

        if choice == "1":
            register()

        elif choice == "2":
            login()

        elif choice == "3":
            show_users()

        elif choice == "4":
            delete_user()

        elif choice == "5":
            break

        else:
            print("Invalid option")


if __name__ == "__main__":
    menu() '''
