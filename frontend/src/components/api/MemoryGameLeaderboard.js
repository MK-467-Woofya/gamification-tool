// frontend/src/components/api/MemoryGameLeaderboard.js

import React, { useEffect, useState } from 'react';
import axios from 'axios';

const MemoryGameLeaderboard = () => {
    const [leaderboard, setLeaderboard] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        axios.get(process.env.REACT_APP_BASE_URL + 'memory-game/leaderboard/')
            .then(response => {
                setLeaderboard(response.data);
                setLoading(false);
            })
            .catch(error => {
                console.error('Error fetching leaderboard:', error);
                setError('Failed to load leaderboard.');
                setLoading(false);
            });
    }, []);

    if (loading) {
        return <div>Loading leaderboard...</div>;
    }

    if (error) {
        return <div>{error}</div>;
    }

    return (
        <div className="leaderboard-container">
            <h2>Memory Game Leaderboard</h2>
            <table>
                <thead>
                    <tr>
                        <th>Rank</th>
                        <th>Username</th>
                        <th>Total Score</th>
                    </tr>
                </thead>
                <tbody>
                    {leaderboard.map((entry, index) => (
                        <tr key={entry.username}>
                            <td>{index + 1}</td>
                            <td>{entry.username}</td>
                            <td>{entry.total_score}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default MemoryGameLeaderboard;
