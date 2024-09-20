import {useEffect, useState} from "react";
import axios from "axios";

export const HomePage = () => {
    const [message, setMessage] = useState('');
    const username = sessionStorage.getItem('username');

    // Get user from Web backend (needs better logic!)
    useEffect(() => {
        if(localStorage.getItem('access_token') === null){
            window.location.href = '/login'  
        }
        else{
            (async () => {
            try {
                const url = 'localhost:8080/users/users/username/' + username;
                const {data} = await axios.get(url, {
                headers: {
                  'Authorization': 'Bearer ' + localStorage.getItem('access_token'),  
                  'Content-Type': 'application/json',
                }
              });

              setMessage(data.username);
            } catch (e) {
                console.log('not auth')
            }
        })()};
    }, []); 
    

    // Post user to API by username. Post fails if already in database (needs better logic!)
    useEffect(() => {
        const url = "http://localhost:8000/api/users/";

        const data = {'username': username}

        const headers = {
            'Content-Type': 'application/json',
            'Gamification-Api-Key': process.env.REACT_APP_API_KEY
        };

        axios.post(url, data, { headers })

            .then(response => {
                console.log('User data posted:', response.data);
            })
            .catch(error => {
                console.error('Error posting user data:', error);
            });
    }, []);

    return <div className="form-signin mt-5 text-center">
        <h3>Hi {username}</h3>
        
    </div>
}
