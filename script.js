function toggleMenu() {
    const nav = document.getElementById("navlinks");
    if (nav) nav.classList.toggle("open");
}

function showInputInfo(name) {
    alert(name + "\n\nThis is a verified-input demo entry. In the production version, supplier details, certification documents, stock and location can be added here.");
}
