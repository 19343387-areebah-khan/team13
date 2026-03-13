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



