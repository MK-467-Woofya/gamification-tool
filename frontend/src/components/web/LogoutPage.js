import {useEffect} from "react";
import Container from 'react-bootstrap/Container';

/**
 * Logout view
 * Clears session and local storage
 */
export const LogoutPage = () => {
    const delay = ms => new Promise(res => setTimeout(res,ms));
    useEffect(() => {
        (async () => {
            try {
                console.log('Logging user out')
                // Clear current user
                sessionStorage.clear();
                // wait 3 seconds before redirecting
                await delay(2000);
                window.location.href = '/login'
            } catch (e) {
        console.log('logout failed')
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