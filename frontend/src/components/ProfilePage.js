import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './styles.css';


const ProfilePage = () => {
    const [user, setUser] = useState(null);

    useEffect(() => {
        console.log('Fetching user data...'); // useEffect
        // axios.get('/api/users/2/')
        axios.get('http://localhost:8000/api/users/2/')

            .then(response => {
                console.log('User data fetched:', response.data); // data grab
                setUser(response.data);
            })
            .catch(error => {
                console.error('Error fetching user data:', error);
            });
    }, []);
    
    

    if (!user) { // return this while loading
        return <div>Loading...</div>;
    }

    return (
        <div>
            <h1>{user.username}'s Profile</h1>

            <section>
                <h2>Basic Information</h2>
                <p>Username: {user.username}</p>
                <p>Email: {user.email}</p>
            </section>

            <section>
                <h2>Points Information</h2>
                <p>Total Points: {user.points_accumulated}</p>
                <p>Spendable Points: {user.points_spendable}</p>
            </section>

            <section>
                <h2>Achievements and Titles</h2>
                {/* Future Development: Display user's achievements and titles here */}
            </section>

            <section>
                <h2>Visited Locations and Events</h2>
                {/* Future Development: Display user's visited locations and events here */}
            </section>
        </div>
    );
}

export default ProfilePage;