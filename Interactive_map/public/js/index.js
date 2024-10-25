import { getUserIdFromSessionOrPostUser } from './userUtils';
import axios from 'axios';

/* global L */
let map;  // Define `map` globally using `let` for better scope management
let eventsData = [];  // Define `eventsData` globally to make it accessible

document.addEventListener('DOMContentLoaded', () => {
    // Fetch the user ID from session storage or post user data if necessary
    getUserIdFromSessionOrPostUser()
        .then(uid => {
            console.log("User ID retrieved:", uid);
            // Proceed to initialize the map and fetch events after retrieving the user ID
            initializeMap();
            fetchEvents(); 
        })
        .catch(error => {
            // If user information cannot be retrieved, alert the user and redirect to login page
            alert('Failed to retrieve user information. Please log in again.');
            window.location.href = 'http://localhost:3000/login';
        });
});

// Function to initialize the map
function initializeMap() {
    // Initialize the map and set the view to Melbourne, Victoria with a zoom level of 13
    map = L.map('map').setView([-37.8136, 144.9631], 13);

    // Load map tiles from OpenStreetMap with attribution
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
}

// Function to fetch events from the backend
function fetchEvents() {
    const url = CONFIG.BASE_URL + 'events';
    axios.get(url)
        .then(response => {
            const events = response.data;  // Store the events data
            eventsData = events;  // Store events globally for filtering/sorting
            displayFilteredEvents(events);  // Display all events initially
            
            // Add event listeners for filtering and sorting
            document.getElementById('searchBar').addEventListener('input', filterAndSortEvents);
            document.getElementById('categoryFilter').addEventListener('change', filterAndSortEvents);
            document.getElementById('sortBy').addEventListener('change', filterAndSortEvents);
        })
        .catch(error => {
            // Log the error and alert the user in case fetching events fails
            console.error('Error fetching events:', error);
            alert("An error occurred while fetching events. Please try again later.");
        });
}

// Function to add events to the event list
function addEventToList(event) {
    var eventList = document.getElementById('events');  // Get the event list element
    var eventItem = document.createElement('li');  // Create a new list item for each event

    // Display event name and date, and add click event to zoom into the map location
    eventItem.innerHTML = `<strong>${event.name}</strong> (${event.date})`;
    eventItem.addEventListener('click', () => {
        // Set map view to the event location with a higher zoom level
        map.setView(event.location, 15);
        // Display a popup with event details and a check-in button
        L.popup()
            .setLatLng(event.location)
            .setContent(
                `<b>${event.name}</b><br>${event.description}<br>${event.date} at ${event.time}
                <br><button onclick="checkIn('${event.code}', '${event.name}', ${event.location[0]}, ${event.location[1]})">Check In</button>`
            )
            .openOn(map);
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
    // Prompt user to enter the check-in code
    var userCode = prompt("Enter the check-in code:");
    var uid = sessionStorage.getItem('uid');  // Re-fetch `uid` from session storage

    // If user ID is not found, alert the user and exit the function
    if (!uid) {
        console.error('User ID not found in session storage');
        alert("Unable to save check-in. User not found. Please make sure you are logged in.");
        return;
    }

    // If the code matches, proceed with check-in
    if (userCode === eventCode) {
        alert("You have successfully checked in!");

        // Save the check-in information for the user
        const checkInUrl = "http://localhost:3002/locations/checkins/";
        const headers = {
            'Content-Type': 'application/json',
            'Gamification-Api-Key': process.env.REACT_APP_API_KEY
        };
        const checkInData = {
            user_id: uid,
            event_name: eventName,
            latitude: latitude,
            longitude: longitude
        };

        axios.post(checkInUrl, checkInData, { headers })
            .then(response => {
                console.log('Checked in successfully:', response.data);
                alert("Check-in saved successfully!");
            })
            .catch(error => {
                console.error('Error saving check-in:', error);
                alert("An error occurred while saving the check-in. Please try again later.");
            });

        // After successful check-in, update points for the user
        const updatePointsUrl = "http://localhost:3002/users/users/" + uid + "/add_points/";
        const pointsData = {
            'experience_points': 1000,
            'shop_points': 1000
        };

        axios.post(updatePointsUrl, pointsData, { headers })
            .then(response => {
                console.log('Points added:', response.data);
                alert("You have been rewarded with 1000 experience points and 1000 shop points!");
            })
            .catch(error => {
                console.error('Error adding points:', error);
                alert("An error occurred while adding points. Please try again later.");
            });
    } else {
        // If the code does not match, inform the user
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

// Function to display filtered events in the list and add them to the map
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
