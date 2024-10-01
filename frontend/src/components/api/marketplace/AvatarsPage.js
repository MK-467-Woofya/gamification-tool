import axios from "axios";
import {useState, useEffect } from "react";
import Container from 'react-bootstrap/Container';

/**
 * View to see all available Avatars
 * 
 */
export const AvatarsPage = () => {
    
    const [avatars, setAvatars] = useState(null);
    const [user, setUser] = useState(null)

    const uid = sessionStorage.getItem('uid');


    useEffect(() => {
        console.log('Fetching avatars data...'); // useEffect

        const avatars_url = "http://localhost:8000/marketplace/avatars/";

        const headers = {
            'Content-Type': 'application/json',
            'Gamification-Api-Key': process.env.REACT_APP_API_KEY
        };

        axios.get(avatars_url, { headers })

            .then(response => {
                console.log('Avatars fetched:', response.data); // data grab
                setAvatars(response.data.results);
            })
            .catch(error => {
                console.error('Error fetching avatars data:', error);
            });
        
        const user_url = "http://localhost:8000/users/users/";

        axios.get(user_url + uid + '/', { headers })

            .then(response => {
                console.log('User data fetched:', response.data); // data grab
                setUser(response.data);
            })
            .catch(error => {
                console.error('Error fetching user data:', error);
            });
    }, []);

    /*useEffect(() => {
        const url = "http://localhost:8000/users/users/";
            const data = {
                'username': sessionStorage.getItem('username'),
                'avatars': []
            };
            const headers = {
                'Content-Type': 'application/json',
                'Gamification-Api-Key': process.env.REACT_APP_API_KEY
            }
        
            axios.put(url, data, { headers })
                .then(response => {
                    console.log('User data posted:', response.data);    
                })
                .catch(error => {
                    console.error('Error posting user data:', error);
                });

        
    }, []); */

    // If avatar is_listed and user doesn't already own
    function canBuy(avatar){
        var canPurchase = "Available";
        if(!avatar.is_listed){
            canPurchase = "Avatar is no longer available";
        }

        if(user.avatars){
            user.avatars.forEach(user_avatar => {
                if(user_avatar.id === avatar.id){
                    canPurchase = "Already owned";
                }
            });
        }
        
        console.log("USER Deets: ", user.avatars);

        return canPurchase;
    }

    
    

    if (!avatars) { // return this while loading
        return <div>Loading...</div>;
    }

    return (
        <Container className="justify-content-md-center">
            <div>
                <h1>Avatars</h1>
            </div>
            <div>
                <table>
                    <thead>
                        <tr>
                            <th>Avatar name</th>
                            <th>Avatar URL</th>
                            <th>Avatar image</th>
                            <th>Collaborator</th>
                            <th>Description</th>
                            <th>Cost</th>
                            <th>Is Listed?</th>
                            <th>Purchasable</th>
                            <th>Buy</th>
                        </tr>
                    </thead>
                    <tbody>
                        {Array.isArray(avatars) && avatars.map((avatar, index) => (
                            <tr key={index}>
                                <td>{avatar.name}</td>
                                <td>{avatar.img_url}</td>
                                <td><img src={avatar.img_url} alt={avatar.name} width={192} height={192}/></td>
                                <td>{avatar.partner}</td>
                                <td>{avatar.description}</td>
                                <td>{avatar.cost}</td>
                                <td>{avatar.is_listed.toString()}</td>
                                <td>
                                    {canBuy(avatar)}
                                </td>
                                <td>
                                {avatar.is_listed ? <button>Buy</button>
                                : <p>Not Available</p>}
                                </td>

                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </Container>
    );

}