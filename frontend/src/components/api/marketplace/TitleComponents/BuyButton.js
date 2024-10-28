import axios from "axios";
import {useState, useEffect } from "react";

/**
 * Button component for buying Titles.
 * This component handles the request to buy the Item
 */
export const BuyButton = ({ user, title, setUser}) => {
    const [isTitleOwned, setIsTitleOwned] = useState(false);
    const uid = sessionStorage.getItem('uid');

    /** Initial state for whether or not a User owns the Avatar */
    useEffect(() => {
        if (title.users.includes(parseInt(uid,10))){
            setIsTitleOwned(true);
        } else {
            setIsTitleOwned(false);
        }
    }, []);

    /** If owned, return message, else PUT request to the API */
    function handleClick() {
        if (isTitleOwned){
            alert(`You already own ${title.name}.`);
        } else {
            let choice = window.confirm(`Purchase ${title.name}?`);
            if(choice){
                var url = process.env.REACT_APP_BASE_URL + `users/users/${user.id}/buy_title/`;
                var headers = {
                    'Content-Type': 'application/json',
                    'Gamification-Api-Key': process.env.REACT_APP_API_KEY
                };
                // Request data
                const data = {
                    'title_id': title.id,
                };
                // PUT request and update state of User mirrorring the values returned from the API
                axios.put(url, data, { headers })
                .then(response => {
                    if(response.data.message){
                        alert(response.data.message);
                    } else {
                        setUser(prevUser => ({
                            ...prevUser,
                            titles: response.data.titles,
                            shop_points: response.data.shop_points
                        }));
                        console.log("USER: ", user);
                        console.log("TITLE: ", title);
                        setIsTitleOwned(true);
                    }
                })
                .catch(error => {
                    console.error('Error adding points:', error);
                });
            }
        }
    }
    // Button visibility based on whether User owns Item
    return (
        <>
            {(isTitleOwned) ? <p>Already owned</p>
            : <button onClick={handleClick}>{title.cost} Points</button> }
        </>
    )
}