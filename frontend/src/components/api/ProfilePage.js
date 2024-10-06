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

        var url = "http://localhost:8000/users/users/";
        var uid = sessionStorage.getItem('uid');
        var headers = {
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

    function handleSubmit(e) {
        e.preventDefault();

        var url = "http://localhost:8000/users/users/";
        var uid = sessionStorage.getItem('uid');
        var headers = {
            'Content-Type': 'application/json',
            'Gamification-Api-Key': process.env.REACT_APP_API_KEY
        };

        const data = {
            'experience_points': 1000,
            'shop_points':  1000
        };

        var update_points_url = url + uid + '/update_points/';

        axios.patch(update_points_url, data, { headers })
        .then(response => {
            console.log('Points added:', response.data);
        })
        .catch(error => {
            console.error('Error adding points:', error);
        });
    }


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
                <form onSubmit={handleSubmit}>
                    <button type="submit">+1000 points</button>
                </form>
            </section>

            <Container className="justify-content-md-center">
            <div>
                <h1>Titles</h1>
            </div>
            <div>
                <table>
                    <thead>
                        <tr>
                            <th>Title name</th>
                            <th>Title text</th>
                            <th>Cost</th>
                        </tr>
                    </thead>
                    <tbody>
                        {Array.isArray(user.titles) && user.titles.map((title, index) => (
                            <tr key={index}>
                                <td>{title.name}</td>
                                <td>{title.text}</td>
                                <td>{title.cost}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
            </Container>

            <Container className="justify-content-md-center">
            <div>
                <h1>Avatars</h1>
            </div>
            <div>
                <table>
                    <thead>
                        <tr>
                            <th>Avatar name</th>
                            <th>Avatar</th>
                            <th>Cost</th>
                        </tr>
                    </thead>
                    <tbody>
                        {Array.isArray(user.avatars) && user.avatars.map((avatar, index) => (
                            <tr key={index}>
                                <td>{avatar.name}</td>
                                <td><img src={avatar.img_url} alt={avatar.name} width={60} height={60}/></td>
                                <td>{avatar.cost}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
            </Container>

            <section>
                <h2>Visited Locations and Events</h2>
                {/* Future Development: Display user's visited locations and events here */}
            </section>
        </Container>
    );
}
