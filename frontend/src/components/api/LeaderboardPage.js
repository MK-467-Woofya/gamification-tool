import React, { useEffect, useState } from 'react';
import axios from 'axios';
import '../styles.css';
import Container from 'react-bootstrap/Container';

export const LeaderboardPage = () => {
    const [users, setUsers] = useState([]);
    const [timeframe, setTimeframe] = useState('weekly');  // weekly by default
    const currentUserId = sessionStorage.getItem('uid');  // Get current user id

    useEffect(() => {
        // request data by time period
        axios.get(`http://localhost:8000/leaderboard/${timeframe}/`, {
            headers: {
                'Content-Type': 'application/json',
                'Gamification-Api-Key': process.env.REACT_APP_API_KEY,
                'Authorization': `UserID ${currentUserId}`  // send UserID to backend
            }
        })
            .then(response => {
                console.log(response.data);
                setUsers(response.data);
            })
            .catch(error => {
                console.error('Error fetching leaderboard data:', error);
            });
    }, [timeframe, currentUserId]);

    return (
        <Container className="justify-content-md-center leaderboard-container">
            <div>
                <h1>{timeframe.charAt(0).toUpperCase() + timeframe.slice(1)} Leaderboard</h1>
            </div>
            <div className='mt-4'>
                <select onChange={(e) => setTimeframe(e.target.value)}>
                    <option value="weekly">Weekly</option>
                    <option value="monthly">Monthly</option>
                    <option value="yearly">Yearly</option>
                    <option value="alltime">All Time</option>
                </select>
            </div>
            <div>
                <table>
                    <thead>
                        <tr>
                            <th>Username</th>
                            <th>Experience Points</th>
                            <th>Shop Points</th>
                        </tr>
                    </thead>
                    <tbody>
                        {Array.isArray(users) && users.map((user, index) => (
                            <tr key={index} className={String(user.id) === currentUserId ? 'highlight' : ''}>
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