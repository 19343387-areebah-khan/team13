from flask import Flask

app = Flask(__name__)

users = []  #This is to store the users, so we can search later 

#input sanitisation
def sanitizeInput(input):
    #This is one way to sanitise the input. It will remove all leading or trailing spaces if the input is a string
    if isinstance(input, str):
        return input.strip()
    return input


#validation
def validateUsername(username):
    #check username length
    if len(username) < 2 or len(username) > 20:
        return False
    #ensure username has only letters and numbers
    if not username.isalnum():
        return False
    return True

def validateEmail(email):

    return 0

def validatePassword(password):
    #ensure password meets minimun length, dont have any specific other requirements at the moment
    if len(password) < 6:
        return False
    return True

#account availability
def isUsernameTaken(username):
    #searches if the username has already exists
    for user in users:
        if user["username"] == username:
            return True
    return False

def isEmailTaken(email):
    #searches if the email is already in use
    for user in users:
        if user["email"] == email:
            return True
    return False

#authentication
def registerUser(data):
    #sanitis user input
    username = sanitizeInput("username")
    email = sanitizeInput("email")
    password = sanitizeInput("password")
    
    #validate username, email, password
    if not validateUsername(username):
        return {"error": "invalid username"}
    
    if not validateEmail(username):
        return {"error": "invalid email"}
    
    if not validatePassword(password):
        return {"error": "invalid password"}
    
    #check if username and email already exist
    if isUsernameTaken(username):
        return {"error": "username taken"}
    
    if isEmailTaken(username):
        return {"error": "email taken"}
    
    #add new user to memory
    users.append({"username": username, "email": email, "password": password})

    return {"success": True}

def loginUser(data):
    #sanitise login input
    email = sanitizeInput("email")
    password = sanitizeInput("password")

    #check credentials against all stored in users
    for user in users:
        if user["email"] == email and user["password"] == password:
            return {"success": True}
        
    return {"error": "invalid credentials"}

if __name__ == "__main__":
    app.run(debug=True)



