// Shared navigation for all pages
function createNavigation() {
    const currentPath = window.location.pathname;
    const isProjectPage = currentPath.includes('/projects/');
    
    if (isProjectPage) {
        return `
            <a href="/#about">About</a>
            <a href="/">Research</a>
            <a href="/#publications">Publications</a>
            <a href="/#contact">Contact</a>
        `;
    } else {
        return `
            <a href="#about">About</a>
            <a href="#research">Research</a>
            <a href="#publications">Publications</a>
            <a href="#contact">Contact</a>
        `;
    }
}

// Insert navigation when page loads
document.addEventListener('DOMContentLoaded', function() {
    const navElement = document.querySelector('nav');
    if (navElement) {
        navElement.innerHTML = createNavigation();
    }
});
