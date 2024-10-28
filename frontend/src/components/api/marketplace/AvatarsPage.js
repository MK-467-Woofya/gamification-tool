import axios from "axios";
import {useState, useEffect } from "react";
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

import { ShopAvatarList } from "./AvatarsComponents/ShopAvatarList";

/**
 * Shop view for Avatars
 * Users can see the list of Avatars, descriptions, costs, etc.
 * Users can buy an Avatar for their profile
 */
export const AvatarsPage = () => {
    
    const [avatars, setAvatars] = useState(null);
    const [user, setUser] = useState(null);
    const uid = sessionStorage.getItem('uid');

    /** GET User from API and store user state */
    useEffect(() => {
        const headers = {
            'Content-Type': 'application/json',
            'Gamification-Api-Key': process.env.REACT_APP_API_KEY
        };
        const user_url = process.env.REACT_APP_BASE_URL + "users/users/";
        axios.get(user_url + uid + '/', { headers })
            .then(response => {
                console.log('User data fetched:', response.data);
                setUser(response.data);
            })
            .catch(error => {
                console.error('Error fetching user data:', error);
            });
        }, []);

        /** GET Avatars list from API and store state */
        useEffect(() => {
            const avatars_url = process.env.REACT_APP_BASE_URL + "marketplace/avatars/";
            const headers = {
                'Content-Type': 'application/json',
                'Gamification-Api-Key': process.env.REACT_APP_API_KEY
            };
            axios.get(avatars_url, { headers })
                .then(response => {
                    console.log('Avatars:', response.data);
                    setAvatars(response.data);
                })
                .catch(error => {
                    console.error('Error fetching avatars data:', error);
                });
            }, []);
            
    // Load before requests return
    if (!avatars || !user) {
        return <div>Loading...</div>;
    }
    
    return (
        <Container fluid>
            <Row>
                <Col>
                    <h5>User shop points: {user.shop_points}</h5>
                </Col>
            </Row>
            <Row>
                <Col>
                    <ShopAvatarList user={user} avatars={avatars} setUser={setUser}/>
                </Col>
            </Row>
        </Container>
    );
}
