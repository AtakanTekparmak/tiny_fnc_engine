function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
}

function applyDarkMode() {
    if (localStorage.getItem('darkMode') === 'true') {
        document.body.classList.add('dark-mode');
    }
}

function searchDocs() {
    const searchInput = document.getElementById('search-input');
    const searchTerm = searchInput.value.toLowerCase();
    const contentElements = document.querySelectorAll('.content h1, .content h2, .content h3, .content p');

    contentElements.forEach(element => {
        const text = element.textContent.toLowerCase();
        if (text.includes(searchTerm)) {
            element.style.backgroundColor = 'yellow';
        } else {
            element.style.backgroundColor = '';
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
    applyDarkMode();
    const searchInput = document.getElementById('search-input');
    searchInput.addEventListener('input', searchDocs);
});