const darkMode = document.querySelector('.dark-mode');

const setDarkModeState = (isDarkMode) => {
    localStorage.setItem('darkMode', isDarkMode ? 'dark' : 'light');
    localStorage.setItem('placeholderColor', isDarkMode ? '#aaa' : '#444');
    localStorage.setItem('paginationColor', isDarkMode ? '#fff' : '#000');
};

const toggleDarkMode = () => {
    document.body.classList.toggle('dark-mode-variables');
    darkMode.querySelector('span:nth-child(1)').classList.toggle('active');
    darkMode.querySelector('span:nth-child(2)').classList.toggle('active');
    setDarkModeState(document.body.classList.contains('dark-mode-variables'));

    const paginationItems = document.querySelectorAll('.pagination-item a');
    const isDarkModeEnabled = document.body.classList.contains('dark-mode-variables');

    
    const paginationColor = localStorage.getItem('paginationColor');

    paginationItems.forEach(item => {
        item.style.color = paginationColor;
    });

    const searchBox = document.querySelector('.search-box');
    searchBox.style.backgroundColor = isDarkModeEnabled ? '#202528' : '#fff';
    searchBox.style.color = isDarkModeEnabled ? '#fff' : '#000';

    
    const inputSearch = document.querySelector('.input-search');
    inputSearch.style.color = isDarkModeEnabled ? '#fff' : '#000';
    const placeholderColor = isDarkModeEnabled ? '#aaa' : '#444';
    inputSearch.setAttribute('placeholder', 'Search...');
    inputSearch.style.setProperty('--placeholder-color', placeholderColor);
};

darkMode.addEventListener('click', toggleDarkMode);


const isDarkModeEnabled = localStorage.getItem('darkMode') === 'dark';
const placeholderColor = localStorage.getItem('placeholderColor');
const paginationColor = localStorage.getItem('paginationColor');

if (isDarkModeEnabled) {
    document.body.classList.add('dark-mode-variables');
    toggleDarkMode();
} else {
    const paginationItems = document.querySelectorAll('.pagination-item a');
    paginationItems.forEach(item => {
        item.style.color = paginationColor;
    });
}
