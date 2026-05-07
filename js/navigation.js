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

function injectFooter() {
    const footer = document.createElement('footer');
    footer.innerHTML = `&copy; ${new Date().getFullYear()} Hunter McCoy`;
    document.body.appendChild(footer);
}

function highlightActiveSection() {
    const sections = document.querySelectorAll('main section[id]');
    if (!sections.length) return;

    const links = document.querySelectorAll('.navbar-links a');

    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach(entry => {
                if (!entry.isIntersecting) return;
                links.forEach(a => a.classList.remove('active'));
                const active = document.querySelector(
                    `.navbar-links a[href="/#${entry.target.id}"]`
                );
                if (active) active.classList.add('active');
            });
        },
        { rootMargin: '-10% 0px -80% 0px' }
    );

    sections.forEach(s => observer.observe(s));
}

document.addEventListener('DOMContentLoaded', function () {
    const navElement = document.querySelector('nav');
    if (navElement) {
        navElement.innerHTML = createNavigation();
    }
    injectFooter();
    highlightActiveSection();
});
