import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { NavigationBar } from './components/ui/NavigationBar';
import { HomePage } from './components/web/HomePage';
import { LoginPage } from './components/web/LoginPage';
import { LogoutPage } from './components/web/LogoutPage';
import { LocationsPage } from './components/api/LocationsPage';
import { EventsPage } from './components/api/EventsPage';
import { ProfilePage } from './components/api/ProfilePage';
import { CheckInsPage } from './components/api/CheckInsPage';
import { QuestsPage } from './components/api/QuestsPage';
import { LeaderboardPage } from './components/api/LeaderboardPage';
import { MarketplacePage } from './components/api/MarketplacePage';

import { Quiz } from './components/api/Quiz';



function App() {
    return (
        <div className="App">
            <Router>
                <NavigationBar></NavigationBar>
                <Routes>
                    <Route path="/" element={<HomePage />} />
                    <Route path="/login" element={<LoginPage />} />
                    <Route path="/user/profile" element={<ProfilePage />} />
                    <Route path="/locations" element={<LocationsPage />} />
                    <Route path="/events" element={<EventsPage />} />
                    <Route path="/user/checkins" element={<CheckInsPage />} />
                    <Route path="/user/quests" element={<QuestsPage />} />
                    <Route path="/user/leaderboard/" element={<LeaderboardPage />} />                    
                    <Route path="/user/marketplace" element={<MarketplacePage />} />
                    <Route path="/logout" element={<LogoutPage />} />

                    <Route path="/quiz" element={<Quiz />} />
                </Routes>
            </Router>
        </div>
    );
}

export default App;


