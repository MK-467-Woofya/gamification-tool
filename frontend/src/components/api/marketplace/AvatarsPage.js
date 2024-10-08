import axios from "axios";
import {useState, useEffect } from "react";
import Container from 'react-bootstrap/Container';

/**
 * View to see all available Avatars
 * 
 */
export const AvatarsPage = () => {
    
    const [avatars, setAvatars] = useState(null);
    const [user, setUser] = useState(null);

    const uid = sessionStorage.getItem('uid');


    useEffect(() => {
        console.log('Fetching avatars data...'); // useEffect

        const avatars_url = process.env.REACT_APP_BASE_URL + "marketplace/avatars/";

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
        
        const user_url = process.env.REACT_APP_BASE_URL + "users/users/";

        axios.get(user_url + uid + '/', { headers })

            .then(response => {
                console.log('User data fetched:', response.data); // data grab
                setUser(response.data);
            })
            .catch(error => {
                console.error('Error fetching user data:', error);
            });
        
        console.log(avatars);

        }, []);


    if (!avatars) { // return this while loading
        return <div>Loading...</div>;
    }

    return (
        <Container className="justify-content-md-center">
            <div>
                <h1>Avatars</h1>
            </div>
            <div className="table-responsive">
                <table>
                    <thead>
                        <tr>
                            <th>Avatar name</th>
                            <th>Avatar image</th>
                            <th>Collaborator</th>
                            <th>Description</th>
                            <th>Cost</th>
                            <th>Is Listed?</th>
                            <th>Already owned</th>
                            <th>Buy</th>
                        </tr>
                    </thead>
                    <tbody>
                        {Array.isArray(avatars) && avatars.map((avatar, index) => (
                            <tr key={index}>
                                <td>{avatar.name}</td>
                                <td><img src={avatar.img_url} alt={avatar.name} width={192} height={192}/></td>
                                <td>{avatar.partner}</td>
                                <td>{avatar.description}</td>
                                <td>{avatar.cost}</td>
                                <td>{avatar.is_listed.toString()}</td>
                                <td>{(avatar.users.includes(parseInt(uid,10))) ? <p>Already owned</p>
                                    : <p>Not owned</p> }
                                </td>
                                <td>
                                    {avatar.is_listed ? <button>Buy</button>
                                    : <p>Not available</p> }
                                </td>

                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </Container>
    );

}