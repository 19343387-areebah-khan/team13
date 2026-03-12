from services.auth_service import register_user, login_user



##def handle_register_submit():
##def handle_login_submit():
##def showLoginErrors(errors)
##def showRegisterErrors(errors)
from services.auth_service import register_user, login_user
from database.db_functions import get_user_by_email, get_user_by_username, update_failed_attempts, reset_failed_attempts
from database.db_connections import get_connection


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
    menu()

'''
# --- Test Registration ---
data = {
    "username": "TestUser",
    "email": "testuser@example.com",
    "password": "Password123!"
}

result = register_user(data)
print("Register Result:", result)

# --- Test Login ---
login_data = {
    "email": "testuser@example.com",
    "password": "Password123!"
}

login_result = login_user(login_data)
print("Login Result:", login_result)

# --- Test Wrong Password ---
wrong_login = {
    "email": "testuser@example.com",
    "password": "WrongPass1!"
}

wrong_result = login_user(wrong_login)
print("Wrong Login Result:", wrong_result)


'''







'''


##-----------------------------------------
# Example usage
def handle_register_submit():
    data = {
        'username': input("Username: "),
        'email': input("Email: "),
        'password': input("Password: ")
    }
    success, message = register_user(data)
    print(message)

def handle_login_submit():
    data = {
        'email': input("Email: "),
        'password': input("Password: ")
    }
    success, message = login_user(data)
    print(message)

if __name__ == "__main__":
    while True:
        choice = input("1=Register, 2=Login, 0=Exit: ")
        if choice == "1":
            handle_register_submit()
        elif choice == "2":
            handle_login_submit()
        else:
            break
'''






