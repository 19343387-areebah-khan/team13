# from flask import Flask, jsonify
# from flask import render_template

# app = Flask(__name__)

# habits = [
#     {"id": 1, "name": "habit 1"},
#     {"id": 2, "name": "habit 2"},
#     {"id": 3, "name": "habit 3"}
# ]

# @app.route("/")
# def home():
#     return render_template("index.html")

# @app.route("/habits", methods=["GET"])
# def get_habits():
#     return jsonify(habits)

# @app.route("/habits/<int:habit_id>", methods=["DELETE"])
# def delete_habit(habit_id):
#     global habits

#     for habit in habits:
#         if habit["id"] == habit_id:
#             habits.remove(habit)
#             return jsonify({"success": True})
        
#     return jsonify({"error": "Habit not found"}), 404

# if __name__ == "__main__":
#     app.run(debug=True)
from flask import Flask, jsonify, request, render_template
from database.db_functions import get_habits_by_user_id, add_habit, delete_habit, update_user

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/habits", methods=["GET", "POST"])
def habits_route():
    user_id = int(request.args.get('user_id') or request.json.get('user_id'))
    
    if request.method == "GET":
        habits = get_habits_by_user_id(user_id)
        return jsonify({"success": True, "habits": habits})

    if request.method == "POST":
        data = request.json
        name = data.get("name")
        habit_type = data.get("habit_type", "other")
        habit_id = add_habit(user_id, name, habit_type)
        return jsonify({"success": True, "habit_id": habit_id})

@app.route("/habits/<int:habit_id>", methods=["DELETE"])
def api_delete_habit(habit_id):
    success = delete_habit(habit_id)
    if success:
        return jsonify({"success": True})
    else:
        return jsonify({"error": "Habit not found"}), 404
    
@app.route("/update-profile", methods=["POST"])
def update_profile():
    data = request.json

    user_id = data.get("user_id")
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not user_id:
        return jsonify({"success": False, "error": "User ID is required"}), 400

    result = update_user(user_id, username=username, email=email, password=password)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)