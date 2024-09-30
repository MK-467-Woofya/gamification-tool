import React, { useEffect, useState } from 'react';
import { mockData, setLoggedInUser, getLoggedInUser } from '../Data/QuestData'; // Adjust the path as necessary
import Quest from './Quest';

const QuestPage = () => {
  const [quests, setQuests] = useState([]);

  setLoggedInUser('user3');

  useEffect(() => {
    const loggedInUser = getLoggedInUser();
    const userQuests = mockData.users.find(user => user.username === loggedInUser)?.quests;
    if (userQuests) {
      setQuests(userQuests);
    }
  }, []);

  return (
    <div>
      <h1>Quests</h1>
      {quests.map(quest => (
        <Quest key={quest.questId} quest={quest} />
      ))}
    </div>
  );
};

export default QuestPage;