const modal = document.getElementById('myModal'),
    btn = document.getElementById('btn'),
    close = document.getElementById('non');

btn.addEventListener('click', openModal);
close.addEventListener('click', closeModal);
modal.addEventListener('click', closeModal);

// Code to open Modal
function openModal(e) {
    e.preventDefault();
    modal.style.display = "block";
};
// code to close Modal
function closeModal() {
    modal.style.display = "none";
};