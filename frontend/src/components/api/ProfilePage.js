import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Container from 'react-bootstrap/Container';

import { ProfileAvatarList } from './marketplace/AvatarsComponents/ProfileAvatarList';
import { ProfileTitleList } from './marketplace/TitleComponents/ProfileTitleList';


/**
 * User profile showing the Gamification information about user, 
 * and linking to other user API pages
 */
export const ProfilePage = () => {
    const [user, setUser] = useState(null);
    const [avatars, setAvatars] = useState(null);
    const [titles, setTitles] = useState(null);

    const uid = sessionStorage.getItem('uid');

    /** Set state for the user and their marketplace items */
    useEffect(() => {
        const headers = {
            'Content-Type': 'application/json',
            'Gamification-Api-Key': process.env.REACT_APP_API_KEY
        };
        const user_url = process.env.REACT_APP_BASE_URL + "users/users/";
        axios.get(user_url + uid + '/', { headers })
            .then(response => {
                console.log('User data fetched:', response.data);
                setUser(response.data);
                setAvatars(response.data.avatars);
                setTitles(response.data.titles);
            })
            .catch(error => {
                console.error('Error fetching user data:', error);
            });
        }, []);

    /** Function to add 100 points to the user
     *  Updates the points mirrored in the request
     *  And updates the User's level
     */
    function handleSubmit(e) {
        e.preventDefault();

        var url = process.env.REACT_APP_BASE_URL + "users/users/";
        var uid = sessionStorage.getItem('uid');
        var headers = {
            'Content-Type': 'application/json',
            'Gamification-Api-Key': process.env.REACT_APP_API_KEY
        };

        const data = {
            'experience_points': 100,
            'shop_points':  100
        };

        var update_points_url = url + uid + '/add_points/';

        axios.patch(update_points_url, data, { headers })
        .then(response => {
            console.log('Points added:', response.data);
        })
        .catch(error => {
            console.error('Error adding points:', error);
        });

        setUser(prevUser => ({
            ...prevUser,
            experience_points: Math.min(prevUser.experience_points + 100,9999999),
            shop_points: Math.min(prevUser.shop_points + 100,9999999),
            level: Math.floor(0.1 * Math.sqrt(prevUser.experience_points)) + 1
        }));
    }

    // Loading while requests return
    if (!user || !avatars) {
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
                <form onSubmit={handleSubmit}>
                    <button type="submit">+100 points</button>
                </form>
            </section>
            <>
                <ProfileTitleList user={user} titles={titles} setUser={setUser} setTitles={setTitles}/>
            </>
            <>
                <ProfileAvatarList user={user} avatars={avatars} setUser={setUser} setAvatars={setAvatars}/>
            </>
            <section>
                <h2>Visited Locations and Events</h2>
                {/* Future Development: Display user's visited locations and events here */}
            </section>
        </Container>
    );
}
