let habitName = ''; // Global variable to store the user's habit name
let habitProgress = []; // Array to store progress for the habit
const habitForm = document.getElementById('habitForm');
const completeHabitBtn = document.getElementById('completeHabitBtn');
const loseHabitBtn = document.getElementById('loseHabitBtn');
const trackingMessage = document.getElementById('trackingMessage');
const progressList = document.getElementById('progressList');

// Function to initialize the habit tracker
function initHabitTracker() {
    habitName = ''; // Reset habit name
    habitProgress = []; // Clear previous progress
    updateProgressDisplay();
    trackingMessage.textContent = ''; // Clear tracking message
    completeHabitBtn.disabled = true; // Disable buttons until habit is set
    loseHabitBtn.disabled = true;
}

// Event listener to handle the habit form submission
habitForm.addEventListener('submit', function(e) {
    e.preventDefault(); // Prevent the form from submitting normally
    
    habitName = document.getElementById('habitName').value.trim();
    
    if (habitName !== '') {
        // Enable tracking buttons once habit is set
        completeHabitBtn.disabled = false;
        loseHabitBtn.disabled = false;
        trackingMessage.textContent = `You are working on: ${habitName}`;
        habitForm.reset(); // Reset form after submission
    } else {
        alert('Please enter a habit name.');
    }
});

// Event listener to mark habit as completed today
completeHabitBtn.addEventListener('click', function() {
    const today = new Date().toLocaleDateString();
    habitProgress.push({ status: 'Completed', date: today });
    updateProgressDisplay();
});

// Event listener to mark habit as failed today
loseHabitBtn.addEventListener('click', function() {
    const today = new Date().toLocaleDateString();
    habitProgress.push({ status: 'Failed', date: today });
    updateProgressDisplay();
});

// Function to update the displayed progress list
function updateProgressDisplay() {
    progressList.innerHTML = ''; // Clear the existing list

    habitProgress.forEach((entry) => {
        const listItem = document.createElement('li');
        listItem.textContent = `${entry.status} - ${entry.date}`;
        progressList.appendChild(listItem);
    });
}

// Initialize habit tracker when the page loads
initHabitTracker();
//szusbgvksgs