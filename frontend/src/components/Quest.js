import React from 'react';

const Quest = ({ quest }) => {
  return (
    <div style={{ margin: '20px', padding: '10px', border: '1px solid #ccc' }}>
      <h2>{quest.title}</h2>
      <p>Goal: {quest.goal} km</p>
      <p>Progress: {quest.progress} km</p>
      <progress value={quest.progress} max={quest.goal}></progress>
    </div>
  );
};

export default Quest;