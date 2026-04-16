/**
 * =============================================================
 * SPRINT 1 - FRONTEND UNIT TESTS: Login (US2)
 * =============================================================
 * Tests for: validateLoginForm() in login.js
 * Written by: Areebah
 *
 * Linked Acceptance Criteria:
 *   - Test 2.1  : Login page renders correctly
 *   - Test 2.2a : Empty fields trigger error messages
 *   - Test 2.2b : Incorrect credentials trigger error message
 *   - Test 2.3  : Too many failed attempts trigger warning
 *   - Test 2.4  : Valid credentials redirect to homepage
 *
 * Run with:
 *   cd C:\Users\areeb\Downloads\team13
 *   npx jest tests/sprint1/test_login_frontend.test.js
 * =============================================================
 */
 
/**
 * We copy the core validation logic from login.js here
 * because login.js is written for the browser (uses document.getElementById).
 * These pure logic functions can be tested without a browser.
 */
 
// --- Copied validation logic from login.js (Areebah) ---
 
function validateLoginForm(email, username, password) {
  const errors = {};
 
  if (!email) errors.email = 'Email is required';
  if (!username) errors.username = 'Username is required';
  if (!password) errors.password = 'Password is required';
 
  return {
    isValid: Object.keys(errors).length === 0,
    errors
  };
}
 
function handleLoginResponse(data) {
  if (data.success) {
    return { action: 'redirect', destination: 'home.html' };
  }
 
  const err = data.error.toLowerCase();
  if (err.includes('locked') || err.includes('too many')) {
    return { action: 'show_attempts_warning' };
  }
 
  return { action: 'show_error', field: 'password', message: data.error };
}
 
// --- Tests ---
 
// =============================================================
// Test 2.2a - Empty fields trigger error messages
// =============================================================
 
describe('Test 2.2a - Empty fields trigger error messages', () => {
 
  test('Empty email triggers error', () => {
    const result = validateLoginForm('', 'areebah', 'Test@1234');
    expect(result.isValid).toBe(false);
    expect(result.errors.email).toBe('Email is required');
  });
 
  test('Empty username triggers error', () => {
    const result = validateLoginForm('test@test.com', '', 'Test@1234');
    expect(result.isValid).toBe(false);
    expect(result.errors.username).toBe('Username is required');
  });
 
  test('Empty password triggers error', () => {
    const result = validateLoginForm('test@test.com', 'areebah', '');
    expect(result.isValid).toBe(false);
    expect(result.errors.password).toBe('Password is required');
  });
 
  test('All fields empty triggers all three errors', () => {
    const result = validateLoginForm('', '', '');
    expect(result.isValid).toBe(false);
    expect(result.errors.email).toBeDefined();
    expect(result.errors.username).toBeDefined();
    expect(result.errors.password).toBeDefined();
  });
 
});
 
// =============================================================
// Test 2.2b - Incorrect credentials trigger error message
// =============================================================
 
describe('Test 2.2b - Incorrect credentials trigger error under password field', () => {
 
  test('Backend invalid credentials shows error under password field', () => {
    const response = handleLoginResponse({ success: false, error: 'Invalid credentials' });
    expect(response.action).toBe('show_error');
    expect(response.field).toBe('password');
  });
 
});
 
// =============================================================
// Test 2.3 - Too many failed attempts trigger warning
// =============================================================
 
describe('Test 2.3 - Too many failed attempts shows warning banner', () => {
 
  test('Locked account error shows attempts warning', () => {
    const response = handleLoginResponse({ success: false, error: 'Account locked due to too many failed attempts' });
    expect(response.action).toBe('show_attempts_warning');
  });
 
  test('"too many" in error message shows attempts warning', () => {
    const response = handleLoginResponse({ success: false, error: 'Too many failed attempts' });
    expect(response.action).toBe('show_attempts_warning');
  });
 
});
 
// =============================================================
// Test 2.4 - Valid credentials redirect to homepage
// =============================================================
 
describe('Test 2.4 - Valid credentials redirect to home page', () => {
 
  test('Successful login triggers redirect to home.html', () => {
    const response = handleLoginResponse({ success: true, user_id: 1 });
    expect(response.action).toBe('redirect');
    expect(response.destination).toBe('home.html');
  });
 
});
 
// =============================================================
// Test 2.1 - Valid form passes frontend validation
// =============================================================
 
describe('Test 2.1 - Valid login form passes frontend validation', () => {
 
  test('All fields filled returns isValid true', () => {
    const result = validateLoginForm('test@test.com', 'areebah', 'Test@1234');
    expect(result.isValid).toBe(true);
    expect(Object.keys(result.errors).length).toBe(0);
  });
 
});