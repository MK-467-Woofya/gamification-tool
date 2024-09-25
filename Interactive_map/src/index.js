/* global L */

// Initialize the map and set the view to Melbourne, Victoria
var map = L.map('map').setView([-37.8136, 144.9631], 13);

// Load map tiles from OpenStreetMap
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Fetch events from the backend
fetch('http://localhost:3000/events')
    .then(response => response.json())  // Parse the response as JSON
    .then(events => {
        // Loop through each event and display it on both the event list and map
        events.forEach(event => {
            addEventToList(event);  // Add the event to the sidebar list
            addEventToMap(event);   // Add the event marker to the map
        });
    });

// Function to add events to the event list
function addEventToList(event) {
    const eventList = document.getElementById('events');
    const eventItem = document.createElement('li');
    eventItem.innerHTML = `<strong>${event.name}</strong> (${event.date})`;

    // Add event listener for clicking an event in the list
    eventItem.addEventListener('click', () => {
        // Center the map on the event location and display the popup with details
        map.setView(event.location, 15);
        L.popup()
            .setLatLng(event.location)  // Position the popup at the event location
            .setContent(`
                <b>${event.name}</b><br>${event.description}<br>${event.date} at ${event.time}
                <br><button onclick="checkIn('${event.code}')">Check In</button>`)  // Add a Check-In button inside the popup
            .openOn(map);
    });

    eventList.appendChild(eventItem);  // Add the event item to the list in the sidebar
}

// Function to add markers to the map for each event
function addEventToMap(event) {
    L.marker(event.location).addTo(map)
        .bindPopup(`<b>${event.name}</b><br>${event.description}<br>${event.date} at ${event.time}`);
}

// Function to handle check-in by comparing user input with the event code
window.checkIn = function(eventCode) {
    // Prompt user to enter the check-in code
    const userCode = prompt("Enter the check-in code:");
    
    // Validate the check-in code
    if (userCode === eventCode) {
        alert("You have successfully checked in!");  // Display success message
    } else {
        alert("Incorrect code! Please try again.");  // Display error message if code is wrong
    }
};