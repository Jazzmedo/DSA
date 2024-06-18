document.addEventListener("DOMContentLoaded", function() {
  const toggleButton = document.getElementById('toggleButton');
  const toggleContent = document.getElementById('toggleContent');

  toggleButton.addEventListener('click', function() {
      const isOpen = toggleButton.textContent.includes("LESS");
      toggleButton.textContent = isOpen ? "EXPLORE MORE" : "EXPLORE LESS";
      toggleContent.style.height = isOpen ? "0" : `${toggleContent.scrollHeight}px`;
  });
});
