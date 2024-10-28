import {useState} from "react";
/**
 * Login view
 * Renders login form and sets username
 * Username can be any value, as the User will either be retrieved or created
 */
export const LoginPage = () => {
    const [username, setUsername] = useState('');

    // If current user, redirect to homepage
    if(sessionStorage.getItem('username') != null){
        window.location.href = '/'  
    }
    // Set username on submit
    const submit = async e => {
        e.preventDefault();
        // Clear current user before signing in
        sessionStorage.clear();
        // Web backend username stored for API user get request
        sessionStorage.setItem('username', username);
        window.location.href = '/';
    }
    // username field
    return(
        <div className="Auth-form-container col-md-4">
            <form className="Auth-form" onSubmit={submit}>
                <div className="Auth-form-content">
                    <h3 className="Auth-form-title">Sign In</h3>
                    <div className="form-group mt-3">
                        <label>Username</label>
                        <input
                            className="form-control mt-1"
                            placeholder="Enter Username"
                            name='username'
                            type='text'
                            value={username}
                            required
                            onChange={e => setUsername(e.target.value)}
                        />
                    </div>
                    <div className="d-grid gap-2 mt-3">
                        <button type="submit" className="btn btn-primary">
                            Submit
                        </button>
                    </div>
                </div>
            </form>
        </div>
    )
}