import axios from "axios";
import {useState, useEffect } from "react";
import Container from 'react-bootstrap/Container';

/**
 * View to see all available Titles
 * 
 */
export const TitlesPage = () => {
    
    const [titles, setTitles] = useState(null);

    useEffect(() => {
        console.log('Fetching title data...'); // useEffect

        const url = "http://localhost:8000/marketplace/titles/";

        const headers = {
            'Content-Type': 'application/json',
            'Gamification-Api-Key': process.env.REACT_APP_API_KEY
        };

        axios.get(url, { headers })

            .then(response => {
                console.log('Titles fetched:', response.data); // data grab
                setTitles(response.data.results);
            })
            .catch(error => {
                console.error('Error fetching title data:', error);
            });
    }, []);
    
    

    if (!titles) { // return this while loading
        return <div>Loading...</div>;
    }

    return (
        <Container className="justify-content-md-center">
            <div>
                <h1>Titles</h1>
            </div>
            <div>
                <table>
                    <thead>
                        <tr>
                            <th>Title name</th>
                            <th>Title text</th>
                            <th>Cost</th>
                        </tr>
                    </thead>
                    <tbody>
                        {Array.isArray(titles) && titles.map((title, index) => (
                            <tr key={index}>
                                <td>{title.name}</td>
                                <td>{title.text}</td>
                                <td>{title.cost}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </Container>
    );
}