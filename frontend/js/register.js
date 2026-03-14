
// Bit by Bit - Register Page JavaScript
// Sprint 1: Registration UI Logic
// frontend by Areebah
// Calls backend functions written by ....



// Show error helper function
// function shows an error message below a field and turns the field border red
function showFieldError(fieldId, errorId, message) {
  const field = document.getElementById(fieldId);
  const error = document.getElementById(errorId);
  field.classList.add('error');
  error.textContent = message;
  error.classList.add('visible');
}


// clear error helper function
// function hides the error message and removes the red border from a field
function clearFieldError(fieldId, errorId) {
  const field = document.getElementById(fieldId);
  const error = document.getElementById(errorId);
  field.classList.remove('error');
  error.classList.remove('visible');
}


// show register errors function
// Called by backend to display
// any server-side errors to the user
function showRegisterErrors(errors) {
  // If email error exists, show it
  if (errors.email) {
    showFieldError('emailField', 'emailError', errors.email);
  }
  // If username error exists, show it
  if (errors.username) {
    showFieldError('usernameField', 'usernameError', errors.username);
  }
  // If password error exists, show it
  if (errors.password) {
    showFieldError('passwordField', 'passwordError', errors.password);
  }
}


// validate form (Frontend checks) 
// Checks all fields before sending to backend
// Returns true if valid, false if not
function validateRegisterForm(email, username, password, confirmPassword) {
  
  // Track if form is valid
  let isValid = true;

  // Clear all previous errors first
  clearFieldError('emailField', 'emailError');
  clearFieldError('usernameField', 'usernameError');
  clearFieldError('passwordField', 'passwordError');
  clearFieldError('confirmPasswordField', 'confirmPasswordError');

  // Check email is not empty
  if (!email) {
    showFieldError('emailField', 'emailError', 'Email is required');
    isValid = false;
  }

  // Check username is not empty
  if (!username) {
    showFieldError('usernameField', 'usernameError', 'Username is required');
    isValid = false;
  }

  // Check password is not empty
  if (!password) {
    showFieldError('passwordField', 'passwordError', 'Password is required');
    isValid = false;
  }
  //Hamza Auth.py added
  if (password) {
    const hasUpperCase = /[A-Z]/.test(password);
    const hasLowerCase = /[a-z]/.test(password);
    const hasNumber = /\d/.test(password);
    const hasSpecial = /[!@#$%^&*(),.?":{}|<>]/.test(password);

    if (password.length < 8 || !hasUpperCase || !hasLowerCase || !hasNumber || !hasSpecial) {
      showFieldError(
        'passwordField',
        'passwordError',
        'Password must be at least 8 characters and include uppercase, lowercase, number, and special character'
      );
      isValid = false;
    }
    
  }

  // Check passwords match
  if (password !== confirmPassword) {
    showFieldError(
      'confirmPasswordField', 
      'confirmPasswordError', 
      'Passwords do not match'
    );
    isValid = false;
  }

  return isValid;
}


// main register function
// the entry point called when user clicks the "Create Account" button
function handelRegisterSubmit() {
  // 1. Get values from input fields
  const email = document.getElementById('email').value.trim();
  const username = document.getElementById('username').value.trim();
  const password = document.getElementById('password').value;
  const confirmPassword = document.getElementById('confirmPassword').value;

  // 2. Frontend validation
  if (!validateRegisterForm(email, username, password, confirmPassword)) return;

  // 3. Create object to send to backend
  const userData = { email, username, password };

  // 4. Call Flask backend
  fetch('http://127.0.0.1:5000/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(userData)
  })
  .then(res => res.json())
  .then(result => {
    if (result.success) {
      // 5a. Success → redirect to login page
      alert('Account created successfully!');
      window.location.href = 'login.html';
    } else {
      // 5b. Failure → show error under the correct field only
      // Backend sends one error string e.g. "Username already taken"
      // so we check the message and route it to the right field
      const err = result.error.toLowerCase();
      if (err.includes('email')) {
        showFieldError('emailField', 'emailError', result.error);
      } else if (err.includes('username')) {
        showFieldError('usernameField', 'usernameError', result.error);
      } else if (err.includes('password')) {
        showFieldError('passwordField', 'passwordError', result.error);
      } else {
        // fallback for any other error
        showFieldError('emailField', 'emailError', result.error);
      }
    }
  })
  .catch(err => console.error('Register fetch error:', err));
}
