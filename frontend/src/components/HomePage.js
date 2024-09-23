import React from 'react';
import { Button, Typography, Container, Box, CircularProgress } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import './styles.css';

function HomePage() {
    const navigate = useNavigate();

    const goToProfile = () => {
        navigate('/profile');  // Navigation
    };

    const goToLeaderboard = () => {
        navigate('/leaderboard');
    };

    return (
        <div>
            <h1>Welcome to Woofya</h1>
            <p>Enhance your dog's life with fun events and rewards!</p>
            <button onClick={goToProfile}>Go to Profile Page</button>
            <button onClick={goToLeaderboard}>Go to Leaderboard</button> {/* leaderboard button */}
        </div>
    );
}

export default HomePage;