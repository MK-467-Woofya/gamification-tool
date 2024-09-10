import React from 'react';
import { Button, Typography, Container, Box, CircularProgress } from '@mui/material';
import { useNavigate } from 'react-router-dom';

function HomePage() {
    const navigate = useNavigate();

    const goToProfile = () => {
        navigate('/profile');  // Navigation
    };

    return (
        <Container>
            <Typography variant="h1" gutterBottom>
                Welcome to Woofya
            </Typography>
            <Typography variant="body1" paragraph>
                Enhance your dog's life with fun events and rewards!
            </Typography>
            <Button variant="contained" color="primary" onClick={goToProfile}>
                Go to Profile Page
            </Button>
        </Container>
    );
}

export default HomePage;