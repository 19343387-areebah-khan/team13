from flask import Flask, request, jsonify, send_from_directory
from database.db_functions import add_habit, get_habits_by_user_id, log_habit_completion

app = Flask(__name__, static_folder="frontend", static_url_path="")

#home page

@app.route('/home')
def home():
    return send_from_directory("frontend", "home.html")

@app.route('/habits', methods=['GET'])
def habits_get():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"success": False, "error": "User ID is required"}), 400
    if not str(user_id).isdigit():
        return jsonify({"success": False, "error": "User ID must be an integer"}), 400

    habits = get_habits_by_user_id(user_id)
    return jsonify({"success": True, "habits": habits})

# create a habit
@app.route('/habits', methods=['POST'])
def habits_post():
    data = request.get_json()

    if not data:
        return jsonify({"success": False, "error": "No data provided"}), 400
    
    user_id = data.get("user_id")
    name = data.get("name", "").strip()
    habit_type = data.get("habit_type", "").strip()

    if not user_id:
        return jsonify({"success": False, "error": "User ID is required"}), 400
    if not str(user_id).isdigit():
        return jsonify({"success": False, "error": "User ID must be an integer"}), 400
    if not name:
        return jsonify({"success": False, "error": "Habit name is required"}), 400
    if not habit_type:
        return jsonify({"success": False, "error": "Habit type is required"}), 400

    result = add_habit(user_id, name, habit_type)
    if result["success"]:
        return jsonify({"success": True,
                        "message": "Habit added successfully",
                        "habit_id": result.get("habit_id")}), 201
    else:
        return jsonify({"success": False, "error": result.get("error", "Unknown error")}), 500
    
# log habit completion
@app.route('/habits/complete', methods=['POST'])
def complete_habit():
    data = request.get_json()

    if not data:
        return jsonify({"success": False, "error": "No data provided"}), 400
    user_id = data.get("user_id")
    habit_id = data.get("habit_id")
    completed = data.get("completed")
    if not user_id:
        return jsonify({"success": False, "error": "User ID is required"}), 400
    if not str(user_id).isdigit():
        return jsonify({"success": False, "error": "User ID must be an integer"}), 400
    if not habit_id:
        return jsonify({"success": False, "error": "Habit ID is required"}), 400
    if not str(habit_id).isdigit():
        return jsonify({"success": False, "error": "Habit ID must be an integer"}), 400
    
    if completed is None:
        return jsonify({"success": False, "error": "Completed status is required"}), 400
    
    result = log_habit_completion(int(habit_id), int(user_id), completed)
    if result["success"]:
        return jsonify({"success": True, "message": "Habit completion logged successfully"})
    else:
        return jsonify({"success": False, "error": result.get("error", "Unknown error")}), 500
    
if __name__ == '__main__':
    app.run(debug=True)    