import React, { useEffect, useState, useCallback } from 'react';
import axios from 'axios';
import '../styles.css';
import Container from 'react-bootstrap/Container';

export const Quiz = () => {
    const [questions, setQuestions] = useState([]);
    const [currentQuestion, setCurrentQuestion] = useState(0);
    const [selectedAnswer, setSelectedAnswer] = useState('');
    const [timeLeft, setTimeLeft] = useState(15);  // 15 second count down
    const [feedback, setFeedback] = useState('');
    const [totalScore, setTotalScore] = useState(0);  // track total score
    const [quizFinished, setQuizFinished] = useState(false); // track if quiz finish
    const currentUsername = sessionStorage.getItem('username'); // get user

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

            setTotalScore(newTotalScore);

            // next quiz
            setTimeout(() => {
                setSelectedAnswer('');
                setFeedback('');
                setTimeLeft(15);  // reset count down

                if (currentQuestion + 1 < questions.length) {
                    setCurrentQuestion(currentQuestion + 1);
                } else {
                    // show total score and send to backend
                    setQuizFinished(true);
                    alert(`Quiz finished! Your total score: ${newTotalScore}`);

                    // upload total score
                    axios.post(`http://localhost:8000/quiz/${quizId}/finalize/`, {
                        username: currentUsername,
                        total_score: newTotalScore  // new total score
                    }).then(() => {
                        console.log("User score updated successfully.");
                    }).catch(err => {
                        console.error("Error updating user score: ", err);
                    });
                }
            }, 2000); // next
        })
        .catch(error => {
            console.error('Error submitting quiz answer:', error);
        });
    }, [selectedAnswer, currentQuestion, questions, currentUsername, totalScore]);

    // count down
    useEffect(() => {
        if (timeLeft > 0 && !quizFinished) {
            const timer = setTimeout(() => setTimeLeft(timeLeft - 1), 1000);
            return () => clearTimeout(timer);
        } else if (timeLeft === 0) {
            setFeedback('Out of time!');
            handleSubmitAnswer();
        }
    }, [timeLeft, quizFinished, handleSubmitAnswer]);

    const handleAnswerSelect = (answer) => {
        setSelectedAnswer(answer);
    };

    if (questions.length === 0 || !questions[currentQuestion]) return <div>Loading quiz...</div>;

    return (
        <Container className="quiz-container quiz-box">
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
        </Container>
    );
};

export default Quiz;
