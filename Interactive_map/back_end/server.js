// Import the Express framework for building the server.
const express = require('express');  
// File system module to interact with the local file system.
const fs = require('fs');  
// Middleware to parse incoming request bodies as JSON.
const bodyParser = require('body-parser');  
// Middleware to enable Cross-Origin Resource Sharing (CORS), allowing requests from different origins.
const cors = require('cors');
// Path module to handle and transform file paths.
const path = require('path');

// Initialize an Express application.
const app = express();  

// Middleware setup
app.use(bodyParser.json());  // Use bodyParser to parse JSON bodies into JavaScript objects.
app.use(cors());  // Allow Cross-Origin Resource Sharing, enabling the frontend and backend to communicate when hosted on different origins.

// Define the path to the events data file.
const EVENTS_FILE = path.join(__dirname, 'events.json');  // Path to the events.json file where event data is stored.

// Serve static files from the 'public' directory
app.use(express.static(path.join(__dirname, '../public')));  // Serve static files from the public directory.

// Route to fetch all events
app.get('/events', (req, res) => {
    // Read the events.json file to retrieve all event data.
    fs.readFile(EVENTS_FILE, (err, data) => {
        if (err) {
            // If there's an error reading the file, send a 500 status (server error) with an error message.
            return res.status(500).json({ error: 'Failed to load events' });
        }
        // Parse the file's contents as JSON and send it as the response.
        const events = JSON.parse(data);
        res.json(events);
    });
});

// Route to add a new event
app.post('/events', (req, res) => {
    const newEvent = req.body;  // Extract the new event data from the request body.
    
    // Read the existing events from the JSON file.
    fs.readFile(EVENTS_FILE, (err, data) => {
        if (err) {
            // If there's an error reading the file, send a 500 status with an error message.
            return res.status(500).json({ error: 'Failed to read events' });
        }
        const events = JSON.parse(data);  // Parse the existing events.
        events.push(newEvent);  // Add the new event to the list.

        // Write the updated events array back to the events.json file.
        fs.writeFile(EVENTS_FILE, JSON.stringify(events, null, 2), (err) => {
            if (err) {
                // If there's an error saving the updated events, send a 500 status with an error message.
                return res.status(500).json({ error: 'Failed to save event' });
            }
            // Send a success response if the event was added successfully.
            res.status(200).json({ message: 'Event added successfully' });
        });
    });
});

// Route to delete an event by its check-in code
app.delete('/events/:code', (req, res) => {
    const eventCode = req.params.code;  // Extract the event's check-in code from the request URL parameters.
    
    // Read the current list of events from the events.json file.
    fs.readFile(EVENTS_FILE, (err, data) => {
        if (err) {
            // If there's an error reading the file, send a 500 status with an error message.
            return res.status(500).json({ error: 'Failed to load events' });
        }
        let events = JSON.parse(data);  // Parse the JSON data.
        
        // Find the index of the event to be deleted using the provided code.
        const eventIndex = events.findIndex(event => event.code === eventCode);
        if (eventIndex === -1) {
            // If the event is not found, send a 404 status (not found) with an error message.
            return res.status(404).json({ error: 'Event not found with the provided code' });
        }

        // Remove the event from the array of events.
        events.splice(eventIndex, 1);

        // Save the updated events array back to the events.json file.
        fs.writeFile(EVENTS_FILE, JSON.stringify(events, null, 2), (err) => {
            if (err) {
                // If there's an error saving the updated events, send a 500 status with an error message.
                return res.status(500).json({ error: 'Failed to save updated events' });
            }
            // Send a success response if the event was deleted successfully.
            res.status(200).json({ message: 'Event deleted successfully' });
        });
    });
});

// Serve the main index.html file for the root route ('/')
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, '../public', 'index.html'));  // Serve the index.html file when visiting the root URL.
});

// Start the server and listen on port 3000
app.listen(3000, () => {
    console.log('Backend running on http://localhost:3000');  // Log a message when the server is successfully running on port 3000.
});
