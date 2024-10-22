document.addEventListener("DOMContentLoaded", function() {
    // Initialize the map and set the view to Melbourne, Victoria with a zoom level of 10
    var map = L.map('map').setView([-37.8136, 144.9631], 10);

    // Load map tiles from OpenStreetMap with attribution
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
});