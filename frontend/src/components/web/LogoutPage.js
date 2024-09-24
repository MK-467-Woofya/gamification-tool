import {useEffect} from "react";
import axios from "axios";
import Container from 'react-bootstrap/Container';

/**
 * Logout view
 * Clears authorization, session and local storage
 */
export const LogoutPage = () => {

    const delay = ms => new Promise(res => setTimeout(res,ms));

    useEffect(() => {
        (async () => {
            try {
                const {data} = await axios.post('http://localhost:8080/users/logout/',{
                    refresh_token:localStorage.getItem('refresh_token')
                } ,{headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
                }}, {withCredentials: true});

                console.log('Logging user out', data)
                localStorage.clear();
                sessionStorage.clear();
                axios.defaults.headers.common['Authorization'] = null;

                // wait 3 seconds before redirecting
                await delay(3000);

                window.location.href = '/login'
            } catch (e) {
                console.log('logout not working')
            }
        })();
    }, []);

    return (
        <Container className="justify-content-md-center">
            <div className="form-signin mt-5 text-center">
                <h3>You have successfully logged out. You will be redirected to the login page. </h3>
                
            </div>
        </Container>
    )
}