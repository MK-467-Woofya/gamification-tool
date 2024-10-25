import {useEffect, useState} from "react";
import axios from "axios";
import Container from "react-bootstrap/Container";

export const HomePage = () => {

    const message = sessionStorage.getItem('username');

    const [users, setUsers] = useState([]);

    // Get all users from db
    useEffect(() => {
        axios.get(process.env.REACT_APP_BASE_URL + 'users/users/', {
            headers: {
                'Content-Type': 'application/json',
                'Gamification-Api-Key': process.env.REACT_APP_API_KEY
            }
            })
            .then(response => {
                console.log(response.data);
                setUsers(response.data);
            })
            .catch(error => {
                console.error('Error fetching users data:', error);
            });
    }, []);

    // Get or post current user data
    useEffect(() => {
        function postApiUser() {
            const url = process.env.REACT_APP_BASE_URL + 'users/users/';
            const data = {
                'username': sessionStorage.getItem('username'),
                'titles': [],
                'avatars': [],
            };
            const headers = {
                'Content-Type': 'application/json',
                'Gamification-Api-Key': process.env.REACT_APP_API_KEY
            }
        
            axios.post(url, data, { headers })
                .then(response => {
                    console.log('User data posted:', response.data);
                    sessionStorage.setItem('uid',response.data.id);
    
                })
                .catch(error => {
                    console.error('Error posting user data:', error);
                });
        }
        // Hacky way of waiting for state change of users, since initial users will be empty
        if(users.length > 0){
            var userExists = false;
            users.forEach(user => {
                if(user.username === sessionStorage.getItem('username')){
                    userExists = true;
                }

            });

            // Post if not exists
            if(!userExists){
                postApiUser();
                console.log("Posting user to API");
            }
            //Get current user id for requests
            else
            {
                const currentUser = users.filter(user => user.username === sessionStorage.getItem('username'));
                if(sessionStorage.getItem('uid') == null){
                    sessionStorage.setItem('uid',currentUser[0].id);
                }                      
            }
        }
    }, [users]);

    if (users.length == 0) { // return this while loading
        return <div>Loading...</div>;
    }
    
    return (
        <Container className="justify-content-md-center">
            <div className="form-signin text-center">
                <h1>Hi {message}. Welcome to Woofya.</h1>
                <p>Enhance your dog's life with fun events and rewards!</p>
            </div>
            <div className="text-center">
                <img src="img/homepage-img.jpg" alt="dog-and-owner-hero" className="img-fluid" />
            </div>
        </Container>
    )
}
