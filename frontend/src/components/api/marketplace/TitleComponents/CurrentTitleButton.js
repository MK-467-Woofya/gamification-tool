import axios from "axios";
import {useState, useEffect } from "react";

/**
 * Button component for selecting current Title
 * Not currently functional due to incomplete backend
 */
export const CurrentTitleButton = ({ user, title, setUser }) => {
    const [isCurrentTitle, setIsCurrentTitle] = useState(false);

    /** Initial state for whether or not a Title is the current one */
    useEffect(() => {
        if (user.current_title == title.id){
            setIsCurrentTitle(true);
        } else {
            setIsCurrentTitle(false);
        }
    }, []);

    /** If current, return message otherwise PUT request to the API */
    function handleClick() {
        if (isCurrentTitle){
            alert(`${title.text} is already your current title.`);
        } else {
            let choice = window.confirm(`Set ${title.name} as your displayed Title?`);
            if(choice){
                var url = process.env.REACT_APP_BASE_URL + `users/users/${user.id}/current_title/`;
                var headers = {
                    'Content-Type': 'application/json',
                    'Gamification-Api-Key': process.env.REACT_APP_API_KEY
                };
                // Request data
                const data = {
                    'title_id': title.id,
                };
                // PUT request to update the current Title
                // Returns response.data.message if already current
                axios.put(url, data, { headers })
                .then(response => {
                    if(response.data.message){
                        alert(response.data.message);
                    } else {
                        setUser(prevUser => ({
                            ...prevUser,
                            current_title: response.data.current_title
                        }));
                        console.log("USER: ", user);
                        console.log("TITLE: ", title);
                        setIsCurrentTitle(true);
                    }
                })
                .catch(error => {
                    console.error('Error adding points:', error);
                });
            }
        }
    }
    // Button visibility based on whether Item is the current Title
    return (
        <>
            {(isCurrentTitle) ? <p>This is your current title</p>
            : <button onClick={handleClick}>Set as current Title</button> }
        </>
    )
}