from flask import Flask, jsonify
from flask import render_template

app = Flask(__name__)

habits = [
    {"id": 1, "name": "habit 1"},
    {"id": 2, "name": "habit 2"},
    {"id": 3, "name": "habit 3"}
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/habits", methods=["GET"])
def get_habits():
    return jsonify(habits)

@app.route("/habits/<int:habit_id>", methods=["DELETE"])
def delete_habit(habit_id):
    global habits

    for habit in habits:
        if habit["id"] == habit_id:
            habits.remove(habit)
            return jsonify({"success": True})
        
    return jsonify({"error": "Habit not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
