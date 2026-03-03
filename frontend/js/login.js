
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

  // Get values from all input fields
  const email = document.getElementById('email').value.trim();
  const username = document.getElementById('username').value.trim();
  const password = document.getElementById('password').value;

  // Run frontend validation first
  const isValid = validateLoginForm(email, username, password);

  // If frontend validation fails, stop here
  if (!isValid) return;

  // if valid, send to backend 
  // NOTE: loginUser() is Hamza's backend function
  // pass the data as an object
  const loginData = {
    email: email,
    username: username,
    password: password
  };

  // TODO: Connect to Hamza's loginUser(loginData) function
  // For now we log to confirm frontend is working
  console.log('Login data ready to send:', loginData);

  // Temporary success redirect until backend is connected
  // replace with Hamza's loginUser() response
  alert('Login successful! Redirecting to home...');
  window.location.href = 'register.html';
}