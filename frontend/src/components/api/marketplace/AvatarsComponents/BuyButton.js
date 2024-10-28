import axios from "axios";
import {useState, useEffect } from "react";

/**
 * Button component for buying Avatars.
 * This component handles the request to buy the Item
 */
export const BuyButton = ({ user, avatar, setUser}) => {
    const [isAvatarOwned, setIsAvatarOwned] = useState(false);
    const uid = sessionStorage.getItem('uid');

    /** Initial state for whether or not a User owns the Avatar */
    useEffect(() => {
        if (avatar.users.includes(parseInt(uid,10))){
            setIsAvatarOwned(true);
        } else {
            setIsAvatarOwned(false);
        }
    }, []);

    /** If owned, return message, else PUT request to the API */
    function handleClick() {
        if (isAvatarOwned){
            alert(`You already own ${avatar.name}.`);
        } else {
            let choice = window.confirm(`Purchase ${avatar.name}?`);
            if(choice){
                var url = process.env.REACT_APP_BASE_URL + `users/users/${user.id}/buy_avatar/`;
                var headers = {
                    'Content-Type': 'application/json',
                    'Gamification-Api-Key': process.env.REACT_APP_API_KEY
                };
                // Avatar ID required for request
                const data = {
                    'avatar_id': avatar.id,
                };
                // PUT request and update state of User mirrorring the values returned from the API
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
                        setIsAvatarOwned(true);
                    }
                })
                .catch(error => {
                    console.error('Error buying Avatar:', error);
                });
            }
        }
    }
    // Button visibility based on whether User owns Item
    return (
        <>
            {(isAvatarOwned) ? <p>Already owned</p>
            : <button onClick={handleClick}>{avatar.cost} Points</button> }
        </>
    )
}