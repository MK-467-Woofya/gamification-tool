import React, { useState } from 'react';
import axios from 'axios';

const API_KEY = process.env.REACT_APP_API_KEY;
const BASE_URL = process.env.REACT_APP_BASE_URL;

const Quest = ({ quest, progress, onUpdateProgress }) => {
  const [newProgress, setNewProgress] = useState(progress);

  const handleProgressChange = (e) => {
    setNewProgress(e.target.value);
  };

  const updateProgress = async () => {
    try {
      // Call the update function passed from the parent component
      await onUpdateProgress(quest.id, newProgress);
    } catch (error) {
      console.error('Failed to update progress:', error);
    }
  };

  return (
    <div style={{ margin: '20px', padding: '10px', border: '1px solid #ccc' }}>
      <h2>{quest.title}</h2>
      <p>Goal: {quest.goal} km</p>
      <p>Current Progress: {progress} km</p>
      <progress value={progress} max={quest.goal}></progress>
      <div style={{ marginTop: '10px' }}>
        <input
          type="number"
          value={newProgress}
          onChange={handleProgressChange}
          placeholder="Update progress"
        />
        <button onClick={updateProgress}>Update Progress</button>
      </div>
    </div>
  );
};

export default Quest;