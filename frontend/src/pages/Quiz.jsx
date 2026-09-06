import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";

const quizQuestions = {
  Fractions: [
    {
      id: 1,
      question: "What is 1/2 + 1/4?",
      options: ["2/6", "3/4", "1/6", "3/8"],
      answer: "3/4",
      concept: "Fractions",
    },
    {
      id: 2,
      question: "Which fraction is equivalent to 2/4?",
      options: ["1/2", "1/3", "2/3", "3/4"],
      answer: "1/2",
      concept: "Fractions",
    },
    {
      id: 3,
      question: "What is 3/5 - 1/5?",
      options: ["2/5", "4/5", "2/10", "1/5"],
      answer: "2/5",
      concept: "Fractions",
    },
  ],

  "Algebraic Expressions": [
    {
      id: 1,
      question: "Simplify: 4x + 2x",
      options: ["6x", "8x", "6", "2x"],
      answer: "6x",
      concept: "Algebraic Expressions",
    },
    {
      id: 2,
      question: "What is the coefficient of x in 7x + 3?",
      options: ["3", "7", "x", "10"],
      answer: "7",
      concept: "Algebraic Expressions",
    },
    {
      id: 3,
      question: "Simplify: 5a - 2a",
      options: ["7a", "3a", "3", "10a"],
      answer: "3a",
      concept: "Algebraic Expressions",
    },
  ],

  "Linear Equations": [
    {
      id: 1,
      question: "Solve: x + 7 = 15",
      options: ["6", "7", "8", "9"],
      answer: "8",
      concept: "Linear Equations",
    },
    {
      id: 2,
      question: "Solve: 2x = 10",
      options: ["2", "5", "10", "12"],
      answer: "5",
      concept: "Linear Equations",
    },
    {
      id: 3,
      question: "Solve: x - 4 = 9",
      options: ["5", "12", "13", "14"],
      answer: "13",
      concept: "Linear Equations",
    },
  ],

  "Quadratic Equations": [
    {
      id: 1,
      question: "Solve: x² - 5x + 6 = 0",
      options: ["2, 3", "1, 6", "3, 4", "2, 4"],
      answer: "2, 3",
      concept: "Quadratic Equations",
    },
    {
      id: 2,
      question: "Which expression is a quadratic equation?",
      options: [
        "2x + 3 = 0",
        "x² + 4x + 4 = 0",
        "5x = 10",
        "x + 1 = 2",
      ],
      answer: "x² + 4x + 4 = 0",
      concept: "Quadratic Equations",
    },
    {
      id: 3,
      question: "What is the highest power in a quadratic equation?",
      options: ["1", "2", "3", "4"],
      answer: "2",
      concept: "Quadratic Equations",
    },
  ],
};

function Quiz() {
  const navigate = useNavigate();
  const location = useLocation();

  const concept = location.state?.concept || "Fractions";

  const questions =
    quizQuestions[concept] ||
    quizQuestions["Fractions"];

  const [currentQuestion, setCurrentQuestion] = useState(0);

  const [answers, setAnswers] = useState({});

  const [selectedAnswer, setSelectedAnswer] =
    useState("");

  const [showFeedback, setShowFeedback] =
    useState(false);

  const question = questions[currentQuestion];

  const progress =
    ((currentQuestion + 1) / questions.length) * 100;


  /* ==========================================
     SELECT ANSWER
  ========================================== */

  const handleAnswer = (option) => {
    if (showFeedback) {
      return;
    }

    setSelectedAnswer(option);

    setAnswers((previousAnswers) => ({
      ...previousAnswers,
      [question.id]: option,
    }));

    setShowFeedback(true);
  };


  /* ==========================================
     SUBMIT QUIZ
  ========================================== */

  const handleSubmit = () => {
    let score = 0;

    questions.forEach((q) => {
      if (answers[q.id] === q.answer) {
        score++;
      }
    });

    /*
      React state updates are asynchronous.
      Therefore, we manually check the final
      selected answer as well.
    */

    if (
      selectedAnswer === question.answer &&
      answers[question.id] !== selectedAnswer
    ) {
      score++;
    }

    const percentage = Math.round(
      (score / questions.length) * 100
    );

    console.log("Adaptive Quiz Result:", {
      concept,
      score,
      total: questions.length,
      percentage,
    });

    /*
      Send the quiz result to QuizResult page.
    */

    navigate("/quiz-result", {
      state: {
        concept: concept,
        score: score,
        total: questions.length,
        percentage: percentage,
      },
    });
  };


  /* ==========================================
     NEXT QUESTION
  ========================================== */

  const handleNext = () => {
    if (!selectedAnswer) {
      return;
    }

    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(
        (previousQuestion) => previousQuestion + 1
      );

      setSelectedAnswer("");

      setShowFeedback(false);
    } else {
      handleSubmit();
    }
  };


  const isCorrect =
    selectedAnswer === question.answer;


  return (
    <div className="quiz-page">

      {/* ======================================
          NAVBAR
      ====================================== */}

      <nav className="dashboard-navbar">

        <div
          className="dashboard-logo"
          onClick={() => navigate("/dashboard")}
          style={{ cursor: "pointer" }}
        >
          Adapt<span>IQ</span> 🧠
        </div>


        <div className="nav-links">

          <button
            onClick={() => navigate("/dashboard")}
          >
            Dashboard
          </button>

          <button
            onClick={() => navigate("/learning-path")}
          >
            Learning Path
          </button>

          <button
            onClick={() => navigate("/progress")}
          >
            Progress
          </button>

          <button
            onClick={() => navigate("/tutor")}
          >
            AI Tutor
          </button>

        </div>


        <div className="student-info">
          👩‍🎓 Student
        </div>

      </nav>


      {/* ======================================
          MAIN CONTAINER
      ====================================== */}

      <main className="quiz-container">


        {/* ====================================
            HEADER
        ==================================== */}

        <section className="quiz-header">

          <div>

            <p className="card-label">
              ADAPTIVE ASSESSMENT
            </p>

            <h1>
              Test your understanding 🎯
            </h1>

            <p>
              AdaptIQ uses your answers to
              understand your current mastery
              of {concept}.
            </p>

          </div>


          <div className="quiz-concept-badge">
            🧠 {concept}
          </div>

        </section>


        {/* ====================================
            PROGRESS
        ==================================== */}

        <section className="quiz-progress-card">

          <div className="quiz-progress-info">

            <span>
              Question {currentQuestion + 1} of{" "}
              {questions.length}
            </span>

            <span>
              {Math.round(progress)}%
            </span>

          </div>


          <div className="quiz-progress-track">

            <div
              className="quiz-progress-fill"
              style={{
                width: `${progress}%`,
              }}
            ></div>

          </div>

        </section>


        {/* ====================================
            QUESTION CARD
        ==================================== */}

        <section className="quiz-card">

          <div className="quiz-question-number">
            QUESTION {currentQuestion + 1}
          </div>


          <h2>
            {question.question}
          </h2>


          {/* OPTIONS */}

          <div className="quiz-options">

            {question.options.map(
              (option, index) => {

                let className = "quiz-option";


                /*
                  After selecting an answer,
                  show correct / incorrect states.
                */

                if (showFeedback) {

                  if (
                    option === question.answer
                  ) {
                    className += " correct";
                  }

                  if (
                    option === selectedAnswer &&
                    option !== question.answer
                  ) {
                    className += " incorrect";
                  }

                } else if (
                  option === selectedAnswer
                ) {

                  className += " selected";

                }


                return (
                  <button
                    key={option}
                    className={className}
                    onClick={() =>
                      handleAnswer(option)
                    }
                  >

                    <span className="quiz-option-letter">
                      {String.fromCharCode(
                        65 + index
                      )}
                    </span>


                    <span>
                      {option}
                    </span>


                    {showFeedback &&
                      option ===
                        question.answer && (
                        <span className="quiz-option-result">
                          ✓
                        </span>
                      )}


                    {showFeedback &&
                      option === selectedAnswer &&
                      option !==
                        question.answer && (
                        <span className="quiz-option-result">
                          ✕
                        </span>
                      )}

                  </button>
                );
              }
            )}

          </div>


          {/* ==================================
              FEEDBACK
          ================================== */}

          {showFeedback && (

            <div
              className={
                isCorrect
                  ? "quiz-feedback correct-feedback"
                  : "quiz-feedback incorrect-feedback"
              }
            >

              <div className="feedback-icon">
                {isCorrect ? "🎉" : "💡"}
              </div>


              <div>

                <strong>
                  {isCorrect
                    ? "Correct!"
                    : "Let's understand this better."}
                </strong>


                <p>
                  {isCorrect
                    ? "Great job! Your mastery of this concept is improving."
                    : `The correct answer is ${question.answer}. AdaptIQ detected that you may need more practice with ${concept}.`}
                </p>

              </div>

            </div>

          )}


          {/* ==================================
              BUTTONS
          ================================== */}

          <div className="quiz-controls">

            <button
              className="quiz-back-button"
              onClick={() =>
                navigate("/learning-path")
              }
            >
              ← Learning Path
            </button>


            <button
              className="quiz-next-button"
              disabled={!selectedAnswer}
              onClick={handleNext}
            >

              {currentQuestion ===
              questions.length - 1
                ? "Finish Quiz ✓"
                : "Next Question →"}

            </button>

          </div>

        </section>


        {/* ====================================
            ADAPTIVE INFORMATION
        ==================================== */}

        <section className="adaptive-info">

          <div className="adaptive-info-icon">
            🧠
          </div>


          <div>

            <p className="card-label">
              ADAPTIQ IS LEARNING ABOUT YOU
            </p>

            <h2>
              Your answers influence your
              learning path
            </h2>

            <p>
              AdaptIQ analyzes your performance
              to identify concepts that need more
              practice and adjust your next
              learning activity.
            </p>

          </div>

        </section>

      </main>

    </div>
  );
}

export default Quiz;