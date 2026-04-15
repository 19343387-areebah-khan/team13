const heatmapGrid = document.getElementById("heatmapGrid");
const monthLabels = document.getElementById("monthLabels");
const logoutBtn = document.getElementById("logoutBtn");

const currentYear = new Date().getFullYear();

function getStoredUserId() {
  const localUserId = localStorage.getItem("user_id");
  const sessionUserId = sessionStorage.getItem("user_id");

  console.log("localStorage user_id:", localUserId);
  console.log("sessionStorage user_id:", sessionUserId);
  console.log("current page:", window.location.href);

  if (localUserId && localUserId !== "undefined" && localUserId !== "null") {
    return localUserId;
  }

  if (sessionUserId && sessionUserId !== "undefined" && sessionUserId !== "null") {
    return sessionUserId;
  }

  return null;
}

function formatDateLocal(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

function getStartMonday(date) {
  const d = new Date(date);
  const day = d.getDay();
  const diff = day === 0 ? -6 : 1 - day;
  d.setDate(d.getDate() + diff);
  d.setHours(0, 0, 0, 0);
  return d;
}

function getEndSunday(date) {
  const d = new Date(date);
  const day = d.getDay();
  const diff = day === 0 ? 0 : 7 - day;
  d.setDate(d.getDate() + diff);
  d.setHours(0, 0, 0, 0);
  return d;
}

function buildDateRatioMap(apiData) {
  const map = {};

  if (!Array.isArray(apiData)) {
    return map;
  }

  apiData.forEach(item => {
    if (item.date) {
      map[item.date] = item.ratio;
    }
  });

  return map;
}

function getLevelClass(ratio) {
  if (ratio === undefined || ratio === null || ratio <= 0) return "level-0";
  if (ratio > 0 && ratio < 0.25) return "level-1";
  if (ratio >= 0.25 && ratio < 0.5) return "level-2";
  if (ratio >= 0.5 && ratio < 1) return "level-3";
  return "level-4";
}

function renderMonthLabels(gridStart, gridEnd) {
  monthLabels.innerHTML = "";

  const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  const placedMonths = new Set();

  let weekIndex = 0;
  const current = new Date(gridStart);

  while (current <= gridEnd) {
    const labelMonth = current.getMonth();
    const labelYear = current.getFullYear();

    if (labelYear === currentYear && !placedMonths.has(labelMonth)) {
      const label = document.createElement("span");
      label.className = "month-label";
      label.textContent = monthNames[labelMonth];
      label.style.gridColumn = `${weekIndex + 1}`;
      monthLabels.appendChild(label);
      placedMonths.add(labelMonth);
    }

    current.setDate(current.getDate() + 7);
    weekIndex++;
  }
}

function renderHeatmap(dateRatioMap) {
  heatmapGrid.innerHTML = "";

  const startOfYear = new Date(currentYear, 0, 1);
  const endOfYear = new Date(currentYear, 11, 31);

  const gridStart = getStartMonday(startOfYear);
  const gridEnd = getEndSunday(endOfYear);

  renderMonthLabels(gridStart, gridEnd);

  let weekIndex = 0;
  const weekStart = new Date(gridStart);

  while (weekStart <= gridEnd) {
    for (let row = 0; row < 7; row++) {
      const currentDate = new Date(weekStart);
      currentDate.setDate(weekStart.getDate() + row);

      const dateString = formatDateLocal(currentDate);
      const ratio = dateRatioMap[dateString];
      const levelClass = getLevelClass(ratio);

      const square = document.createElement("div");
      square.className = `day-square ${levelClass}`;
      square.style.gridColumn = `${weekIndex + 1}`;
      square.style.gridRow = `${row + 1}`;

      const isInCurrentYear = currentDate.getFullYear() === currentYear;

      if (!isInCurrentYear) {
        square.classList.add("outside-year");
      }

      square.title = isInCurrentYear
        ? `${dateString} - ${ratio !== undefined ? Math.round(ratio * 100) + "%" : "No data"}`
        : "";

      heatmapGrid.appendChild(square);
    }

    weekStart.setDate(weekStart.getDate() + 7);
    weekIndex++;
  }
}

async function loadHeatmap() {
  const userId = getStoredUserId();

  if (!userId) {
    alert("No logged-in user found. Please log in again.");
    return;
  }

  try {
    const response = await fetch(`/heatmap?user_id=${encodeURIComponent(userId)}`);
    const data = await response.json();

    console.log("Heatmap API data:", data);

    if (!response.ok) {
      throw new Error(data.error || "Failed to load heatmap data");
    }

    const dateRatioMap = buildDateRatioMap(data);
    renderHeatmap(dateRatioMap);
  } catch (error) {
    console.error("Error loading heatmap:", error);
    alert("Could not load heatmap data.");
  }
}

if (logoutBtn) {
  logoutBtn.addEventListener("click", () => {
    localStorage.removeItem("user_id");
    sessionStorage.removeItem("user_id");
    window.location.href = "login.html";
  });
}

// T26.4: Fetch and populate notes table (Areebah)
async function loadWeeklyNotes() {
  const userId = getStoredUserId();
  if (!userId) return;

  try {
    const response = await fetch(`/weekly-notes?user_id=${encodeURIComponent(userId)}`);
    const data = await response.json();
    const tbody = document.getElementById("notesTableBody");

    if (!data.success || data.notes.length === 0) {
      tbody.innerHTML = `<tr><td colspan="4">No notes logged this week.</td></tr>`;
      return;
    }

    tbody.innerHTML = data.notes.map(note => `
      <tr>
        <td>${note.date}</td>
        <td>${note.habit_name}</td>
        <td><span class="status-badge status-${note.status}">${note.status.replace("_", " ")}</span></td>
        <td>${note.note || ""}</td>
      </tr>
    `).join("");
  } catch (error) {
    console.error("Error loading weekly notes:", error);
  }
}

loadHeatmap();
loadWeeklyNotes();

