import React, { useEffect, useState, useCallback } from 'react';
import axios from 'axios';
import '../styles.css';
import Container from 'react-bootstrap/Container';
import QuizLeaderboard from './QuizLeaderboard';  // Import the QuizLeaderboard component

export const Quiz = () => {
    const [questions, setQuestions] = useState([]);
    const [currentQuestion, setCurrentQuestion] = useState(0);
    const [selectedAnswer, setSelectedAnswer] = useState('');
    const [timeLeft, setTimeLeft] = useState(15);  // 15-second countdown
    const [feedback, setFeedback] = useState('');
    const [totalScore, setTotalScore] = useState(0);  // Used to track the total score during the quiz
    const [quizFinished, setQuizFinished] = useState(false); // Used to track whether the quiz has finished
    const [quizStarted, setQuizStarted] = useState(false); // Used to track whether the quiz has started
    const [canEarnPoints, setCanEarnPoints] = useState(true); // Used to track if the user can earn points
    const currentUsername = sessionStorage.getItem('username'); // Get the current user
    const quizId = 1;  // Define quizId here for reuse
    const [totalCorrectAnswers, setTotalCorrectAnswers] = useState(0);

    useEffect(() => {
        // Get quiz questions (backend now returns 3 random questions)
        axios.get(`http://localhost:8000/quiz/${quizId}/questions/`)
            .then(response => {
                setQuestions(response.data.questions);
            })
            .catch(error => {
                console.error('Error fetching quiz questions:', error);
            });
    }, [quizId]);

    // Function to check quiz eligibility
    const handleStartQuiz = () => {
        axios.get(`http://localhost:8000/quiz/${quizId}/eligibility/`, {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Username ${currentUsername}`
            }
        })
        .then(response => {
            if (response.data.can_earn_points) {
                setCanEarnPoints(true);
                setQuizStarted(true);
            } else {
                const { hours, minutes, seconds } = response.data.remaining_time;
                const proceed = window.confirm(`You have ${hours} hours, ${minutes} minutes, and ${seconds} seconds remaining before you can earn points again. Do you still want to proceed with the quiz?`);
                if (proceed) {
                    setCanEarnPoints(false);
                    setQuizStarted(true);
                }
            }
        })
        .catch(error => {
            console.error('Error checking quiz eligibility:', error);
        });
    };

    // Logic to handle answer submission
    const handleSubmitAnswer = useCallback((isTimeout = false) => {
        if (!selectedAnswer && !isTimeout) {
            setFeedback('Please select an answer before submitting.');
            return;
        }

        const questionId = questions[currentQuestion].id;
        let newTotalScore = totalScore;

        // Submit the answer to the backend
        axios.post(`http://localhost:8000/quiz/${quizId}/submit/`, {
            answers: { [questionId]: selectedAnswer || '' }
        }, {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Username ${currentUsername}`  // Authenticate the user
            }
        })
        .then(response => {
            const { message } = response.data;
            const questionPoints = questions[currentQuestion].points || 0;

            // Update feedback based on timeout
            if (isTimeout) {
                setFeedback('Time out!');
            } else if (message === 'Correct') {
                setFeedback('Correct!');
                newTotalScore += questionPoints;
                setTotalCorrectAnswers(prev => prev + 1);  // num of corrected quiz
            } else {
                setFeedback('Incorrect!');
            }

            // Update the total score in the state
            setTotalScore(newTotalScore);

            // Handle the next steps
            setTimeout(() => {
                setSelectedAnswer('');
                setFeedback('');
                setTimeLeft(15);  // Reset the countdown timer

                if (currentQuestion + 1 < questions.length) {
                    setCurrentQuestion(currentQuestion + 1);
                } else {
                    // Show total score and send to backend
                    setQuizFinished(true);

                    // If the user cannot earn points, show a different message
                    if (canEarnPoints) {
                        alert(`Quiz finished! Your total score is: ${newTotalScore}`);
                    } else {
                        alert('Quiz completed.');
                    }

                    // Upload total score
                    axios.post(`http://localhost:8000/quiz/${quizId}/finalize/`, {
                        username: currentUsername,
                        total_score: newTotalScore,  // New total score
                        total_correct: totalCorrectAnswers
                    }).then((response) => {
                        console.log("User score updated successfully.");
                        if (response.data.message) {
                            alert(response.data.message);
                        }
                    }).catch(err => {
                        console.error("Error updating user score:", err);
                    });

                    // Reset quiz state
                    setQuizStarted(false);          // Back to 'start quiz'
                    setCurrentQuestion(0);          // Reset question index
                    setTotalScore(0);               // Reset total score
                    setTimeLeft(15);                // Reset time countdown
                    setSelectedAnswer('');          // Clear selected answer
                    setFeedback('');                // Clear feedback
                    setQuizFinished(false);         // Reset finished state
                    setCanEarnPoints(true);         // Reset canEarnPoints
                    setTotalCorrectAnswers(0);      // Reset TotalCorrectAnswers
                }
            }, 2000); // 2 seconds before proceeding to the next step
        })
        .catch(error => {
            console.error('Error submitting quiz answer:', error);
        });
    }, [selectedAnswer, currentQuestion, questions, currentUsername, totalScore, canEarnPoints, quizId]);

    // Countdown logic
    useEffect(() => {
        if (quizStarted && timeLeft > 0 && !quizFinished) {
            const timer = setTimeout(() => setTimeLeft(timeLeft - 1), 1000);
            return () => clearTimeout(timer);
        } else if (quizStarted && timeLeft === 0) {
            handleSubmitAnswer(true); // Pass true to indicate timeout
        }
    }, [quizStarted, timeLeft, quizFinished, handleSubmitAnswer]);

    const handleAnswerSelect = (answer) => {
        setSelectedAnswer(answer);
    };

    if (questions.length === 0 || !questions[currentQuestion]) return <div>Loading quiz...</div>;

    return (
        <Container className="quiz-container quiz-box">
            {!quizStarted ? (
                <>
                    <button onClick={handleStartQuiz} className="start-quiz-button">Start Quiz</button>
                    {/* Embed the QuizLeaderboard component */}
                    <QuizLeaderboard quizId={quizId} />
                </>
            ) : (
                <>
                    <h2 className="quiz-question">{questions[currentQuestion].question_text}</h2>
                    <div className="time-left">Time left: {timeLeft} seconds</div>
                    <div className="choices-container">
                        {questions[currentQuestion].choices.map((choice, index) => (
                            <button
                                key={index}
                                onClick={() => handleAnswerSelect(choice.text)}
                                className={`choice-button ${selectedAnswer === choice.text ? 'selected' : ''}`}
                            >
                                {choice.text}
                            </button>
                        ))}
                    </div>
                    <div className="submit-button-container">
                        <button onClick={() => handleSubmitAnswer()} className="submit-button">Submit</button>
                    </div>
                    {feedback && <div className="feedback">{feedback}</div>}
                </>
            )}
        </Container>
    );
};

export default Quiz;
