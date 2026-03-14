const habitList = document.getElementById("habit-list");
const emptyMessage = document.getElementById("empty-message");
const addHabitButton = document.getElementById("add-habit");

function getHabits() {

    const savedHabits = localStorage.getItem("habits");

    if (!savedHabits) {
        return [];
    }

    return JSON.parse(savedHabits);
}

function renderHabits() {

    const habits =getHabits();

    habitList.innerHTML = "";

    if(habits.length === 0) {
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

   localStorage.setItem("habits", JSON.stringify(habits));

   renderHabits();

});

renderHabits();
