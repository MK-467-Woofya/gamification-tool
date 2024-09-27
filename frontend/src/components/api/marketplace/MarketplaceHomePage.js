import axios from "axios";
import {useState, useEffect } from "react";
import Container from 'react-bootstrap/Container';

/**
 * Marketplace for shop functionality
 * 
 */
export const MarketplaceHomePage = () => {
   
    return (
        <Container className="justify-content-md-center">
            <h1>Marketplace items</h1>
            <section>
                <h2>Titles</h2>
                <a href="/marketplace/titles">Got to Titles</a>
            </section>

            <section>
                <h2>Avatars</h2>
                <a href="/marketplace/avatars">Got to Avatars</a>
            </section>
        </Container>
    );
}