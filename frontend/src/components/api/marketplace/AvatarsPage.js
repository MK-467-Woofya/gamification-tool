import axios from "axios";
import {useState, useEffect } from "react";
import Container from 'react-bootstrap/Container';

/**
 * View to see all available Avatars
 * 
 */
export const AvatarsPage = () => {
    
    const [avatars, setAvatars] = useState(null);

    useEffect(() => {
        console.log('Fetching avatars data...'); // useEffect

        const url = "http://localhost:8000/marketplace/avatars/";

        const headers = {
            'Content-Type': 'application/json',
            'Gamification-Api-Key': process.env.REACT_APP_API_KEY
        };

        axios.get(url, { headers })

            .then(response => {
                console.log('Avatars fetched:', response.data); // data grab
                setAvatars(response.data.results);
            })
            .catch(error => {
                console.error('Error fetching avatars data:', error);
            });
    }, []);
    
    

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
                            <th>Cost</th>
                        </tr>
                    </thead>
                    <tbody>
                        {Array.isArray(avatars) && avatars.map((avatar, index) => (
                            <tr key={index}>
                                <td>{avatar.name}</td>
                                <td>{avatar.img_url}</td>
                                <td><img src={avatar.img_url} alt={avatar.name}/></td>
                                <td>{avatar.cost}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </Container>
    );

}