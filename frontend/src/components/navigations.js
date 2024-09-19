import {Nav, Navbar} from 'react-bootstrap';
import React, { useState, useEffect} from 'react';

/**
 * Navigation bar component. Includes all main routes
 * 
 */
export function Navigation() {
  const [isAuth, setIsAuth] = useState(false);

  useEffect(() => {
    if (localStorage.getItem('access_token') !== null) {
      setIsAuth(true);
    }
  }, [isAuth]);

  //Navbar, Nav, Link all have react-bootstrap styling
  return (
    <div>
    <Navbar bg="dark" variant="dark">
          <Navbar.Brand href="/">Woofya</Navbar.Brand>
          <Nav className="me-auto">
          {isAuth ?
            <Nav.Link href="/">Home</Nav.Link>
            : null}
          {isAuth ?
            <Nav.Link href="/profile">Profile</Nav.Link>
            : null}
          {isAuth ?
            <Nav.Link href="/leaderboard">Leaderboard</Nav.Link>
            : null}
          {isAuth ?
            <Nav.Link href="/locations">Locations</Nav.Link>
            : null}
          {isAuth ?
            <Nav.Link href="/quests">Quests</Nav.Link>
            : null}
          {isAuth ?
            <Nav.Link href="/marketplace">Marketplace</Nav.Link>
            : null}
          </Nav>
          <Nav>
          {isAuth ?
            <Nav.Link href="/logout">Logout</Nav.Link>:
            <Nav.Link href="/login">Login</Nav.Link>
          }
          </Nav>
      </Navbar>
      </div>
  );
}