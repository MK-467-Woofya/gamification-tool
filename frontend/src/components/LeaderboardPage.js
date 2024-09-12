import React, { useEffect, useState } from 'react';
import axios from 'axios';

function LeaderboardPage() {
    const [users, setUsers] = useState([]);
    const [currentUserId, setCurrentUserId] = useState(2); // assume that user id is 2, in future implementation it should be auto-fetched


    useEffect(() => {
        // Fetch leaderboard data
        axios.get('http://localhost:8000/api/users/leaderboard/')
            .then(response => {
                console.log(response.data);
                setUsers(response.data); // Update state with leaderboard data
            })
            .catch(error => {
                console.error('Error fetching leaderboard data:', error);
            });
    }, []);

    return (
        <div>
            <h1>Leaderboard</h1>
            <table>
                <thead>
                    <tr>
                        <th>Username</th>
                        <th>Points Accumulated</th>
                        <th>Points Spendable</th>
                    </tr>
                </thead>
                <tbody>
                    {users.map((user, index) => (
                        <tr key={index} style={{ backgroundColor: user.id === currentUserId ? 'lightgreen' : 'transparent' }}>
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
