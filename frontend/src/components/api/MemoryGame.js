// frontend/src/components/api/MemoryGame.js

import React, { useState, useEffect, useCallback } from 'react';
import './MemoryGame.css';
import SingleCard from './SingleCard';
import axios from 'axios';

const cardImages = [
    { src: '/img/dog1.jpg', matched: false },
    { src: '/img/dog2.jpg', matched: false },
    { src: '/img/dog3.jpg', matched: false },
    { src: '/img/dog4.jpg', matched: false },
    { src: '/img/dog5.jpg', matched: false },
    { src: '/img/dog6.jpg', matched: false },
    { src: '/img/dog7.jpg', matched: false },
    { src: '/img/dog8.jpg', matched: false },
    { src: '/img/dog9.jpg', matched: false },
];

const MemoryGame = () => {
    const [cards, setCards] = useState([]);
    const [firstChoice, setFirstChoice] = useState(null);
    const [secondChoice, setSecondChoice] = useState(null);
    const [disabled, setDisabled] = useState(false);
    const [score, setScore] = useState(0);
    const [timeLeft, setTimeLeft] = useState(60); // 60-second countdown
    const [gameStarted, setGameStarted] = useState(false); // if the game has started
    const currentUsername = sessionStorage.getItem('username'); // current user

    // Shuffle cards and start a new game
    const shuffleCards = () => {
        const shuffledCards = [...cardImages, ...cardImages]
            .sort(() => Math.random() - 0.5)
            .map((card) => ({ ...card, id: Math.random() }));

        setCards(shuffledCards);
        setFirstChoice(null);
        setSecondChoice(null);
        setScore(0);
        setTimeLeft(60);
        setGameStarted(true); // Start the game
    };

    // Handle user's card choice
    const handleChoice = (card) => {
        if (!disabled) {
            firstChoice ? setSecondChoice(card) : setFirstChoice(card);
        }
    };

    // Compare two selected cards
    useEffect(() => {
        if (firstChoice && secondChoice) {
            setDisabled(true);
            if (firstChoice.src === secondChoice.src) {
                setCards((prevCards) => {
                    return prevCards.map((card) => {
                        if (card.src === firstChoice.src) {
                            return { ...card, matched: true };
                        } else {
                            return card;
                        }
                    });
                });
                setScore((prevScore) => prevScore + 5); // Increase score by 5
                resetTurn();
            } else {
                setTimeout(() => resetTurn(), 1000); // Flip back after 1 second
            }
        }
    }, [firstChoice, secondChoice]);

    // Reset choices and enable clicking
    const resetTurn = () => {
        setFirstChoice(null);
        setSecondChoice(null);
        setDisabled(false);
    };

    // Send score to the backend
    const sendScore = useCallback(() => {
        axios
            .post('http://localhost:8000/memory-game/submit-score/', {
                username: currentUsername,
                score: score,
            })
            .then((response) => {
                console.log('Score submitted successfully.');
            })
            .catch((error) => {
                console.error('Error submitting score:', error);
            });
    }, [currentUsername, score]);

    // Start the timer
    useEffect(() => {
        if (gameStarted && timeLeft > 0 && cards.length > 0) {
            const timer = setTimeout(() => setTimeLeft(timeLeft - 1), 1000);
            return () => clearTimeout(timer);
        } else if (gameStarted && timeLeft === 0) {
            // Time is up
            alert('Time is up!');
            sendScore();
            // Reset the game
            setGameStarted(false);
            setCards([]);
        }
    }, [timeLeft, cards, sendScore, gameStarted]);

    // Check if the game is completed
    useEffect(() => {
        if (gameStarted && cards.length > 0 && cards.every((card) => card.matched)) {
            alert('Congratulations! You completed the game!');
            sendScore();
            // Reset the game
            setGameStarted(false);
            setCards([]);
        }
    }, [cards, sendScore, gameStarted]);

    return (
        <div className="memory-game">
            {!gameStarted ? (
                <>
                    <button onClick={shuffleCards} className="start-game-button">
                        Start Game
                    </button>
                </>
            ) : (
                <>
                    <h1>Doggy Memory Flip Game</h1>
                    <p>Time Left: {timeLeft} seconds</p>
                    <p>Score: {score}</p>
                    <button onClick={() => setGameStarted(false)} className="end-game-button">
                        End Game
                    </button>
                    <div className="card-grid">
                        {cards.map((card) => (
                            <SingleCard
                                key={card.id}
                                card={card}
                                handleChoice={handleChoice}
                                flipped={card === firstChoice || card === secondChoice || card.matched}
                                disabled={disabled}
                            />
                        ))}
                    </div>
                </>
            )}
        </div>
    );
};

export default MemoryGame;
