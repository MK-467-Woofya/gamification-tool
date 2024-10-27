import axios from "axios";
import {useState, useEffect } from "react";
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

import { ShopTitleList } from "./TitleComponents/ShopTitleList";

/**
 * Shop view for Titles
 * Users can see the list of Titles, descriptions, costs, etc.
 * Users can buy a Title for their profile
 */
export const TitlesPage = () => {
    
    const [titles, setTitles] = useState(null);
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

        /** GET Titles list from API and store state */
        useEffect(() => {
            console.log('Fetching titles data...');
            const titles_url = process.env.REACT_APP_BASE_URL + "marketplace/titles/";
            const headers = {
                'Content-Type': 'application/json',
                'Gamification-Api-Key': process.env.REACT_APP_API_KEY
            };
            axios.get(titles_url, { headers })
                .then(response => {
                    console.log('Titles fetched:', response.data);
                    setTitles(response.data);
                })
                .catch(error => {
                    console.error('Error fetching titles data:', error);
                });
            }, []);

    // Load before requests return
    if (!titles || !user) {
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
                    <ShopTitleList user={user} titles={titles} setUser={setUser}/>
                </Col>
            </Row>
        </Container>
    );
}
