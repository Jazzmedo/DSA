document.addEventListener("DOMContentLoaded", function () {
    const toggleButton = document.getElementById('toggleButton');
    const toggleContent = document.getElementById('toggleContent');

    toggleButton.addEventListener('click', function () {
        const isOpen = toggleButton.textContent.includes("LESS");
        toggleButton.textContent = isOpen ? "EXPLORE MORE" : "EXPLORE LESS";
        toggleContent.style.height = isOpen ? "0" : `${toggleContent.scrollHeight}px`;
    });
});

var divs = document.querySelectorAll('.con');

function handleClick(event) {
    divs.forEach(function (div) {
        div.classList.remove('clicked');
    });

    event.target.classList.add('clicked');
}

divs.forEach(function (div) {
    div.addEventListener('click', handleClick);
});