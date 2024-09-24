import {useEffect, useState} from "react";
import axios from "axios";
import Container from "react-bootstrap/Container";

export const HomePage = () => {
    const [message, setMessage] = useState('');

    // Get user from Web backend (needs better logic!)
    // Also checks if API user exists and posts if not
    useEffect(() => {

        // GET API USER
        function getApiUser() {
            const url = "http://localhost:8000/users/users/" + sessionStorage.getItem('uid') + '/';
            const headers = {
                'Content-Type': 'application/json',
                'Gamification-Api-Key': process.env.REACT_APP_API_KEY
            };
        
            axios.get(url, { headers })
                .then(response => {
                    console.log('User data posted:', response.data);
                    console.log("Response status: ", response.status);
                    if (response.status !== 200){
                        postApiUser();
                        console.log("Created new API user with username", sessionStorage.getItem('username'));
                    }
                })
                .catch(error => {
                    console.error('Error getting user data:', error);
                });
        }
    
        // POST API USER IF DOESN"T EXIST
        function postApiUser() {
            const url = "http://localhost:8000/users/users/";
            const data = {'username': sessionStorage.getItem('username')};
            const headers = {
                'Content-Type': 'application/json',
                'Gamification-Api-Key': process.env.REACT_APP_API_KEY
            }
        
            axios.post(url, data, { headers })
                .then(response => {
                    console.log('User data posted:', response.data);
                })
                .catch(error => {
                    console.error('Error posting user data:', error);
                });
        }

        if(localStorage.getItem('access_token') === null){
            window.location.href = '/login'  
        }
        else{
            (async () => {
            try {
                const url = 'http://localhost:8080/users/users/username/' + sessionStorage.getItem('username') + '/';
                console.log(url);
                const {data} = await axios.get(url, {
                headers: {
                  'Authorization': 'Bearer ' + localStorage.getItem('access_token'),  
                  'Content-Type': 'application/json',
                }
              });
              sessionStorage.setItem('uid',data.id);
              console.log(data.id);
              setMessage(data.username);

              // Call functions to get and post API user if not exists
              getApiUser();
            } catch (e) {
                console.log(e,'not auth')
            }
        })()};
    }, []); 

    return (
        <Container className="justify-content-md-center">
            <div className="form-signin mt-5 text-center">
                <h1>Hi {message}. Welcome to Woofya.</h1>
                <p>Enhance your dog's life with fun events and rewards!</p>
            </div>
        </Container>
    )
}
