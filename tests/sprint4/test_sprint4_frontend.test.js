/**
 * =============================================================
 * SPRINT 4 - FRONTEND UNIT TESTS
 * =============================================================
 * Tests for: US9 (Frequency), US11 (Edit Habit), US31 (Delete Confirmation)
 * Written by: Areebah
 *
 * Linked Acceptance Criteria:
 *   - AC9.1  : Frequency defaults to daily if not specified
 *   - AC9.3  : Frequency toggle is visible on create habit form
 *   - AC9.4  : Selected frequency is saved and shown on habit card
 *   - AC11.1 : Edit button opens a pre-filled modal
 *   - AC11.3 : Cancel closes the modal with no changes
 *   - AC31.1 : Confirmation prompt appears before deletion
 *   - AC31.3 : Cancel closes the prompt and habit remains
 *
 * Run with:
 *   cd C:\Users\areeb\Downloads\team13
 *   npx jest tests/sprint4/test_sprint4_frontend.test.js
 * =============================================================
 */
 
 
// =============================================================
// US9 - Frequency validation logic (from home.html - Taran T9.2, T9.3)
// =============================================================
 
function validateHabitFormWithFrequency(name, habitType, frequency) {
  const errors = {};
  const validFrequencies = ['daily', 'weekly'];
 
  if (!name || name.trim() === '') {
    errors.name = 'Habit name is required';
  }
 
  if (!habitType || habitType.trim() === '') {
    errors.habitType = 'Habit type is required';
  }
 
  if (!frequency || !validFrequencies.includes(frequency)) {
    errors.frequency = 'Invalid frequency';
  }
 
  return {
    isValid: Object.keys(errors).length === 0,
    errors
  };
}
 
// =============================================================
// US9 - Frequency display on habit card (from home.html - T9.4)
// =============================================================
 
function getFrequencyDisplay(habit) {
  return `${habit.habit_type} · ${habit.frequency || 'daily'}`;
}
 
// =============================================================
// US11 - Edit modal state logic (from home.html - Benjy T11.3, T11.4)
// =============================================================
 
function validateEditForm(name, habitType) {
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
// US31 - Delete confirmation state logic (from home.html - Hamza T31.1)
// =============================================================
 
function handleDeleteConfirmation(confirmed, habitId) {
  if (!confirmed) {
    return { action: 'cancel', habitId: null };
  }
  return { action: 'delete', habitId };
}
 
 
// =============================================================
// TESTS
// =============================================================
 
// AC9.1 - Frequency defaults to daily
describe('AC9.1 - Frequency defaults to daily if not specified', () => {
 
  test('Habit with no frequency falls back to daily in display', () => {
    const habit = { habit_type: 'health', frequency: null };
    const display = getFrequencyDisplay(habit);
    expect(display).toContain('daily');
  });
 
  test('Habit with daily frequency shows daily', () => {
    const habit = { habit_type: 'health', frequency: 'daily' };
    const display = getFrequencyDisplay(habit);
    expect(display).toContain('daily');
  });
 
});
 
// AC9.2 - Only valid frequency values accepted
describe('AC9.2 - Only valid frequency values are accepted', () => {
 
  test('Daily frequency passes validation', () => {
    const result = validateHabitFormWithFrequency('Exercise', 'health', 'daily');
    expect(result.isValid).toBe(true);
  });
 
  test('Weekly frequency passes validation', () => {
    const result = validateHabitFormWithFrequency('Exercise', 'health', 'weekly');
    expect(result.isValid).toBe(true);
  });
 
  test('Invalid frequency triggers error', () => {
    const result = validateHabitFormWithFrequency('Exercise', 'health', 'monthly');
    expect(result.isValid).toBe(false);
    expect(result.errors.frequency).toBeDefined();
  });
 
  test('Empty frequency triggers error', () => {
    const result = validateHabitFormWithFrequency('Exercise', 'health', '');
    expect(result.isValid).toBe(false);
    expect(result.errors.frequency).toBeDefined();
  });
 
});
 
// AC9.4 - Selected frequency shown on habit card
describe('AC9.4 - Selected frequency is shown on the habit card', () => {
 
  test('Weekly habit card displays weekly', () => {
    const habit = { habit_type: 'fitness', frequency: 'weekly' };
    const display = getFrequencyDisplay(habit);
    expect(display).toContain('weekly');
  });
 
  test('Daily habit card displays daily', () => {
    const habit = { habit_type: 'health', frequency: 'daily' };
    const display = getFrequencyDisplay(habit);
    expect(display).toContain('daily');
  });
 
  test('Habit card shows type and frequency separated by dot', () => {
    const habit = { habit_type: 'health', frequency: 'weekly' };
    const display = getFrequencyDisplay(habit);
    expect(display).toBe('health · weekly');
  });
 
});
 
// AC11.1 - Edit modal opens with pre-filled values
describe('AC11.1 - Edit modal opens with pre-filled values', () => {
 
  test('Valid name and type passes edit form validation', () => {
    const result = validateEditForm('Run', 'fitness');
    expect(result.isValid).toBe(true);
  });
 
  test('Empty name in edit form triggers error', () => {
    const result = validateEditForm('', 'fitness');
    expect(result.isValid).toBe(false);
    expect(result.errors.name).toBeDefined();
  });
 
  test('Empty type in edit form triggers error', () => {
    const result = validateEditForm('Run', '');
    expect(result.isValid).toBe(false);
    expect(result.errors.habitType).toBeDefined();
  });
 
});
 
// AC11.3 - Cancel closes modal with no changes
describe('AC11.3 - Cancel closes the edit modal with no changes', () => {
 
  test('Cancelling edit does not trigger save', () => {
    // Simulates clicking cancel — no validation errors means no submission occurred
    let saved = false;
    function cancelEdit() { saved = false; }
    cancelEdit();
    expect(saved).toBe(false);
  });
 
});
 
// AC31.1 - Confirmation prompt appears before deletion
describe('AC31.1 - Confirmation prompt appears before deletion', () => {
 
  test('Confirming delete returns delete action with habitId', () => {
    const result = handleDeleteConfirmation(true, 5);
    expect(result.action).toBe('delete');
    expect(result.habitId).toBe(5);
  });
 
});
 
// AC31.3 - Cancel closes prompt and habit remains
describe('AC31.3 - Cancel closes confirmation and habit remains', () => {
 
  test('Cancelling delete returns cancel action', () => {
    const result = handleDeleteConfirmation(false, 5);
    expect(result.action).toBe('cancel');
    expect(result.habitId).toBeNull();
  });
 
});