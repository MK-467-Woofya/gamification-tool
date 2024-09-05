import React from 'react';
import { useNavigate } from 'react-router-dom';

function HomePage() {
    const navigate = useNavigate();

    const goToProfile = () => {
        navigate('/profile');
    };

    const goToLeaderboard = () => {
        navigate('/leaderboard');
    };

    return (
        <div>
            <h1>Welcome to the Home Page</h1>
            <p>This is the homepage of your React app.</p>
            <button onClick={goToProfile}>Go to Profile Page</button>
            <button onClick={goToLeaderboard}>Go to Leaderboard</button> {/* leaderboard button */}
        </div>
    );
}

export default HomePage;

