
// // Sprint 2: T6.4 areebha
// // These fetch() functions connect the frontend to the Flask habit endpoints
// // will be used by home.js once Hamza builds the frontend UI
// // Stipan replaces the localStorage code with these calls


// // CREATE A NEW HABIT
// // called when user submits the habit creation form
// // sends habit data to POST /habits and returns the result
// function createHabit(name, habitType) {



// Sprint 2: T6.4 areebha
// These functions connect the frontend to the Flask habit endpoints
// All habit data is stored in the backend, not localStorage

const USER_ID = localStorage.getItem('user_id');

// CREATE
async function createHabit(name, habitType) {
    const res = await fetch('http://127.0.0.1:5000/habits', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: USER_ID, name, habit_type: habitType })
    });
    return res.json();
}

// READ / LOAD
async function loadHabits() {
    const res = await fetch(`http://127.0.0.1:5000/habits?user_id=${USER_ID}`);
    return res.json();
}

// RENDER
async function renderHabits() {
    const data = await loadHabits();
    const list = document.getElementById('habit-list');
    list.innerHTML = '';

    if (!data.success || data.habits.length === 0) {
        list.innerHTML = '<p>No habits yet.</p>';
        return;
    }

    data.habits.forEach(habit => {
        const item = document.createElement('div');
        item.className = 'habit-item';
        item.id = `habit-${habit.habit_id}`;

        item.innerHTML = `
            <span>${habit.name} (${habit.habit_type})</span>
            <button onclick="deleteHabit(${habit.habit_id})">Delete</button>
        `;
        list.appendChild(item);
    });
}

// DELETE
async function deleteHabit(habit_id) {
    if (!confirm('Are you sure?')) return;

    const res = await fetch(`http://127.0.0.1:5000/habits/${habit_id}`, { method: 'DELETE' });
    const data = await res.json();

    if (data.success) renderHabits();
    else alert(data.error || 'Failed to delete habit');
}

// INIT
document.addEventListener("DOMContentLoaded", () => {
    renderHabits();

    const habitForm = document.getElementById('habit-form');
    habitForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const name = document.getElementById('habit-name').value.trim();
        const type = document.getElementById('habit-type').value;
        if (!name) return;

        const result = await createHabit(name, type);
        if (result.success) {
            document.getElementById('habit-name').value = '';
            document.getElementById('toast').textContent = "Habit added successfully";
            renderHabits();
        } else {
            document.getElementById('toast').textContent = result.error || "Failed to add habit";
        }
    });
});



//   // get the logged-in user's ID from localStorage (saved during login)
//   const userId = localStorage.getItem('user_id');

//   // if no user is logged in, stop
//   if (!userId) {
//     console.error('No user logged in');
//     return;
//   }

//   // send the habit data to the backend
//   return fetch('http://127.0.0.1:5000/habits', {
//     method: 'POST',
//     headers: { 'Content-Type': 'application/json' },
//     body: JSON.stringify({
//       user_id: userId,
//       name: name,
//       habit_type: habitType
//     })
//   })
//   .then(res => res.json())
//   .then(result => {
//     if (result.success) {
//       console.log('Habit created with ID:', result.habit_id);
//     } else {
//       console.error('Failed to create habit:', result.error);
//     }
//     return result;
//   })
//   .catch(err => {
//     console.error('Error connecting to backend:', err);
//   });
// }


// // LOAD ALL HABITS FOR THE CURRENT USER
// // called when the home page loads to display the user's habit list
// // fetches habits from GET /habits?user_id=X
// function loadHabits() {

//   // get the logged-in user's ID from localStorage
//   const userId = localStorage.getItem('user_id');

//   // if no user is logged in, stop
//   if (!userId) {
//     console.error('No user logged in');
//     return;
//   }

//   // fetch the user's habits from the backend
//   return fetch('http://127.0.0.1:5000/habits?user_id=' + userId)
//   .then(res => res.json())
//   .then(result => {
//     if (result.success) {
//       console.log('Loaded habits:', result.habits);
//     } else {
//       console.error('Failed to load habits:', result.error);
//     }
//     return result;
//   })
//   .catch(err => {
//     console.error('Error connecting to backend:', err);
//   });
// }


// //new 

// async function renderHabits() {
//     const result = await loadHabits();
//     const list = document.getElementById("habit-list");
//     list.innerHTML = "";

//     if (!result.success || !result.habits.length) {
//         list.innerHTML = "<p>No habits yet.</p>";
//         return;
//     }

//     result.habits.forEach(habit => {
//         const item = document.createElement("div");
//         item.className = "habit-item";
//         item.id = `habit-${habit.id}`;

//         item.innerHTML = `
//             <span>${habit.name}</span>
//             <button onclick="deleteHabit(${habit.id})">Delete</button>
//         `;
//         list.appendChild(item);
//     });
// }

// // Override deleteHabit to include confirmation and rerender
// function deleteHabit(id) {
//     if (!confirm("Are you sure?")) return;

//     fetch("/habits/" + id, { method: "DELETE" })
//     .then(res => res.json())
//     .then(data => {
//         if (data.success) {
//             renderHabits(); // re-render after deletion
//         } else {
//             alert(data.error || "Failed to delete habit");
//         }
//     });
// }