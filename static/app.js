let $ = document.querySelector.bind(document);
let $$ = document.querySelectorAll.bind(document);

function toggleHamburger() {
    $$('.bar').forEach(bar => bar.classList.toggle('x'));
    $('nav').classList.toggle('visible');
}

$('.nav-toggle').addEventListener('click', toggleHamburger);

$('#theme-select').addEventListener('change', (e) => {
    $('html').classList.remove(...$('html').classList);
    $('html').classList.add($('#theme-select').value);
    localStorage.setItem("theme", $('#theme-select').value);
});

let selectedTheme = localStorage.getItem("theme");
if (selectedTheme) {
    $('html').classList.add(selectedTheme);
    $('#theme-select').value = selectedTheme;
}