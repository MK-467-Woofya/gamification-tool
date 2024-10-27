
import axios from "axios";
import {useState, useEffect } from "react";

/**
 * Button component for refunding Avatars.
 * This component handles the request to refund the Item
 */
export const RefundButton = ({ user, avatar, setUser }) => {
    const [isAvatarOwned, setIsAvatarOwned] = useState(false);
    const uid = sessionStorage.getItem('uid');

    /** Initial state for whether or not a User owns the Avatar */
    useEffect(() => {
        if (avatar.users.includes(parseInt(uid,10))){
            setIsAvatarOwned(true);
        }
    }, []);

    /** If owned, return message, else PUT request to the API */
    function handleClick() {
        if (!isAvatarOwned){
            alert(`You don't own ${avatar.name}.`);
        } else {
            let choice = window.confirm(`Refund ${avatar.name}?`);
            if(choice){
                var url = process.env.REACT_APP_BASE_URL + `users/users/${user.id}/refund_avatar/`;
                var headers = {
                    'Content-Type': 'application/json',
                    'Gamification-Api-Key': process.env.REACT_APP_API_KEY
                };
                // Request data
                const data = {
                    'avatar_id': avatar.id,
                };
                // PUT request to remove Avatar and refund points
                axios.put(url, data, { headers })
                .then(response => {
                    if(response.data.message){
                        alert(response.data.message);
                    } else {
                        setUser(prevUser => ({
                            ...prevUser,
                            avatars: response.data.avatars,
                            shop_points: response.data.shop_points

                        }));
                        setIsAvatarOwned(false);
                    }
                })
                .catch(error => {
                    console.error('Error refunding Avatar:', error);
                });
            }
        }
    }
    // Conditional button based on state of isAvatarOwned
    return (
        <>
            { (isAvatarOwned) ? <button onClick={handleClick}>Refund</button>
            : <p>Avatar not owned</p> }
        </>
    )
}