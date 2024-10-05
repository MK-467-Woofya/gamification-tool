import React, { useEffect, useState, useCallback } from 'react';
import axios from 'axios';
import '../styles.css';
import Container from 'react-bootstrap/Container';

export const Quiz = () => {
    const [questions, setQuestions] = useState([]);
    const [currentQuestion, setCurrentQuestion] = useState(0);
    const [selectedAnswer, setSelectedAnswer] = useState('');
    const [timeLeft, setTimeLeft] = useState(15);  // 15-second countdown
    const [feedback, setFeedback] = useState('');
    const [totalScore, setTotalScore] = useState(0);  // Used to track the total score during the quiz
    const [quizFinished, setQuizFinished] = useState(false); // Used to track whether the quiz has finished
    const [quizStarted, setQuizStarted] = useState(false); // Used to track whether the quiz has started
    const currentUsername = sessionStorage.getItem('username'); // Get the current user

    useEffect(() => {
        // get quiz
        const quizId = 1;
        axios.get(`http://localhost:8000/quiz/${quizId}/questions/`)
            .then(response => {
                setQuestions(response.data.questions);
            })
            .catch(error => {
                console.error('Error fetching quiz questions:', error);
            });
    }, []);

    // submit logic
    const handleSubmitAnswer = useCallback(() => {
        if (!selectedAnswer) {
            setFeedback('Please select an answer before submitting.');
            return;
        }

        const quizId = 1;
        const questionId = questions[currentQuestion].id;
        let newTotalScore = totalScore;

        // submit
        axios.post(`http://localhost:8000/quiz/${quizId}/submit/`, {
            answers: { [questionId]: selectedAnswer }
        }, {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Username ${currentUsername}`  // authenticate
            }
        })
        .then(response => {
            const { message } = response.data;
            const questionPoints = questions[currentQuestion].points || 0;

            // update score
            if (message === 'Correct') {
                setFeedback('Correct!');
                newTotalScore += questionPoints;
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
                    // show total score and send to backend
                    setQuizFinished(true);
                    alert(`Quiz finished! Your total score is: ${newTotalScore}`);

                    // upload total score
                    axios.post(`http://localhost:8000/quiz/${quizId}/finalize/`, {
                        username: currentUsername,
                        total_score: newTotalScore  // new total score
                    }).then(() => {
                        console.log("User score updated successfully.");
                    }).catch(err => {
                        console.error("Error updating user score:", err);
                    });

                    setQuizStarted(false);          // back to 'start quiz'
                    setCurrentQuestion(0);          // reset question index
                    setTotalScore(0);               // reset total score
                    setTimeLeft(15);                // reset time count down
                    setSelectedAnswer('');          // clear answer
                    setFeedback('');                // clear feedback
                    setQuizFinished(false);         // reset finished state
                }
            }, 2000); // 2 seconds before proceeding to the next step
        })
        .catch(error => {
            console.error('Error submitting quiz answer:', error);
        });
    }, [selectedAnswer, currentQuestion, questions, currentUsername, totalScore]);

    // count down
    useEffect(() => {
        if (quizStarted && timeLeft > 0 && !quizFinished) {
            const timer = setTimeout(() => setTimeLeft(timeLeft - 1), 1000);
            return () => clearTimeout(timer);
        } else if (quizStarted && timeLeft === 0) {
            setFeedback('Time\'s up!');
            handleSubmitAnswer();
        }
    }, [quizStarted, timeLeft, quizFinished, handleSubmitAnswer]);

    const handleAnswerSelect = (answer) => {
        setSelectedAnswer(answer);
    };

    if (questions.length === 0 || !questions[currentQuestion]) return <div>Loading quiz...</div>;

    return (
        <Container className="quiz-container quiz-box">
            {!quizStarted ? (
                <button onClick={() => setQuizStarted(true)} className="start-quiz-button">Start Quiz</button>
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
                        <button onClick={handleSubmitAnswer} className="submit-button">Submit</button>
                    </div>
                    {feedback && <div className="feedback">{feedback}</div>}
                </>
            )}
        </Container>
    );
};

export default Quiz;
