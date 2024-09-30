import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { NavigationBar } from './components/ui/NavigationBar';
import { HomePage } from './components/web/HomePage';
import { LoginPage } from './components/web/LoginPage';
import { LogoutPage } from './components/web/LogoutPage';
import { LocationsPage } from './components/web/LocationsPage';
import { EventsPage } from './components/web/EventsPage';
import { ProfilePage } from './components/api/ProfilePage';
import { CheckInsPage } from './components/api/CheckInsPage';
import { QuestsPage } from './components/api/QuestsPage';
import { LeaderboardPage } from './components/api/LeaderboardPage';
import { MarketplacePage } from './components/api/MarketplacePage';



function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/profile" element={<ProfilePage />} />
                <Route path="/leaderboard" element={<LeaderboardPage />} />  {/* leaderboard */}
            </Routes>
        </Router>
    );
}

export default App;


