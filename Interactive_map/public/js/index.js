/* global L */

// Initialize the map and set the view to Melbourne, Victoria with a zoom level of 13
var map = L.map('map').setView([-37.8136, 144.9631], 13);

// Load map tiles from OpenStreetMap with attribution
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

let eventsData = [];  // Global variable to store all event data

// Fetch events from the backend and populate the map and list
fetch('http://localhost:3000/events')
    .then(response => response.json())  // Parse the response as JSON
    .then(events => {
        eventsData = events;  // Store events globally for filtering/sorting
        displayFilteredEvents(events);  // Display all events initially
        
        // Add event listeners for filtering and sorting
        document.getElementById('searchBar').addEventListener('input', filterAndSortEvents);
        document.getElementById('categoryFilter').addEventListener('change', filterAndSortEvents);
        document.getElementById('sortBy').addEventListener('change', filterAndSortEvents);
    });

// Function to add events to the event list
function addEventToList(event) {
    const eventList = document.getElementById('events');
    const eventItem = document.createElement('li');

    eventItem.innerHTML = `<strong>${event.name}</strong> (${event.date})`;
    eventItem.addEventListener('click', () => {
        map.setView(event.location, 15);
        L.popup()
            .setLatLng(event.location)
            .setContent(
                `<b>${event.name}</b><br>${event.description}<br>${event.date} at ${event.time}
                <br><button onclick="checkIn('${event.code}')">Check In</button>`
            )
            .openOn(map);
    });

    eventList.appendChild(eventItem);
}

// Function to add event markers to the map
function addEventToMap(event) {
    L.marker(event.location).addTo(map)
        .bindPopup(`<b>${event.name}</b><br>${event.description}<br>${event.date} at ${event.time}`);
}

// Function to handle check-in by comparing the event code with user input
window.checkIn = function(eventCode) {
    const userCode = prompt("Enter the check-in code:");

    if (userCode === eventCode) {
        alert("You have successfully checked in!");
    } else {
        alert("Incorrect code! Please try again.");
    }
};

function navigateToAddEventPage() {
    window.location.href = '/add-event'; // Directly navigate using backend route
}

function navigateToRemoveEventPage() {
    window.location.href = '/remove-event'; // Directly navigate using backend route
}

// Filtering and Sorting Functions
function filterAndSortEvents() {
    const searchTerm = document.getElementById('searchBar').value.toLowerCase();
    const selectedCategory = document.getElementById('categoryFilter').value;
    const sortBy = document.getElementById('sortBy').value;

    let filteredEvents = eventsData.filter(event => {
        const matchesSearch = event.name.toLowerCase().includes(searchTerm);
        const matchesCategory = selectedCategory === 'all' || event.genre === selectedCategory;
        return matchesSearch && matchesCategory;
    });

    if (sortBy === 'most-reviewed') {
        filteredEvents.sort((a, b) => b.reviews - a.reviews);
    } else if (sortBy === 'most-viewed') {
        filteredEvents.sort((a, b) => b.views - a.views);
    } else if (sortBy === 'highest-rated') {
        filteredEvents.sort((a, b) => b.rating - a.rating);
    }

    displayFilteredEvents(filteredEvents);
}

function displayFilteredEvents(events) {
    const eventList = document.getElementById('events');
    eventList.innerHTML = '';

    map.eachLayer(layer => {
        if (layer instanceof L.Marker) {
            map.removeLayer(layer);
        }
    });

    events.forEach(event => {
        addEventToList(event);
        addEventToMap(event);
    });
}
