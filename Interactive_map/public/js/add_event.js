/* global L */
var selectedLocation = null;  // Variable to store the selected location coordinates

// Initialize the map and set the view to Melbourne, Victoria with zoom level 13
var map = L.map('map').setView([-37.8136, 144.9631], 13);

// Load OpenStreetMap tiles for map rendering, with attribution to OpenStreetMap contributors
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Event listener for clicking on the map to select the event location
// When the map is clicked, it captures the latitude and longitude of the clicked location
map.on('click', function(e) {
    selectedLocation = [e.latlng.lat, e.latlng.lng];  // Store the selected location
    // Update the HTML element to show the selected location
    document.getElementById('event-location').innerText = 
        `Selected Location: (${selectedLocation[0].toFixed(4)}, ${selectedLocation[1].toFixed(4)})`;
});

// Event listener for handling the form submission when adding a new event
document.getElementById('event-form').addEventListener('submit', function(e) {
    e.preventDefault();  // Prevent default form submission behavior

    // Check if a location has been selected on the map
    if (!selectedLocation) {
        alert('Please select a location on the map.');  // Alert the user if no location is selected
        return;  // Stop the form submission
    }

    // Create a new event object with the details from the form fields
    const newEvent = {
        name: document.getElementById('name').value,  // Event name
        date: document.getElementById('date').value,  // Event date
        time: document.getElementById('time').value,  // Event time
        description: document.getElementById('description').value,  // Event description
        genre: document.getElementById('genre').value,  // Event genre selected from the dropdown
        code: document.getElementById('code').value,  // Unique 5-digit check-in code for the event
        location: {  // Event location as an object with latitude and longitude
            lat: selectedLocation[0],
            lng: selectedLocation[1]
        }
    };

    // Send the event data to the backend API using the POST method
    fetch('http://localhost:3002/events', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'  // Specify that the request body is in JSON format
        },
        body: JSON.stringify(newEvent)  // Convert the newEvent object to a JSON string for transmission
    })
    .then(response => response.json())  // Parse the JSON response from the server
    .then(data => {
        // Check if the event was successfully added by looking at the message in the response
        if (data.message === 'Event added successfully') {
            alert('Event added successfully!');  // Notify the user that the event was added
            // Optionally, reset the form fields after a successful submission
            document.getElementById('event-form').reset();
            document.getElementById('event-location').innerText = '';  // Clear the selected location text
        } else {
            alert('Error adding event. Please try again.');  // Handle any errors in event submission
        }
    })
    .catch(err => {
        // Log the error and alert the user if there was a connection issue with the backend
        console.error('Error:', err);
        alert('Failed to connect to the server.');
    });
});
