import React, { useState } from 'react';

const Quest = ({ quest, progress, onUpdateProgress }) => {
  const [newProgress, setNewProgress] = useState(progress);

  const handleProgressChange = (e) => {
    setNewProgress(e.target.value);
  };

  const updateProgress = async () => {
    try {
      await onUpdateProgress(quest.id, newProgress);
    } catch (error) {
      console.error('Failed to update progress:', error);
    }
  };

  return (
    <div style={{ margin: '20px', padding: '10px', border: '1px solid #ccc' }}>
      <h2>{quest.title}</h2>
      <p>Reward: {quest.rewards} 🦴</p>
      <p>Current Progress: {progress} / {quest.goal}</p> {/* Flexible progress display */}
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