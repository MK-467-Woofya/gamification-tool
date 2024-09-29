import React, { useEffect, useState } from 'react';
import axios from 'axios';
import '../styles.css';
import Container from 'react-bootstrap/Container';

export const LeaderboardPage = () => {
    const [users, setUsers] = useState([]);
    const [timeframe, setTimeframe] = useState('weekly');  // default
    const [isFriends, setIsFriends] = useState(false);  // global
    const currentUsername = sessionStorage.getItem('username');  // current user name

    useEffect(() => {
        // friend or global
        const apiEndpoint = isFriends
            ? 'http://localhost:8000/leaderboard/friends/'  // friend API
            : `http://localhost:8000/leaderboard/${timeframe}/`;  // global API

        axios.get(apiEndpoint, {
            headers: {
                'Content-Type': 'application/json',
                'Gamification-Api-Key': process.env.REACT_APP_API_KEY,
                'Authorization': `Username ${currentUsername}`  // send user name
            }
        })
            .then(response => {
                console.log(response.data);
                setUsers(response.data);
            })
            .catch(error => {
                console.error('Error fetching leaderboard data:', error);
            });
    }, [timeframe, isFriends, currentUsername]);

    return (
        <Container className="justify-content-md-center leaderboard-container">
            <div>
                <h1>{isFriends ? 'Friends' : timeframe.charAt(0).toUpperCase() + timeframe.slice(1)} Leaderboard</h1>
            </div>
            <div className='mt-4'>
                <button onClick={() => setIsFriends(false)} className={!isFriends ? 'active' : ''}>global</button>
                <button onClick={() => setIsFriends(true)} className={isFriends ? 'active' : ''}>friends</button>
                {!isFriends && (
                    <select onChange={(e) => setTimeframe(e.target.value)}>
                        <option value="weekly">Weekly</option>
                        <option value="monthly">Monthly</option>
                        <option value="yearly">Yearly</option>
                        <option value="alltime">All Time</option>
                    </select>
                )}
            </div>
            <div>
                <table>
                    <thead>
                        <tr>
                            <th>name</th>
                            <th>experience</th>
                            <th>available points</th>
                        </tr>
                    </thead>
                    <tbody>
                        {Array.isArray(users) && users.map((user, index) => (
                            <tr key={index} className={user.is_current_user ? 'highlight' : ''}>
                                <td>{user.username}</td>
                                <td>{user.experience_points}</td>
                                <td>{user.shop_points}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </Container>
    );
}

export default LeaderboardPage;
