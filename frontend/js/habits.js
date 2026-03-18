
// Sprint 2: T6.4 areebha
// These fetch() functions connect the frontend to the Flask habit endpoints
// will be used by home.js once Hamza builds the frontend UI
// Stipan replaces the localStorage code with these calls


// CREATE A NEW HABIT
// called when user submits the habit creation form
// sends habit data to POST /habits and returns the result
function createHabit(name, habitType) {

  // get the logged-in user's ID from localStorage (saved during login)
  const userId = localStorage.getItem('user_id');

  // if no user is logged in, stop
  if (!userId) {
    console.error('No user logged in');
    return;
  }

  // send the habit data to the backend
  return fetch('http://127.0.0.1:5000/habits', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      user_id: userId,
      name: name,
      habit_type: habitType
    })
  })
  .then(res => res.json())
  .then(result => {
    if (result.success) {
      console.log('Habit created with ID:', result.habit_id);
    } else {
      console.error('Failed to create habit:', result.error);
    }
    return result;
  })
  .catch(err => {
    console.error('Error connecting to backend:', err);
  });
}


// LOAD ALL HABITS FOR THE CURRENT USER
// called when the home page loads to display the user's habit list
// fetches habits from GET /habits?user_id=X
function loadHabits() {

  // get the logged-in user's ID from localStorage
  const userId = localStorage.getItem('user_id');

  // if no user is logged in, stop
  if (!userId) {
    console.error('No user logged in');
    return;
  }

  // fetch the user's habits from the backend
  return fetch('http://127.0.0.1:5000/habits?user_id=' + userId)
  .then(res => res.json())
  .then(result => {
    if (result.success) {
      console.log('Loaded habits:', result.habits);
    } else {
      console.error('Failed to load habits:', result.error);
    }
    return result;
  })
  .catch(err => {
    console.error('Error connecting to backend:', err);
  });
}
