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
        document.getElementById('searchBar').addEventListener('input', filterAndSortEvents);  // Handle search input
        document.getElementById('categoryFilter').addEventListener('change', filterAndSortEvents);  // Handle category change
        document.getElementById('sortBy').addEventListener('change', filterAndSortEvents);  // Handle sorting change
    });

// Function to add events to the event list
function addEventToList(event) {
    const eventList = document.getElementById('events');  // Get the event list element
    const eventItem = document.createElement('li');  // Create a list item for each event

    // Display event name and date
    eventItem.innerHTML = `<strong>${event.name}</strong> (${event.date})`;

    // Add click event to focus on the event marker in the map and show event details
    eventItem.addEventListener('click', () => {
        map.setView(event.location, 15);  // Center map on event location
        L.popup()
            .setLatLng(event.location)  // Set the popup location
            .setContent(`
                <b>${event.name}</b><br>${event.description}<br>${event.date} at ${event.time}
                <br><button onclick="checkIn('${event.code}')">Check In</button>`)  // Include a check-in button
            .openOn(map);  // Display the popup on the map
    });

    eventList.appendChild(eventItem);  // Append the event item to the list
}

// Function to add event markers to the map
function addEventToMap(event) {
    L.marker(event.location).addTo(map)
        .bindPopup(`<b>${event.name}</b><br>${event.description}<br>${event.date} at ${event.time}`);  // Bind popup content
}

// Function to handle check-in by comparing the event code with user input
window.checkIn = function(eventCode) {
    const userCode = prompt("Enter the check-in code:");  // Ask the user for the check-in code

    // Validate the user's code against the event code
    if (userCode === eventCode) {
        alert("You have successfully checked in!");  // Success message
    } else {
        alert("Incorrect code! Please try again.");  // Error message if the code is wrong
    }
};

// Function to filter and sort events based on user input
function filterAndSortEvents() {
    const searchTerm = document.getElementById('searchBar').value.toLowerCase();  // Get the search term
    const selectedCategory = document.getElementById('categoryFilter').value;  // Get the selected category
    const sortBy = document.getElementById('sortBy').value;  // Get the selected sorting option

    // Filter events based on the search term and category
    let filteredEvents = eventsData.filter(event => {
        const matchesSearch = event.name.toLowerCase().includes(searchTerm);  // Match search term
        const matchesCategory = selectedCategory === 'all' || event.genre === selectedCategory;  // Match category
        return matchesSearch && matchesCategory;  // Return events that match both criteria
    });

    // Sort the filtered events based on the selected sorting criteria
    if (sortBy === 'most-reviewed') {
        filteredEvents.sort((a, b) => b.reviews - a.reviews);  // Sort by number of reviews
    } else if (sortBy === 'most-viewed') {
        filteredEvents.sort((a, b) => b.views - a.views);  // Sort by number of views
    } else if (sortBy === 'highest-rated') {
        filteredEvents.sort((a, b) => b.rating - a.rating);  // Sort by rating
    }

    displayFilteredEvents(filteredEvents);  // Display the filtered and sorted events
}

// Function to display filtered and sorted events in the list and on the map
function displayFilteredEvents(events) {
    const eventList = document.getElementById('events');
    eventList.innerHTML = '';  // Clear the event list

    // Remove existing map markers
    map.eachLayer(layer => {
        if (layer instanceof L.Marker) {
            map.removeLayer(layer);
        }
    });

    // Add filtered and sorted events to the list and map
    events.forEach(event => {
        addEventToList(event);  // Add event to the sidebar list
        addEventToMap(event);  // Add event marker to the map
    });
}