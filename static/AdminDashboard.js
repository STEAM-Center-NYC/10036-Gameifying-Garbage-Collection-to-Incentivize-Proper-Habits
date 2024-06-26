const sideMenu = document.querySelector('aside');
const menuBtn = document.getElementById('menu-btn');
const closeBtn = document.getElementById('close-btn');
const darkMode = document.querySelector('.dark-mode');
const paginationLinks = document.querySelectorAll('.pagination-link');
const inputSearch = document.querySelector('.input-search'); // Select the input search element

// Function to set dark mode state in local storage
const setDarkModeState = (isDarkMode) => {
    localStorage.setItem('darkMode', isDarkMode);
};

// Function to toggle dark mode
const toggleDarkMode = () => {
    const isDarkMode = document.body.classList.toggle('dark-mode-variables');
    darkMode.querySelector('span:nth-child(1)').classList.toggle('active');
    darkMode.querySelector('span:nth-child(2)').classList.toggle('active');
    // Update dark mode state in local storage
    setDarkModeState(isDarkMode);
    // Adjust pagination link color
    paginationLinks.forEach(link => {
        link.style.color = isDarkMode ? '#fff' : '#000';
    });
    // Adjust input search color
    inputSearch.style.color = isDarkMode ? '#fff' : '#000'; // Set color based on dark mode
};

// Event listener for opening side menu
menuBtn.addEventListener('click', () => {
    sideMenu.style.display = 'block';
});

// Event listener for closing side menu
closeBtn.addEventListener('click', () => {
    sideMenu.style.display = 'none';
});

// Event listener for toggling dark mode
darkMode.addEventListener('click', toggleDarkMode);

// Retrieve dark mode state from local storage and apply it
const isDarkModeEnabled = JSON.parse(localStorage.getItem('darkMode'));
if (isDarkModeEnabled) {
    toggleDarkMode();
}
