import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Container from 'react-bootstrap/Container';
/**
 * User profile showing the Gamification information about user, 
 * and linking to other user API pages
 * 
 */
export const ProfilePage = () => {
    const [user, setUser] = useState(null);

    useEffect(() => {
        console.log('Fetching user data...'); // useEffect

        const url = "http://localhost:8000/users/users/";
        const uid = sessionStorage.getItem('uid');

        const headers = {
            'Content-Type': 'application/json',
            'Gamification-Api-Key': process.env.REACT_APP_API_KEY
        };

        axios.get(url + uid + '/', { headers })

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
        <Container className="justify-content-md-center">
            <h1>{user.username}'s Profile</h1>

            <section>
                <h2>Basic Information</h2>
                <p>Username: {user.username}</p>
                <p>User ID: {user.id}</p>
            </section>

            <section>
                <h2>Points Information</h2>
                <p>Level: {user.level}</p>
                <p>Experience: {user.experience_points}</p>
                <p>Shop Points: {user.shop_points}</p>
            </section>

            <section>
                <h2>Achievements and Titles</h2>
                <p>Title: {user.title}</p>
            </section>

            <section>
                <h2>Visited Locations and Events</h2>
                {/* Future Development: Display user's visited locations and events here */}
            </section>
        </Container>
    );
}
