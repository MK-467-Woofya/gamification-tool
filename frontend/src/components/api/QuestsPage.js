import React, { useEffect, useState } from 'react';
import Quest from './Quest';
import axios from 'axios';

const API_KEY = process.env.REACT_APP_API_KEY;
const BASE_URL = process.env.REACT_APP_BASE_URL;

export const QuestsPage = () => {
  const [quests, setQuests] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const userId = sessionStorage.getItem('uid');
    
    const fetchQuests = async () => {
      try {
        const response = await axios.get(`${BASE_URL}quests/user-progress/`, {
          params: { user_id: userId },
          headers: {
            'Gamification-Api-Key': API_KEY
          }
        });
        setQuests(response.data.results);
      } catch (err) {
        console.error('Error fetching quest data:', err);
        setError('Could not fetch quest data. Please try again later.');
      }
    };

    fetchQuests();
  }, []);

  const handleUpdateProgress = async (questId, newProgress) => {
    try {
      // Find the UserQuestProgress entry by its quest ID
      const userQuestProgress = quests.find(q => q.quest.id === questId);
      
      if (!userQuestProgress) return;

      await axios.patch(`${BASE_URL}quests/user-progress/${userQuestProgress.id}/`, 
        { progress: newProgress },
        {
          headers: {
            'Gamification-Api-Key': API_KEY
          }
        }
      );

      // Update the local state with the new progress value
      setQuests(quests.map(q => 
        q.quest.id === questId ? { ...q, progress: newProgress } : q
      ));
    } catch (error) {
      console.error('Error updating quest progress:', error);
      setError('Failed to update progress.');
    }
  };

  return (
    <div>
      <h1>Quests</h1>
      {error && <p>{error}</p>}
      {quests.length > 0 ? (
        quests.map(questProgress => (
          <Quest
            key={questProgress.id}
            quest={questProgress.quest}
            progress={questProgress.progress}
            onUpdateProgress={handleUpdateProgress}
          />
        ))
      ) : (
        <p>No quests available</p>
      )}
    </div>
  );
};