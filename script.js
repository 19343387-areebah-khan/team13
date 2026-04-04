function deleteHabit(id) {
    fetch("/habits/" + id, {
        method: "DELETE"
    })
    .then(function(response) {
        return response.json();
    })
    .then(function(data) {
        console.log("Habit deleted");
        loadHabits();
    });
}

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