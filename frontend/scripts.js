document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    const queryInput = document.getElementById('query');
    
    form.addEventListener('submit', () => {
        const loadingIndicator = document.createElement('div');
        loadingIndicator.className = 'loading';
        loadingIndicator.textContent = 'Loading...';
        form.appendChild(loadingIndicator);
    });
});
