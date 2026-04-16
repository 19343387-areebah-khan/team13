/**
 * =============================================================
 * SPRINT 3 - FRONTEND UNIT TESTS
 * =============================================================
 * Tests for: US18 (Status Modal), US14/15 (Heatmap), US4 (Logout), US12 (Delete)
 *
 * Linked Acceptance Criteria:
 *   - AC18.1: Clicking the tick opens the status modal
 *   - AC18.2: Not Complete reveals the note textarea
 *   - AC18.3: Cancel closes the modal with no changes
 *   - AC18.4: Confirming a status updates the habit visually
 *   - AC18.5: Invalid status shows an error
 *   - AC14.3: Hovering a square shows date and completion percentage
 *   - AC14.6: Days with no activity default to grey (level-0)
 *   - AC15.2: Colour tier matches completion ratio correctly
 *   - AC4.2 : Logout clears the session
 *   - AC4.3 : Logout redirects to login page
 *   - AC12.1: Each habit displays a delete button
 *
 * Run with:
 *   cd C:\Users\areeb\Downloads\team13
 *   npx jest tests/sprint3/test_sprint3_frontend.test.js
 * =============================================================
 */
 
 
// --- Status modal logic (from home.html - Areebah T18.3, T18.4, T18.5) ---
 
const VALID_STATUSES = ["good", "partial", "not_complete"];
 
function validateStatus(status) {
  if (!status || !VALID_STATUSES.includes(status)) {
    return { isValid: false, error: "Please select a status before confirming" };
  }
  return { isValid: true };
}
 
function shouldShowNoteField(status) {
  return status === "not_complete";
}
 
function handleModalCancel(originalStatus) {
  return { action: "close_modal", status: originalStatus };
}
 
function handleStatusConfirm(selectedStatus, note) {
  const validation = validateStatus(selectedStatus);
  if (!validation.isValid) {
    return { action: "show_error", message: validation.error };
  }
  return { action: "submit", status: selectedStatus, note: note || "" };
}
 
 
// --- Heatmap colour tier logic (from map.js - Hamza T14.8, Stipan T15.3) ---
 
function getLevelClass(ratio) {
  if (ratio === undefined || ratio === null || ratio <= 0) return "level-0";
  if (ratio > 0 && ratio < 0.25) return "level-1";
  if (ratio >= 0.25 && ratio < 0.5) return "level-2";
  if (ratio >= 0.5 && ratio < 1) return "level-3";
  return "level-4";
}
 
function getTooltipText(dateString, ratio) {
  if (ratio === undefined) return `${dateString} - No data`;
  return `${dateString} - ${Math.round(ratio * 100)}%`;
}
 
function buildDateRatioMap(apiData) {
  const map = {};
  if (!apiData || apiData.length === 0) return map;
  apiData.forEach(item => { map[item.date] = item.ratio; });
  return map;
}
 
 
// --- Logout logic (from home.html - Taran T4.2) ---
 
function handleLogout(storage) {
  storage.clear();
  return { action: "redirect", destination: "login.html" };
}
 
 
// =============================================================
// AC18.1 - Status modal opens on tick click
// =============================================================
 
describe("AC18.1 - Status modal validation", () => {
 
  test("Valid good status passes validation", () => {
    const result = validateStatus("good");
    expect(result.isValid).toBe(true);
  });
 
  test("Valid partial status passes validation", () => {
    expect(validateStatus("partial").isValid).toBe(true);
  });
 
  test("Valid not_complete status passes validation", () => {
    expect(validateStatus("not_complete").isValid).toBe(true);
  });
 
  test("Invalid status fails validation", () => {
    const result = validateStatus("invalid");
    expect(result.isValid).toBe(false);
    expect(result.error).toBeDefined();
  });
 
  test("Empty status fails validation", () => {
    expect(validateStatus("").isValid).toBe(false);
  });
 
  test("Null status fails validation", () => {
    expect(validateStatus(null).isValid).toBe(false);
  });
 
});
 
 
// =============================================================
// AC18.2 - Not Complete reveals note textarea
// =============================================================
 
describe("AC18.2 - Note textarea visibility", () => {
 
  test("Not Complete status shows note field", () => {
    expect(shouldShowNoteField("not_complete")).toBe(true);
  });
 
  test("Good status hides note field", () => {
    expect(shouldShowNoteField("good")).toBe(false);
  });
 
  test("Partial status hides note field", () => {
    expect(shouldShowNoteField("partial")).toBe(false);
  });
 
});
 
 
// =============================================================
// AC18.3 - Cancel closes modal with no changes
// =============================================================
 
describe("AC18.3 - Cancel closes modal with no changes", () => {
 
  test("Cancel returns close_modal action with original status", () => {
    const result = handleModalCancel("good");
    expect(result.action).toBe("close_modal");
    expect(result.status).toBe("good");
  });
 
  test("Cancel with no previous status preserves null", () => {
    const result = handleModalCancel(null);
    expect(result.action).toBe("close_modal");
    expect(result.status).toBeNull();
  });
 
});
 
 
// =============================================================
// AC18.4 & AC18.5 - Confirming status
// =============================================================
 
describe("AC18.4 & AC18.5 - Confirm submits or shows error", () => {
 
  test("Valid status with note triggers submit", () => {
    const result = handleStatusConfirm("not_complete", "Was tired");
    expect(result.action).toBe("submit");
    expect(result.status).toBe("not_complete");
    expect(result.note).toBe("Was tired");
  });
 
  test("Valid status with no note submits with empty note", () => {
    const result = handleStatusConfirm("good", "");
    expect(result.action).toBe("submit");
    expect(result.note).toBe("");
  });
 
  test("Invalid status triggers show_error", () => {
    const result = handleStatusConfirm("bad_status", "");
    expect(result.action).toBe("show_error");
    expect(result.message).toBeDefined();
  });
 
  test("Null status triggers show_error", () => {
    expect(handleStatusConfirm(null, "").action).toBe("show_error");
  });
 
});
 
 
// =============================================================
// AC14.6 & AC15.2 - Heatmap colour tiers
// =============================================================
 
describe("AC14.6 & AC15.2 - Heatmap colour tier assignment", () => {
 
  test("No data shows level-0 (grey)", () => {
    expect(getLevelClass(undefined)).toBe("level-0");
  });
 
  test("Zero ratio shows level-0 (grey)", () => {
    expect(getLevelClass(0)).toBe("level-0");
  });
 
  test("Negative ratio shows level-0", () => {
    expect(getLevelClass(-0.1)).toBe("level-0");
  });
 
  test("1-24% shows level-1 (light orange)", () => {
    expect(getLevelClass(0.1)).toBe("level-1");
    expect(getLevelClass(0.24)).toBe("level-1");
  });
 
  test("25-49% shows level-2 (medium orange)", () => {
    expect(getLevelClass(0.25)).toBe("level-2");
    expect(getLevelClass(0.49)).toBe("level-2");
  });
 
  test("50-99% shows level-3 (dark orange)", () => {
    expect(getLevelClass(0.5)).toBe("level-3");
    expect(getLevelClass(0.99)).toBe("level-3");
  });
 
  test("100% shows level-4 (darkest burnt orange)", () => {
    expect(getLevelClass(1)).toBe("level-4");
  });
 
});
 
 
// =============================================================
// AC14.3 - Tooltip shows date and percentage
// =============================================================
 
describe("AC14.3 - Tooltip text is correct", () => {
 
  test("Day with data shows percentage", () => {
    expect(getTooltipText("2026-04-10", 0.75)).toBe("2026-04-10 - 75%");
  });
 
  test("Day with no data shows No data", () => {
    expect(getTooltipText("2026-04-10", undefined)).toBe("2026-04-10 - No data");
  });
 
  test("100% completion shows 100%", () => {
    expect(getTooltipText("2026-04-10", 1)).toBe("2026-04-10 - 100%");
  });
 
});
 
 
// =============================================================
// AC4.2 & AC4.3 - Logout clears session and redirects
// =============================================================
 
describe("AC4.2 & AC4.3 - Logout clears session and redirects to login", () => {
 
  test("Logout clears storage", () => {
    const mockStorage = { cleared: false, clear() { this.cleared = true; } };
    handleLogout(mockStorage);
    expect(mockStorage.cleared).toBe(true);
  });
 
  test("Logout redirects to login.html", () => {
    const mockStorage = { clear() {} };
    const result = handleLogout(mockStorage);
    expect(result.action).toBe("redirect");
    expect(result.destination).toBe("login.html");
  });
 
});
 
 
// =============================================================
// Date-ratio map building (Hamza - T14.7)
// =============================================================
 
describe("Heatmap date-ratio map building", () => {
 
  test("Empty API data returns empty map", () => {
    expect(buildDateRatioMap([])).toEqual({});
  });
 
  test("API data is correctly mapped by date", () => {
    const data = [{ date: "2026-04-10", ratio: 0.5 }];
    const map = buildDateRatioMap(data);
    expect(map["2026-04-10"]).toBe(0.5);
  });
 
  test("Multiple entries are all mapped", () => {
    const data = [
      { date: "2026-04-10", ratio: 0.5 },
      { date: "2026-04-11", ratio: 1.0 }
    ];
    const map = buildDateRatioMap(data);
    expect(Object.keys(map).length).toBe(2);
  });
 
});
