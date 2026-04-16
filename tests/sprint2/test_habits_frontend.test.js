/**
 * =============================================================
 * SPRINT 2 - FRONTEND UNIT TESTS: Habit Creation & Completion
 * =============================================================
 * Tests for: habit creation form validation and completion toggle
 * Written by: Areebah (T6.4, T6.8, T10.1, T10.2, T10.5, T10.6)
 *
 * Linked Acceptance Criteria:
 *   - AC6.4  : Empty or invalid habit input triggers error
 *   - AC6.5  : Valid habit is saved via POST /habits
 *   - AC10.1 : Each habit displays a completion toggle
 *   - AC10.2 : Marking complete updates the UI
 *
 * Run with:
 *   cd C:\Users\areeb\Downloads\team13
 *   npx jest tests/sprint2/test_habits_frontend.test.js
 * =============================================================
 */
 
// =============================================================
// Habit creation form validation logic (from home.html - Areebah)
// =============================================================
 
function validateHabitForm(name, habitType) {
  const errors = {};
 
  if (!name || name.trim() === '') {
    errors.name = 'Habit name is required';
  }
 
  if (!habitType || habitType.trim() === '') {
    errors.habitType = 'Habit type is required';
  }
 
  return {
    isValid: Object.keys(errors).length === 0,
    errors
  };
}
 
// =============================================================
// Completion toggle display logic (from home.html - Areebah T10.5)
// =============================================================
 
function getTickDisplay(habit) {
  if (!habit.today_status || habit.today_status === null) {
    return { classes: 'habit-check', text: '', color: '' };
  }
  if (habit.today_status === 'good') {
    return { classes: 'habit-check done good', text: '✓', color: '#D97757' };
  }
  if (habit.today_status === 'partial') {
    return { classes: 'habit-check done partial', text: '~', color: '#D97757' };
  }
  if (habit.today_status === 'not_complete') {
    return { classes: 'habit-check done not-complete', text: '✗', color: '#D97757' };
  }
  if (habit.completed_today) {
    return { classes: 'habit-check done', text: '✓', color: '#D97757' };
  }
  return { classes: 'habit-check', text: '', color: '' };
}
 
// =============================================================
// Tests
// =============================================================
 
// AC6.4 - Empty or invalid habit input triggers error
describe('AC6.4 - Empty or invalid habit input triggers error', () => {
 
  test('Empty habit name triggers error', () => {
    const result = validateHabitForm('', 'health');
    expect(result.isValid).toBe(false);
    expect(result.errors.name).toBe('Habit name is required');
  });
 
  test('Whitespace-only habit name triggers error', () => {
    const result = validateHabitForm('   ', 'health');
    expect(result.isValid).toBe(false);
    expect(result.errors.name).toBeDefined();
  });
 
  test('Empty habit type triggers error', () => {
    const result = validateHabitForm('Exercise', '');
    expect(result.isValid).toBe(false);
    expect(result.errors.habitType).toBe('Habit type is required');
  });
 
  test('Both fields empty triggers two errors', () => {
    const result = validateHabitForm('', '');
    expect(result.isValid).toBe(false);
    expect(result.errors.name).toBeDefined();
    expect(result.errors.habitType).toBeDefined();
  });
 
});
 
// AC6.5 - Valid habit input passes validation
describe('AC6.5 - Valid habit input passes frontend validation', () => {
 
  test('Valid name and type passes validation', () => {
    const result = validateHabitForm('Exercise', 'health');
    expect(result.isValid).toBe(true);
    expect(Object.keys(result.errors).length).toBe(0);
  });
 
});
 
// AC10.1 & AC10.2 - Completion toggle display
describe('AC10.1 & AC10.2 - Completion toggle displays correctly', () => {
 
  test('Habit with no status shows empty toggle', () => {
    const display = getTickDisplay({ today_status: null, completed_today: 0 });
    expect(display.classes).toBe('habit-check');
    expect(display.text).toBe('');
  });
 
  test('Habit with good status shows done class and tick', () => {
    const display = getTickDisplay({ today_status: 'good', completed_today: 1 });
    expect(display.classes).toContain('done');
    expect(display.classes).toContain('good');
    expect(display.text).toBe('✓');
  });
 
  test('Habit with partial status shows done class and tilde', () => {
    const display = getTickDisplay({ today_status: 'partial', completed_today: 1 });
    expect(display.classes).toContain('done');
    expect(display.classes).toContain('partial');
    expect(display.text).toBe('~');
  });
 
  test('Habit with not_complete status shows done class and cross', () => {
    const display = getTickDisplay({ today_status: 'not_complete', completed_today: 0 });
    expect(display.classes).toContain('done');
    expect(display.text).toBe('✗');
  });
 
  test('Habit with null status shows empty toggle (status required to show completion)', () => {
    const display = getTickDisplay({ today_status: null, completed_today: 1 });
    expect(display.classes).toBe('habit-check');
    expect(display.text).toBe('');
  });
 
});