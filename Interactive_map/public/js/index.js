/* global L */

// Initialize the map and set the view to Melbourne, Victoria with a zoom level of 13
var map = L.map('map').setView([-37.8136, 144.9631], 13);

// Load map tiles from OpenStreetMap with attribution
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

var eventsData = [];

    // Fetch events from the backend and populate the map and list
fetch('http://localhost:3002/events')
    .then(response => response.json())  // Parse the response as JSON
    .then(events => {
        eventsData = events;  // Store events globally for filtering/sorting
        displayFilteredEvents(events);  // Display all events initially

        // Add event listeners for filtering and sorting
        document.getElementById('searchBar').addEventListener('input', filterAndSortEvents);
        document.getElementById('categoryFilter').addEventListener('change', filterAndSortEvents);
        document.getElementById('sortBy').addEventListener('change', filterAndSortEvents);
    });

function addEventToList(event) {
    var eventList = document.getElementById('events');
    var eventItem = document.createElement('li');

    // Display event name and date, and add click event to zoom into the map location
    eventItem.innerHTML = `<strong>${event.name}</strong> (${event.date})`;
    eventItem.addEventListener('click', () => {
        map.setView(event.location, 15);  // Zoom into the event location on the map
        L.popup()
            .setLatLng(event.location)
            .setContent(
                `<b>${event.name}</b><br>${event.description}<br>${event.date} at ${event.time}
                <br><button onclick="checkIn('${event.code}')">Check In</button>`
            )
            .openOn(map);  // Display a popup with event details and check-in button
    });

    eventList.appendChild(eventItem);  // Add the event to the event list in the sidebar
}

// Function to add event markers to the map
function addEventToMap(event) {
    // Add a marker for the event on the map and bind a popup with event details
    L.marker(event.location).addTo(map)
        .bindPopup(`<b>${event.name}</b><br>${event.description}<br>${event.date} at ${event.time}`);
}

// Function to handle user check-in for an event
window.checkIn = function(eventCode, eventName, latitude, longitude) {
    const userCode = prompt("Enter the check-in code:");
    const uid = sessionStorage.getItem('uid');

    if (!uid) {
        alert("Unable to save check-in. User not found. Please log in.");
        return;
    }

    if (userCode === eventCode) {
        alert("You have successfully checked in!");

        const checkInData = {
            user_id: uid,
            event_name: eventName,
            latitude: latitude,
            longitude: longitude
        };
        const headers = { 'Content-Type': 'application/json', 'Gamification-Api-Key': process.env.REACT_APP_API_KEY };

        // Post check-in data to the backend to be retrieved by checked_in_locations.js
        axios.post("http://localhost:3002/locations/checkins/", checkInData, { headers })
            .then(() => alert("Check-in saved successfully!"))
            .catch(error => alert("An error occurred while saving the check-in."));

        // Update user points after a successful check-in
        axios.post(`http://localhost:3002/users/users/${uid}/add_points/`, { 'experience_points': 1000, 'shop_points': 1000 }, { headers })
            .then(() => alert("You have been rewarded with 1000 experience points and 1000 shop points!"))
            .catch(error => alert("An error occurred while adding points."));
    } else {
        alert("Incorrect code! Please try again.");
    }
};

// Filtering and Sorting Functions
function filterAndSortEvents() {
    // Get search term, selected category, and sorting option from the UI
    var searchTerm = document.getElementById('searchBar').value.toLowerCase();
    var selectedCategory = document.getElementById('categoryFilter').value;
    var sortBy = document.getElementById('sortBy').value;

    // Filter events based on search term and category
    var filteredEvents = eventsData.filter(event => {
        var matchesSearch = event.name.toLowerCase().includes(searchTerm);
        var matchesCategory = selectedCategory === 'all' || event.genre === selectedCategory;
        return matchesSearch && matchesCategory;
    });

    // Sort events based on the selected sorting option
    if (sortBy === 'most-reviewed') {
        filteredEvents.sort((a, b) => b.reviews - a.reviews);
    } else if (sortBy === 'most-viewed') {
        filteredEvents.sort((a, b) => b.views - a.views);
    } else if (sortBy === 'highest-rated') {
        filteredEvents.sort((a, b) => b.rating - a.rating);
    }

    // Display the filtered and sorted events
    displayFilteredEvents(filteredEvents);
}

function displayFilteredEvents(events) {
    var eventList = document.getElementById('events');
    eventList.innerHTML = '';  // Clear the current event list

    // Remove all existing markers from the map
    map.eachLayer(layer => {
        if (layer instanceof L.Marker) {
            map.removeLayer(layer);
        }
    });

    // Add filtered events to the list and map
    events.forEach(event => {
        addEventToList(event);
        addEventToMap(event);
    });
}