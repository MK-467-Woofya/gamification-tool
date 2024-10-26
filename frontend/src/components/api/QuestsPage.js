import React, { useEffect, useState } from 'react';
import Quest from './Quest';
import axios from 'axios';

// Load environment variables
const API_KEY = process.env.REACT_APP_API_KEY;
const BASE_URL = process.env.REACT_APP_BASE_URL;

export const QuestsPage = () => {
  const [quests, setQuests] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Get the current logged-in user ID from sessionStorage
    const userId = sessionStorage.getItem('uid');
    
    // Fetch user quest progress from the backend
    const fetchQuests = async () => {
      try {
        const response = await axios.get(`${BASE_URL}quests/user-progress/`, {
          params: { user_id: userId },
          headers: {
            'Gamification-Api-Key': API_KEY
          }
        });
        // Update the state with the fetched quest progress data
        setQuests(response.data.results);
      } catch (err) {
        console.error('Error fetching quest data:', err);
        setError('Could not fetch quest data. Please try again later.');
      }
    };

    fetchQuests();
  }, []);

  return (
    <div>
      <h1>Quests</h1>
      {error && <p>{error}</p>}
      {quests.length > 0 ? (
        quests.map(questProgress => (
          <Quest key={questProgress.id} quest={questProgress.quest} progress={questProgress.progress} />
        ))
      ) : (
        <p>No quests available</p>
      )}
    </div>
  );
};