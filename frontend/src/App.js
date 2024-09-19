import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import {Navigation} from './components/navigations';
import {HomePage} from './components/HomePage';
import ProfilePage from './components/ProfilePage';
import {Quests} from './components/Quests';
import {LoginPage} from './components/LoginPage';
import {LogoutPage} from './components/logout';


function App() {
    return (
        <div className="App">
            <Router>
                <Navigation></Navigation>
                <Routes>
                    <Route path="/" element={<HomePage />} />
                    <Route path="/login" element={<LoginPage />} />
                    <Route path="/profile" element={<ProfilePage />} />
                    <Route path="/quests" element={<Quests />} />
                    <Route path="/logout" element={<LogoutPage />} />
                </Routes>
            </Router>
        </div>
    );
}

export default App;


