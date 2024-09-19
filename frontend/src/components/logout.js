import {useEffect} from "react";
import axios from "axios";

/**
 * Logout component
 * Clears authorization, session and local storage
 */
export const LogoutPage = () => {

    const delay = ms => new Promise(res => setTimeout(res,ms));

    useEffect(() => {
        (async () => {
            try {
                const {data} = await axios.post('http://localhost:8080/logout/',{
                    refresh_token:localStorage.getItem('refresh_token')
                } ,{headers: {
                    'Content-Type': 'application/json'
                }}, {withCredentials: true});

                console.log('logout', data)
                localStorage.clear();
                sessionStorage.clear();
                axios.defaults.headers.common['Authorization'] = null;

                // wait 5 seconds before redirecting
                await delay(5000);

                window.location.href = '/login'
            } catch (e) {
                console.log('logout not working')
            }
        })();
    }, []);

    return (
    <div className="form-signin mt-5 text-center">
        <h3>You have successfully logged out. You will be redirected to the login page. </h3>
        
    </div>
    )
}