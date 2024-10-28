// frontend/src/components/api/SingleCard.js

import React from 'react';
import './SingleCard.css';

const SingleCard = ({ card, handleChoice, flipped, disabled }) => {
    const handleClick = () => {
        if (!disabled) {
            handleChoice(card);
        }
    };

    return (
        <div className="card">
            <div className={flipped ? 'flipped' : ''}>
                <img className="front" src={card.src} alt="card front" />
                <img
                    className="back"
                    src="/img/cover.jpg" // Card back image, ensure cover.jpg exists in public/img
                    onClick={handleClick}
                    alt="card back"
                />
            </div>
        </div>
    );
};

export default SingleCard;
