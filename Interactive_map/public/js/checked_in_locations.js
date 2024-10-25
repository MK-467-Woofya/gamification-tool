import { getUserIdFromSessionOrPostUser } from './userUtils';
import axios from 'axios';

/* global L */
document.addEventListener("DOMContentLoaded", function() {
    // Fetch the user ID from session storage or post user data if necessary
    getUserIdFromSessionOrPostUser()
        .then(uid => {
            console.log("User ID retrieved:", uid);
            // Proceed to fetch user's checked-in locations

            // Initialize the map and set the view to Melbourne, Victoria with a zoom level of 10
            var map = L.map('map').setView([-37.8136, 144.9631], 10);

            // Load map tiles from OpenStreetMap with attribution
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(map);

            // Base URL for fetching checked-in locations
            var baseUrl = "http://localhost:3002/locations/checkins/";
            var headers = {
                'Content-Type': 'application/json',
                'Gamification-Api-Key': process.env.REACT_APP_API_KEY  // API key for accessing the backend
            };

            // Fetch the user's checked-in locations from the backend
            axios.get(baseUrl + "?user=" + uid, { headers })
                .then(response => {
                    const checkIns = response.data;
                    // Loop through each checked-in location and add it to the map and list
                    checkIns.forEach(checkIn => {
                        // Add a marker for each checked-in location on the map
                        L.marker([checkIn.latitude, checkIn.longitude])
                            .addTo(map)
                            .bindPopup(`<b>${checkIn.event_name}</b><br>Checked in on ${new Date(checkIn.check_in_time).toLocaleString()}`);

                        // Create a list item for each checked-in location
                        var listElement = document.createElement('li');
                        listElement.textContent = `${checkIn.event_name} - Checked in on ${new Date(checkIn.check_in_time).toLocaleString()}`;
                        
                        // Append the list item to the checked-in events list in the HTML
                        document.getElementById('checked-events').appendChild(listElement);
                    });
                })
                .catch(error => {
                    // Log the error and alert the user in case of any issues during the fetch
                    console.error('Error fetching checked-in locations:', error);
                    alert("An error occurred while fetching checked-in locations. Please try again later.");
                });
        })
        .catch(error => {
            // If user information cannot be retrieved, alert the user and redirect to login page
            alert('Failed to retrieve user information. Please log in again.');
            window.location.href = 'http://localhost:3000/login';
        });
});
