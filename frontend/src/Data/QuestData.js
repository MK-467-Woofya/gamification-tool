const mockData = {
    users: [
      {
        id: 1,
        username: "user1",
        quests: [
          {
            questId: 101,
            title: "Walk 10km in July",
            goal: 10,
            progress: 3.3
          },
          {
            questId: 102,
            title: "Walk 2 times this week",
            goal: 2,
            progress: 1
          },
          {
            questId: 103,
            title: "Visit 5 different parks",
            goal: 5,
            progress: 1
          }
        ]
      },
      {
        id: 2,
        username: "user2",
        quests: [
          {
            questId: 101,
            title: "Walk 10km in July",
            goal: 10,
            progress: 7
          },
          {
            questId: 102,
            title: "Walk 2 times this week",
            goal: 2,
            progress: 2
          }
        ]
      },
      {
        id: 3,
        username: "user3",
        quests: [
          {
            questId: 101,
            title: "Walk 10km in July",
            goal: 10,
            progress: 9.5
          },
          {
            questId: 103,
            title: "Visit 5 different parks",
            goal: 5,
            progress: 3
          },
          {
            questId: 104,
            title: "Complete 3 training sessions",
            goal: 3,
            progress: 2
          }
        ]
      }
    ]
  };

  // Function to set the logged-in user
function setLoggedInUser(username) {
  localStorage.setItem('loggedInUser', username);
}

// Function to get the logged-in user
function getLoggedInUser() {
  return localStorage.getItem('loggedInUser');
}

export { mockData, setLoggedInUser, getLoggedInUser };
localStorage.setItem('mockData', JSON.stringify(mockData));