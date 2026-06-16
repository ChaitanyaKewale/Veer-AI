// VeerAI Main JavaScript

// Highlight active nav link
document.addEventListener('DOMContentLoaded', function () {
    const links = document.querySelectorAll('.nav-link');
    links.forEach(link => {
        if (link.href === window.location.href) {
            link.style.background = '#4a6741';
            link.style.color = '#c9a227';
        }
    });
});
