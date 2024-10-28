/* global L */
var map = L.map('map').setView([-37.8136, 144.9631], 10);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

function fetchCheckIns(uid, map) {
    const baseUrl = "http://localhost:3002/locations/checkins/";
    const headers = { 'Content-Type': 'application/json', 'Gamification-Api-Key': process.env.REACT_APP_API_KEY };

    axios.get(`${baseUrl}?user=${uid}`, { headers })
        .then(response => {
            const checkIns = response.data;
            checkIns.forEach(checkIn => {
                L.marker([checkIn.latitude, checkIn.longitude])
                    .addTo(map)
                    .bindPopup(`<b>${checkIn.event_name}</b><br>Checked in on ${new Date(checkIn.check_in_time).toLocaleString()}`);

                const listElement = document.createElement('li');
                listElement.textContent = `${checkIn.event_name} - Checked in on ${new Date(checkIn.check_in_time).toLocaleString()}`;
                document.getElementById('checked-events').appendChild(listElement);
            });
        })
        .catch(error => {
            console.error('Error fetching checked-in locations:', error);
            alert("An error occurred while fetching checked-in locations. Please try again later.");
        });
}
