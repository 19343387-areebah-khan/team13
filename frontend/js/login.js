
// BIT BY BIT - Login Page JavaScript
// Sprint 1: Login UI Logic
// Frontend function written by Areebah (handleLoginSubmit, showLoginErrors)
// Calls backend functions written by Hamza 



// show error helper function
// Shows error message below a field
// and turns the field border red
function showFieldError(fieldId, errorId, message) {
  const field = document.getElementById(fieldId);
  const error = document.getElementById(errorId);
  field.classList.add('error');
  error.textContent = message;
  error.classList.add('visible');
}


// clear error helper function
// Hides error message and removes red border from a field
function clearFieldError(fieldId, errorId) {
  const field = document.getElementById(fieldId);
  const error = document.getElementById(errorId);
  field.classList.remove('error');
  error.classList.remove('visible');
}


// Show login errors function
// Called by backend (Hamza) to display
// any server-side errors to the user
function showLoginErrors(errors) {
  // If email error exists, show it
  if (errors.email) {
    showFieldError('emailField', 'emailError', errors.email);
  }
  // If username error exists, show it
  if (errors.username) {
    showFieldError(
      'usernameField', 
      'usernameError', 
      errors.username
    );
  }
  // If password error exists, show it
  if (errors.password) {
    showFieldError(
      'passwordField', 
      'passwordError', 
      errors.password
    );
  }
  // If too many failed attempts, show warning
  if (errors.attempts) {
    const warning = document.getElementById('attemptsWarning');
    warning.classList.add('visible');
  }
}


// validate form (Frontend checks) 
// Checks all fields before sending to backend
// Returns true if valid, false if not
function validateLoginForm(email, username, password) {

  // Track if form is valid
  let isValid = true;

  // Clear all previous errors first
  clearFieldError('emailField', 'emailError');
  clearFieldError('usernameField', 'usernameError');
  clearFieldError('passwordField', 'passwordError');

  // Hide attempts warning
  const warning = document.getElementById('attemptsWarning');
  warning.classList.remove('visible');

  // Check email is not empty
  if (!email) {
    showFieldError(
      'emailField', 
      'emailError', 
      'Email is required'
    );
    isValid = false;
  }

  // Check username is not empty
  if (!username) {
    showFieldError(
      'usernameField', 
      'usernameError', 
      'Username is required'
    );
    isValid = false;
  }

  // check password is not empty
  if (!password) {
    showFieldError(
      'passwordField', 
      'passwordError', 
      'Password is required'
    );
    isValid = false;
  }

  return isValid;
}


// MAIN LOGIN FUNCTION
// Entry point called when user clicks the login button
function handleLoginSubmit() {

  // 1. Get values from input fields
  const email = document.getElementById('email').value.trim();
  const username = document.getElementById('username').value.trim();
  const password = document.getElementById('password').value;

  // 2. Run frontend validation
  const isValid = validateLoginForm(email, username, password);
  if (!isValid) return; // stop if invalid

  // 3. Create object to send to backend
  const loginData = { email, username, password };

  // 4. Call Flask backend
  fetch('http://localhost:5000/login', {  // make sure Flask has @app.route("/login")
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(loginData)
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      // 5a. Success → save user session and go to home page
      localStorage.setItem('user_id', data.user_id);
      window.location.href = 'home.html';
    } else {
      // 5b. Failure → show error under the correct place
      // Backend returns "Invalid credentials" or "Account locked..."
      const err = data.error.toLowerCase();
      if (err.includes('locked') || err.includes('too many')) {
        // show the attempts warning banner
        showLoginErrors({ attempts: true });
      } else {
        // "Invalid credentials" — show under password field
        // backend doesn't say which field was wrong for security
        showFieldError('passwordField', 'passwordError', data.error);
      }
    }
  })
  .catch(error => console.error('Error connecting to backend:', error));
}

