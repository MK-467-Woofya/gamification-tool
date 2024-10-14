/* global L */
let map;
let selectedEvent = null;  // Variable to store the currently selected event

// Initialize the map and set the default view to Melbourne, Victoria
map = L.map('map').setView([-37.8136, 144.9631], 13);

// Load and display OpenStreetMap tiles, with attribution to OpenStreetMap contributors
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Fetch the list of events from the backend and populate the event dropdown
fetch('http://localhost:3002/events')
    .then(response => response.json())  // Convert the response to JSON
    .then(events => {
        const eventList = document.getElementById('event-list');  // Reference the event dropdown
        
        // Loop through each event and add it to the dropdown list
        events.forEach(event => {
            const option = document.createElement('option');  // Create a new option element
            option.value = event.code;  // Use the event's check-in code as the value
            option.textContent = event.name;  // Display the event name in the dropdown
            eventList.appendChild(option);  // Add the option to the dropdown
            
            // Place a marker on the map for each event location
            L.marker([event.location.lat, event.location.lng]).addTo(map)
                .bindPopup(`<strong>${event.name}</strong><br>${event.description}`);  // Bind a popup with event details
        });

        // Add an event listener for when the user selects an event from the dropdown
        eventList.addEventListener('change', function() {
            selectedEvent = events.find(event => event.code === this.value);  // Find the selected event based on its code
            
            if (selectedEvent) {
                // Populate the event details section with the selected event's information
                document.getElementById('event-name').innerText = selectedEvent.name;
                document.getElementById('event-date').innerText = selectedEvent.date;
                document.getElementById('event-time').innerText = selectedEvent.time;
                document.getElementById('event-description').innerText = selectedEvent.description;
                document.getElementById('event-genre').innerText = selectedEvent.genre;
                document.getElementById('event-code').innerText = selectedEvent.code;

                // Enable the buttons to show location and remove the event
                document.getElementById('show-location-btn').disabled = false;
                document.getElementById('remove-event-btn').disabled = false;
            }
        });

        // Event listener for showing the selected event's location on the map
        document.getElementById('show-location-btn').addEventListener('click', function() {
            if (selectedEvent) {
                // Center the map on the selected event's location
                map.setView([selectedEvent.location.lat, selectedEvent.location.lng], 15);
            }
        });

        // Event listener for removing the selected event
        document.getElementById('remove-event-btn').addEventListener('click', function() {
            const userCode = prompt('Please enter the check-in code to remove this event:');  // Ask the user for the check-in code

            // Check if the entered code matches the selected event's check-in code
            if (userCode === selectedEvent.code) {
                deleteEvent(selectedEvent.code);  // Call the delete function if the code matches
            } else {
                alert('Incorrect code! Event removal canceled.');  // Alert if the code is incorrect
            }
        });
    })
    .catch(error => console.error('Error fetching events:', error));  // Handle any errors in fetching the events

// Function to delete the selected event by its check-in code
function deleteEvent(eventCode) {
    // Send a DELETE request to the backend to remove the event by its check-in code
    fetch(`http://localhost:3002/events/${eventCode}`, {
        method: 'DELETE',
    })
    .then(response => {
        if (response.ok) {
            alert('Event removed successfully');  // Notify the user if the event was deleted
            window.location.reload();  // Refresh the page to update the event list
        } else {
            alert('Failed to remove event');  // Handle the case where event removal failed
        }
    })
    .catch(error => console.error('Error removing event:', error));  // Handle any errors during the deletion process
}