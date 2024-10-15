document.addEventListener("DOMContentLoaded", function() {
    // Initialize the map and set the view to Melbourne, Victoria with a zoom level of 10
    var map = L.map('map').setView([-37.8136, 144.9631], 10);

    // Load map tiles from OpenStreetMap with attribution
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    function loadUserCheckIns() {
        const uid = sessionStorage.getItem('uid');  // Assuming the user ID is stored here
        const authToken = sessionStorage.getItem('authToken');  // Assuming a token is stored after login
        if (!uid || !authToken) {
            console.error('User not authenticated or ID not found.');
            return;
        }

        // Fetch user's check-ins using the user's ID and token
        fetch(`http://localhost:8000/api/user/${uid}/checkins/`, {
            headers: {
                'Authorization': `Bearer ${authToken}`,
                'Content-Type': 'application/json'
            }
        })
            .then(response => response.json())
            .then(data => {
                let checkinList = document.getElementById('checked-events');
                data.checkins.forEach(function(checkin) {
                    let listItem = document.createElement('li');
                    listItem.textContent = `${checkin.event_name} - ${checkin.date_checked_in}`;
                    listItem.dataset.lat = checkin.lat;
                    listItem.dataset.lng = checkin.lng;

                    listItem.addEventListener('click', function() {
                        // On click, center the map on the event location and add a marker
                        let latLng = [parseFloat(this.dataset.lat), parseFloat(this.dataset.lng)];
                        map.setView(latLng, 15);
                        L.marker(latLng).addTo(map)
                            .bindPopup(`<b>${checkin.event_name}</b><br>${checkin.date_checked_in}`)
                            .openPopup();
                    });

                    checkinList.appendChild(listItem);
                });
            })
            .catch(error => {
                console.error('Error fetching check-ins:', error);
            });
    }

    // Load user check-ins
    loadUserCheckIns();
});
