import {Nav, Navbar, Container, NavDropdown} from 'react-bootstrap';
import React, { useState, useEffect} from 'react';
import '../styles.css';


/**
 * Navigation bar component. Includes all main routes
 * 
 */
export const NavigationBar = () => {
    const [isAuth, setIsAuth] = useState(false);

    useEffect(() => {
        if (sessionStorage.getItem('username') !== null) {
            setIsAuth(true);
        }
    }, [isAuth]);

    //Navbar, Nav, Link all have react-bootstrap styling
    return (
        <div className='mb-5'>
        <Navbar expand ="lg" className="bg-body-tertiary">
            <Navbar.Brand href="/">Woofya</Navbar.Brand>
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav">
                <Nav className="me-auto">
                {isAuth ?
                    <Nav.Link href="/">Home</Nav.Link>
                    : null}
                {isAuth ?
                    <Nav.Link href="/locations">Locations</Nav.Link>
                    : null}
                {isAuth ?
                    <Nav.Link href="/events">Events</Nav.Link>
                    : null}
                {isAuth ?
                    <Nav.Link href="/leaderboard">Leaderboard</Nav.Link>
                    : null}
                {isAuth ?
                    <Nav.Link href="/quiz">Quiz</Nav.Link>
                : null}
                </Nav>
                <Nav>
                {isAuth ?
                    <Nav.Link href="/user/profile">Profile</Nav.Link>
                    : null}
                {isAuth ?
                    <Nav.Link href="/user/checkins">Check Ins</Nav.Link>
                    : null}
                {isAuth ?
                    <Nav.Link href="/user/quests">Quests</Nav.Link>
                    : null}
                {isAuth ?
                    <Nav.Link href="/marketplace">Marketplace</Nav.Link>
                    : null}
                {isAuth ?
                    <Nav.Link href="/logout">Logout</Nav.Link>:
                    <Nav.Link href="/login">Login</Nav.Link>
                }
                </Nav>
            </Navbar.Collapse>
        </Navbar>
        </div>
    );
}