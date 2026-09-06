import { useState } from "react";
import { useNavigate } from "react-router-dom";

const questions = [
  {
    id: 1,
    question: "What is 3/4 + 1/4?",
    options: ["1", "1/2", "3/8", "4/8"],
    answer: "1",
    concept: "Fractions",
  },
  {
    id: 2,
    question: "Solve: x + 5 = 12",
    options: ["5", "7", "17", "6"],
    answer: "7",
    concept: "Linear Equations",
  },
  {
    id: 3,
    question: "Simplify: 2x + 3x",
    options: ["5x", "6x", "5", "x"],
    answer: "5x",
    concept: "Algebraic Expressions",
  },
  {
    id: 4,
    question: "Solve: x² - 5x + 6 = 0",
    options: ["2, 3", "1, 6", "3, 4", "2, 4"],
    answer: "2, 3",
    concept: "Quadratic Equations",
  },
];

function Diagnostic() {
  const navigate = useNavigate();

  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState({});

  const question = questions[currentQuestion];

  const selectedAnswer = answers[question.id];

  const progress =
    ((currentQuestion + 1) / questions.length) * 100;

  // Select answer
  const handleAnswer = (option) => {
    setAnswers((previousAnswers) => ({
      ...previousAnswers,
      [question.id]: option,
    }));
  };

  // Next question
  const handleNext = () => {
    if (!selectedAnswer) return;

    setCurrentQuestion((previous) => previous + 1);
  };

  // Previous question
  const handlePrevious = () => {
    if (currentQuestion === 0) return;

    setCurrentQuestion((previous) => previous - 1);
  };

  // Submit
  const handleSubmit = () => {
    let score = 0;

    const conceptResults = {};

    questions.forEach((q) => {
      const userAnswer = answers[q.id];

      const isCorrect = userAnswer === q.answer;

      if (isCorrect) {
        score++;
      }

      if (!conceptResults[q.concept]) {
        conceptResults[q.concept] = {
          correct: 0,
          total: 0,
        };
      }

      conceptResults[q.concept].total++;

      if (isCorrect) {
        conceptResults[q.concept].correct++;
      }
    });

    // Calculate mastery
    const mastery = {};

    Object.entries(conceptResults).forEach(
      ([concept, result]) => {
        mastery[concept] = Math.round(
          (result.correct / result.total) * 100
        );
      }
    );

    console.log("Diagnostic submitted:", {
      score,
      total: questions.length,
      mastery,
    });

    // GO TO RESULTS
    navigate("/results", {
      state: {
        score: score,
        total: questions.length,
        mastery: mastery,
      },
    });
  };

  return (
    <div className="diagnostic-page">

      {/* NAVBAR */}

      <nav className="dashboard-navbar">

        <div
          className="dashboard-logo"
          onClick={() => navigate("/dashboard")}
          style={{ cursor: "pointer" }}
        >
          Adapt<span>IQ</span> 🧠
        </div>

        <div className="student-info">
          👩‍🎓 Student
        </div>

      </nav>


      {/* MAIN */}

      <main className="diagnostic-container">

        <div className="diagnostic-header">

          <p className="card-label">
            ADAPTIVE ASSESSMENT
          </p>

          <h1>
            Let's understand what you know 🧠
          </h1>

          <p>
            This short assessment helps AdaptIQ identify
            your strengths and learning gaps.
          </p>

        </div>


        {/* PROGRESS */}

        <div className="question-progress">

          <div className="progress-info">

            <span>
              Question {currentQuestion + 1} of{" "}
              {questions.length}
            </span>

            <span>
              {Math.round(progress)}%
            </span>

          </div>

          <div className="progress-track">

            <div
              className="progress-fill"
              style={{
                width: `${progress}%`,
              }}
            ></div>

          </div>

        </div>


        {/* QUESTION */}

        <div className="diagnostic-card">

          <div className="question-number">
            Question {question.id}
          </div>

          <h2>
            {question.question}
          </h2>


          {/* OPTIONS */}

          <div className="diagnostic-options">

            {question.options.map((option) => (

              <button
                key={option}
                className={
                  selectedAnswer === option
                    ? "diagnostic-option selected"
                    : "diagnostic-option"
                }
                onClick={() =>
                  handleAnswer(option)
                }
              >
                <span className="option-circle">
                  {option}
                </span>
              </button>

            ))}

          </div>


          {/* BUTTONS */}

          <div className="diagnostic-controls">

            <button
              className="previous-button"
              onClick={handlePrevious}
              disabled={currentQuestion === 0}
            >
              ← Previous
            </button>


            {currentQuestion <
            questions.length - 1 ? (

              <button
                className="next-button"
                onClick={handleNext}
                disabled={!selectedAnswer}
              >
                Next →
              </button>

            ) : (

              <button
                className="submit-button"
                onClick={handleSubmit}
                disabled={!selectedAnswer}
              >
                Submit Assessment ✓
              </button>

            )}

          </div>

        </div>


        {/* TIP */}

        <div className="diagnostic-tip">

          💡 <strong>Tip:</strong> Don't worry about
          getting everything correct. AdaptIQ uses your
          answers to understand what you need to learn next.

        </div>

      </main>

    </div>
  );
}

export default Diagnostic;