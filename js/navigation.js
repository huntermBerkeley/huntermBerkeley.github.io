function createNavigation() {
    return `
        <div class="navbar-brand">
            <a href="/">Hunter McCoy</a>
        </div>
        <button class="navbar-toggle" onclick="toggleNav()" aria-label="Toggle navigation">&#9776;</button>
        <div class="navbar-links" id="nav-links">
            <a href="/#about">About</a>
            <a href="/#research">Research</a>
            <a href="/#publications">Publications</a>
            <a href="/blog/">Blog</a>
            <a href="/#contact">Contact</a>
        </div>
    `;
}

function toggleNav() {
    document.getElementById('nav-links').classList.toggle('open');
}

document.addEventListener('DOMContentLoaded', function () {
    const navElement = document.querySelector('nav');
    if (navElement) {
        navElement.innerHTML = createNavigation();
    }
});
