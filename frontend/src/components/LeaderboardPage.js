import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './styles.css';

function LeaderboardPage() {
    const [users, setUsers] = useState([]);
    const [timeframe, setTimeframe] = useState('weekly');  // weekly by default

    useEffect(() => {
        // request data by time period
        axios.get(`http://localhost:8000/leaderboard/${timeframe}/`)
            .then(response => {
                console.log(response.data);
                setUsers(response.data);
            })
            .catch(error => {
                console.error('Error fetching leaderboard data:', error);
            });
    }, [timeframe]);

    return (
        <div>
            <h1>{timeframe.charAt(0).toUpperCase() + timeframe.slice(1)} Leaderboard</h1>
            <select onChange={(e) => setTimeframe(e.target.value)}>
                <option value="weekly">Weekly</option>
                <option value="monthly">Monthly</option>
                <option value="yearly">Yearly</option>
                <option value="alltime">All Time</option>
            </select>
            <table>
                <thead>
                    <tr>
                        <th>Username</th>
                        <th>Points Accumulated</th>
                        <th>Points Spendable</th>
                    </tr>
                </thead>
                <tbody>
                    {Array.isArray(users) && users.map((user, index) => (
                        <tr key={index}>
                            <td>{user.username}</td>
                            <td>{user.points_accumulated}</td>
                            <td>{user.points_spendable}</td>
                        </tr>
                    ))}
                </tbody>

            </table>
        </div>
    );
}

export default LeaderboardPage;
