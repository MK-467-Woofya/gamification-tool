import axios from 'axios';

// Helper function to get user ID or create a new user if they don't exist
export function getUserIdFromSessionOrPostUser() {
    return new Promise((resolve, reject) => {
        const uid = sessionStorage.getItem('uid');

        // If uid already exists in session storage, resolve immediately
        if (uid) {
            resolve(uid);
            return;
        }

        // Otherwise, fetch all users and post the current user if they don't exist
        const baseUrl = process.env.REACT_APP_BASE_URL + 'users/users/';
        axios.get(baseUrl, {
            headers: {
                'Content-Type': 'application/json',
                'Gamification-Api-Key': process.env.REACT_APP_API_KEY
            }
        })
        .then(response => {
            const users = response.data;
            const currentUsername = sessionStorage.getItem('username');

            // Check if user exists
            let user = users.find(user => user.username === currentUsername);
            if (user) {
                sessionStorage.setItem('uid', user.id);
                resolve(user.id);
            } else {
                // Post user if it doesn't exist
                const newUser = {
                    'username': currentUsername,
                    'titles': [],
                    'avatars': [],
                };

                axios.post(baseUrl, newUser, {
                    headers: {
                        'Content-Type': 'application/json',
                        'Gamification-Api-Key': process.env.REACT_APP_API_KEY
                    }
                })
                .then(response => {
                    sessionStorage.setItem('uid', response.data.id);
                    resolve(response.data.id);
                })
                .catch(postError => {
                    console.error('Error posting user:', postError);
                    reject(postError);
                });
            }
        })
        .catch(fetchError => {
            console.error('Error fetching users:', fetchError);
            reject(fetchError);
        });
    });
}