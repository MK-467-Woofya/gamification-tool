// src/components/QuizLeaderboard.js

import React, { useEffect, useState } from 'react';
import axios from 'axios';

const QuizLeaderboard = ({ quizId }) => {
    const [leaderboardData, setLeaderboardData] = useState([]);
    const [showLeaderboard, setShowLeaderboard] = useState(false);
    const currentUsername = sessionStorage.getItem('username');

    const toggleLeaderboard = () => {
        setShowLeaderboard(!showLeaderboard);
    };

    useEffect(() => {
        if (showLeaderboard) {
            axios.get(`http://localhost:8000/quiz/${quizId}/leaderboard/`, {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Username ${currentUsername}`
                }
            })
            .then(response => {
                setLeaderboardData(response.data);
            })
            .catch(error => {
                console.error('Error fetching quiz leaderboard data:', error);
            });
        }
    }, [showLeaderboard, quizId, currentUsername]);

    return (
        <div className="quiz-leaderboard">
            <button onClick={toggleLeaderboard} className="toggle-leaderboard-button">
                {showLeaderboard ? 'Hide Leaderboard' : 'Show Leaderboard'}
            </button>
            {showLeaderboard && (
                <div className="leaderboard-content">
                    <h3>Quiz Leaderboard</h3>
                    <table>
                        <thead>
                            <tr>
                                <th>Rank</th>
                                <th>Username</th>
                                <th>Total Correct Answers</th>
                            </tr>
                        </thead>
                        <tbody>
                            {leaderboardData.map((user, index) => (
                                <tr key={index} className={user.username === currentUsername ? 'current-user' : ''}>
                                    <td>{index + 1}</td>
                                    <td>{user.username}</td>
                                    <td>{user.total_correct}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
};

export default QuizLeaderboard;
