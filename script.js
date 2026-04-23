const STORAGE_KEY = "habitus-habits-v1";
const DAYS_TARGET = 21;

const form = document.getElementById("habit-form");
const input = document.getElementById("habit-input");
const list = document.getElementById("habit-list");
const emptyState = document.getElementById("empty-state");
const itemTemplate = document.getElementById("habit-item-template");

let habits = loadHabits();

function loadHabits() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw);
    if (!Array.isArray(parsed)) return [];
    return parsed
      .filter((habit) => habit && typeof habit.name === "string")
      .map((habit) => ({
        id: habit.id || crypto.randomUUID(),
        name: habit.name.trim(),
        completedDays: Math.min(Math.max(Number(habit.completedDays) || 0, 0), DAYS_TARGET)
      }));
  } catch (error) {
    return [];
  }
}

function saveHabits() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(habits));
}

function addHabit(name) {
  habits.unshift({
    id: crypto.randomUUID(),
    name: name.trim(),
    completedDays: 0
  });
  saveHabits();
  renderHabits();
}

function markDone(habitId) {
  habits = habits.map((habit) => {
    if (habit.id !== habitId) return habit;
    return {
      ...habit,
      completedDays: Math.min(habit.completedDays + 1, DAYS_TARGET)
    };
  });
  saveHabits();
  renderHabits();
}

function deleteHabit(habitId) {
  habits = habits.filter((habit) => habit.id !== habitId);
  saveHabits();
  renderHabits();
}

function renderHabits() {
  list.innerHTML = "";
  emptyState.hidden = habits.length > 0;

  habits.forEach((habit) => {
    const item = itemTemplate.content.firstElementChild.cloneNode(true);
    const nameEl = item.querySelector(".habit-name");
    const progressTextEl = item.querySelector(".progress-text");
    const progressFillEl = item.querySelector(".progress-fill");
    const doneBtn = item.querySelector(".done-btn");
    const deleteBtn = item.querySelector(".delete-btn");

    const percent = Math.round((habit.completedDays / DAYS_TARGET) * 100);
    const complete = habit.completedDays >= DAYS_TARGET;

    nameEl.textContent = habit.name;
    progressTextEl.textContent = `${habit.completedDays}/${DAYS_TARGET} days completed (${percent}%)`;
    progressFillEl.style.width = `${percent}%`;

    if (complete) {
      item.classList.add("progress-complete");
      doneBtn.textContent = "Completed";
      doneBtn.disabled = true;
    }

    doneBtn.addEventListener("click", () => markDone(habit.id));
    deleteBtn.addEventListener("click", () => deleteHabit(habit.id));

    list.appendChild(item);
  });
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const habitName = input.value.trim();
  if (!habitName) return;
  addHabit(habitName);
  input.value = "";
  input.focus();
});

renderHabits();
