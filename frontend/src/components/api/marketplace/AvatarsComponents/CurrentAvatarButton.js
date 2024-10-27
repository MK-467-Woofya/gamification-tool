import axios from "axios";
import {useState, useEffect } from "react";

/**
 * Button component for selecting current Avatar
 * Not currently functional due to incomplete backend
 */
export const CurrentAvatarButton = ({ user, avatar, setUser}) => {
    const [isCurrentAvatar, setIsCurrentAvatar] = useState(false);

    /** Initial state for whether or not an Avatar is the current one */
    useEffect(() => {
        if (user.current_avatar.id == avatar.id){
            setIsCurrentAvatar(true);
        } else {
            setIsCurrentAvatar(false);
        }
    }, []);

    /** If current, return message otherwise PUT request to the API */
    function handleClick() {
        if (isCurrentAvatar){
            alert(`${avatar.text} is already your current avatar.`);
        } else {
            let choice = window.confirm(`Set ${avatar.name} as your displayed Avatar?`);
            if(choice){
                var url = process.env.REACT_APP_BASE_URL + `users/users/${user.id}/current_avatar/`;
                var headers = {
                    'Content-Type': 'application/json',
                    'Gamification-Api-Key': process.env.REACT_APP_API_KEY
                };
                // Request data
                const data = {
                    'avatar_id': avatar.id,
                };
                // PUT request to update the current Avatar
                // Returns response.data.message if already current
                axios.put(url, data, { headers })
                .then(response => {
                    if(response.data.message){
                        alert(response.data.message);
                    } else {
                        setUser(prevUser => ({
                            ...prevUser,
                            current_avatar: response.data.current_avatar
                        }));
                        console.log("USER: ", user);
                        console.log("AVATAR: ", avatar);
                        setIsCurrentAvatar(true);
                    }
                })
                .catch(error => {
                    console.error('Error adding points:', error);
                });
            }
        }
    }
    // Button visibility based on whether Item is the current Avatar
    return (
        <>
            {(isCurrentAvatar) ? <p>This is your current avatar</p>
            : <button onClick={handleClick}>Set as current Avatar</button> }
        </>
    )
}