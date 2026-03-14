const habitList = document.getElementById("habit-list");
const emptyMessage = document.getElementById("empty-message");
const addHabitButton = document.getElementById("add-habit");

function getCurrentUser() {
    const savedUser = localStorage.getItem("currentUser");

    if (!savedUser) {
        return "defaultUser";
    }

    return savedUser;
}

function getHabitsKey() {
    const currentUser = getCurrentUser();
    return "habits_" + currentUser;
}

function getHabits() {
    const savedHabits = localStorage.getItem(getHabitsKey());

    if (!savedHabits) {
        return [];
    }

    return JSON.parse(savedHabits);
}

function saveHabits(habits) {
    localStorage.setItem(getHabitsKey(), JSON.stringify(habits));
}

function renderHabits() {
    const habits = getHabits();

    habitList.innerHTML = "";

    if (habits.length === 0) {
        emptyMessage.style.display = "block";
        return;
    }

    emptyMessage.style.display = "none";

    habits.forEach(function(habit) {
        const listItem = document.createElement("li");
        listItem.textContent = habit;
        habitList.appendChild(listItem);
    });
}

addHabitButton.addEventListener("click", function() {
    const newHabit = prompt("Enter a new habit:");

    if (!newHabit) {
        return;
    }

    const habits = getHabits();
    habits.push(newHabit);
    saveHabits(habits);
    renderHabits();
});

renderHabits();
