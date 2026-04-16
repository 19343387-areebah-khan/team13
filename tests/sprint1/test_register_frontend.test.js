/**
 * =============================================================
 * SPRINT 1 - FRONTEND UNIT TESTS: Registration (US1)
 * =============================================================
 * Tests for: validateRegisterForm() in register.js
 * Written by: Areebah
 *
 * Linked Acceptance Criteria:
 *   - Test 1.1  : Registration page renders correctly
 *   - Test 1.2  : Empty or invalid inputs trigger error messages
 *   - Test 1.2b : Mismatched passwords trigger error
 *   - Test 1.3  : Valid registration redirects to login
 *
 * Run with:
 *   cd C:\Users\areeb\Downloads\team13
 *   npx jest tests/sprint1/test_register_frontend.test.js
 * =============================================================
 */
 
/**
 * We copy the core validation logic from register.js here
 * because register.js is written for the browser (uses document.getElementById).
 * These pure logic functions can be tested without a browser.
 */
 
// --- Copied validation logic from register.js (Areebah) ---
 
function validateRegisterForm(email, username, password, confirmPassword) {
  const errors = {};
 
  if (!email) errors.email = 'Email is required';
  if (!username) errors.username = 'Username is required';
  if (!password) errors.password = 'Password is required';
 
  if (password) {
    const hasUpperCase = /[A-Z]/.test(password);
    const hasLowerCase = /[a-z]/.test(password);
    const hasNumber = /\d/.test(password);
    const hasSpecial = /[!@#$%^&*(),.?":{}|<>]/.test(password);
 
    if (password.length < 8 || !hasUpperCase || !hasLowerCase || !hasNumber || !hasSpecial) {
      errors.password = 'Password must be at least 8 characters and include uppercase, lowercase, number, and special character';
    }
  }
 
  if (password && confirmPassword && password !== confirmPassword) {
    errors.confirmPassword = 'Passwords do not match';
  }
 
  return {
    isValid: Object.keys(errors).length === 0,
    errors
  };
}
 
// --- Tests ---
 
// =============================================================
// Test 1.2 - Empty fields trigger error messages
// =============================================================
 
describe('Test 1.2 - Empty or invalid inputs trigger errors', () => {
 
  test('Empty email triggers error', () => {
    const result = validateRegisterForm('', 'areebah', 'Test@1234', 'Test@1234');
    expect(result.isValid).toBe(false);
    expect(result.errors.email).toBe('Email is required');
  });
 
  test('Empty username triggers error', () => {
    const result = validateRegisterForm('test@test.com', '', 'Test@1234', 'Test@1234');
    expect(result.isValid).toBe(false);
    expect(result.errors.username).toBe('Username is required');
  });
 
  test('Empty password triggers error', () => {
    const result = validateRegisterForm('test@test.com', 'areebah', '', '');
    expect(result.isValid).toBe(false);
    expect(result.errors.password).toBe('Password is required');
  });
 
  test('All fields empty triggers multiple errors', () => {
    const result = validateRegisterForm('', '', '', '');
    expect(result.isValid).toBe(false);
    expect(result.errors.email).toBeDefined();
    expect(result.errors.username).toBeDefined();
    expect(result.errors.password).toBeDefined();
  });
 
  test('Weak password (no uppercase) triggers error', () => {
    const result = validateRegisterForm('test@test.com', 'areebah', 'test@1234', 'test@1234');
    expect(result.isValid).toBe(false);
    expect(result.errors.password).toContain('uppercase');
  });
 
  test('Weak password (too short) triggers error', () => {
    const result = validateRegisterForm('test@test.com', 'areebah', 'Ab1!', 'Ab1!');
    expect(result.isValid).toBe(false);
    expect(result.errors.password).toContain('8 characters');
  });
 
  test('Weak password (no special character) triggers error', () => {
    const result = validateRegisterForm('test@test.com', 'areebah', 'Test1234', 'Test1234');
    expect(result.isValid).toBe(false);
    expect(result.errors.password).toBeDefined();
  });
 
});
 
// =============================================================
// Test 1.2b - Mismatched passwords trigger error
// =============================================================
 
describe('Test 1.2b - Mismatched passwords trigger error', () => {
 
  test('Different passwords trigger confirm password error', () => {
    const result = validateRegisterForm('test@test.com', 'areebah', 'Test@1234', 'Test@5678');
    expect(result.isValid).toBe(false);
    expect(result.errors.confirmPassword).toBe('Passwords do not match');
  });
 
  test('Matching passwords do not trigger confirm password error', () => {
    const result = validateRegisterForm('test@test.com', 'areebah', 'Test@1234', 'Test@1234');
    expect(result.errors.confirmPassword).toBeUndefined();
  });
 
});
 
// =============================================================
// Test 1.3 - Valid registration form passes validation
// =============================================================
 
describe('Test 1.3 - Valid registration passes frontend validation', () => {
 
  test('All valid inputs return isValid true', () => {
    const result = validateRegisterForm('test1@test.com', 'test1', 'Leoisacutecat890!', 'Leoisacutecat890!');
    expect(result.isValid).toBe(true);
    expect(Object.keys(result.errors).length).toBe(0);
  });
 
});