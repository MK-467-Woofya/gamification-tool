
import axios from "axios";
import {useState, useEffect } from "react";

/**
 * Button component for refunding Titles.
 * This component handles the request to refund the Item
 */
export const RefundButton = ({ user, title, setUser }) => {
    const [isTitleOwned, setIsTitleOwned] = useState(false);
    const uid = sessionStorage.getItem('uid');

    /** Initial state for whether or not a User owns the Avatar */
    useEffect(() => {
        if (title.users.includes(parseInt(uid,10))){
            setIsTitleOwned(true);
        }
    }, []);

    /** If owned, return message, else PUT request to the API */
    function handleClick() {
        if (!isTitleOwned){
            alert(`You don't own ${title.name}.`);
        } else {
            let choice = window.confirm(`Refund ${title.name}?`);
            if(choice){
                var url = process.env.REACT_APP_BASE_URL + `users/users/${user.id}/refund_title/`;
                var headers = {
                    'Content-Type': 'application/json',
                    'Gamification-Api-Key': process.env.REACT_APP_API_KEY
                };
                // Request Data
                const data = {
                    'title_id': title.id,
                };
                // PUT request to remove Avatar and refund points
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
                        setIsTitleOwned(false);
                    }
                })
                .catch(error => {
                    console.error('Error refunding Title:', error);
                });
            }
        }
    }
    // Conditional button based on state of isTitleOwned
    return (
        <>
            { (isTitleOwned) ? <button onClick={handleClick}>Refund</button>
            : <p>Title not owned</p> }
        </>
    )
}