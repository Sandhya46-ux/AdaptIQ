import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const questions = [
  {
    id: 1,
    question: "What is 1/2 + 1/4?",
    options: ["1/4", "2/4", "3/4", "4/4"],
    answer: "3/4",
    concept: "Fractions",
  },
  {
    id: 2,
    question: "Solve: 2x + 5 = 15",
    options: ["x = 5", "x = 10", "x = 7", "x = 3"],
    answer: "x = 5",
    concept: "Linear Equations",
  },
  {
    id: 3,
    question: "Simplify: 3x + 2x",
    options: ["5", "5x", "6x", "x"],
    answer: "5x",
    concept: "Algebraic Expressions",
  },
  {
    id: 4,
    question: "What are the roots of x² - 5x + 6 = 0?",
    options: [
      "2 and 3",
      "1 and 6",
      "-2 and -3",
      "3 and 4",
    ],
    answer: "2 and 3",
    concept: "Quadratic Equations",
  },
];

function Diagnostic() {
  const navigate = useNavigate();

  const [answers, setAnswers] = useState({});
  const [submitted, setSubmitted] = useState(false);

  const handleAnswer = (questionId, answer) => {
    setAnswers((prev) => ({
      ...prev,
      [questionId]: answer,
    }));
  };

  const calculateResults = () => {
    let score = 0;

    const mastery = {};

    questions.forEach((question) => {
      const isCorrect = answers[question.id] === question.answer;

      if (isCorrect) {
        score++;
      }

      mastery[question.concept] = isCorrect ? 100 : 0;
    });

    const percentage = Math.round((score / questions.length) * 100);

    return {
      score,
      total: questions.length,
      percentage,
      mastery,
    };
  };

  const handleSubmit = () => {
    if (Object.keys(answers).length !== questions.length) {
      alert("Please answer all questions before submitting.");
      return;
    }

    const result = calculateResults();

    // Save diagnostic result in browser
    localStorage.setItem(
      "adaptIQDiagnostic",
      JSON.stringify(result)
    );

    setSubmitted(true);

    // Move to Learner Profile
    setTimeout(() => {
      navigate("/learner-profile");
    }, 500);
  };

  return (
    <div className="diagnostic-page">

      {/* Header */}
      <header className="page-header">
        <div className="logo">
          <span>Adapt</span>IQ
        </div>

        <nav>
          <button onClick={() => navigate("/dashboard")}>
            Dashboard
          </button>

          <button className="active">
            Diagnostic
          </button>

          <button onClick={() => navigate("/learning-path")}>
            Learning Path
          </button>

          <button onClick={() => navigate("/progress")}>
            Progress
          </button>

          <button onClick={() => navigate("/tutor")}>
            AI Tutor
          </button>
        </nav>
      </header>

      {/* Main */}
      <main className="diagnostic-container">

        <div className="diagnostic-heading">
          <h1>Diagnostic Assessment</h1>

          <p>
            Let's understand your current knowledge level.
            Answer the questions honestly so AdaptIQ can
            create a personalized learning path for you.
          </p>
        </div>

        {/* Progress */}
        <div className="diagnostic-progress">
          <div>
            <span>Questions</span>
            <strong>
              {Object.keys(answers).length} / {questions.length}
            </strong>
          </div>

          <div className="progress-bar">
            <div
              style={{
                width: `${
                  (Object.keys(answers).length /
                    questions.length) *
                  100
                }%`,
              }}
            ></div>
          </div>
        </div>

        {/* Questions */}
        <div className="questions-container">

          {questions.map((question, index) => (
            <div className="question-card" key={question.id}>

              <div className="question-number">
                Question {index + 1}
              </div>

              <h2>{question.question}</h2>

              <p className="concept">
                Topic: {question.concept}
              </p>

              <div className="options">

                {question.options.map((option) => (
                  <label
                    key={option}
                    className={`option ${
                      answers[question.id] === option
                        ? "selected"
                        : ""
                    }`}
                  >

                    <input
                      type="radio"
                      name={`question-${question.id}`}
                      value={option}
                      checked={
                        answers[question.id] === option
                      }
                      onChange={() =>
                        handleAnswer(
                          question.id,
                          option
                        )
                      }
                    />

                    <span>{option}</span>

                  </label>
                ))}

              </div>

            </div>
          ))}

        </div>

        {/* Submit */}
        <div className="submit-section">

          <button
            className="submit-diagnostic"
            onClick={handleSubmit}
            disabled={submitted}
          >
            {submitted
              ? "Analyzing Your Performance..."
              : "Submit Diagnostic Test"}
          </button>

        </div>

      </main>

      {/* Page CSS */}
      <style>{`

        * {
          box-sizing: border-box;
        }

        .diagnostic-page {
          min-height: 100vh;
          background: #f6f8fc;
          color: #1e293b;
        }

        /* Header */

        .page-header {
          height: 70px;
          background: white;
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 0 7%;
          border-bottom: 1px solid #e5e7eb;
          position: sticky;
          top: 0;
          z-index: 10;
        }

        .logo {
          font-size: 26px;
          font-weight: 800;
          color: #111827;
        }

        .logo span {
          color: #6366f1;
        }

        .page-header nav {
          display: flex;
          gap: 8px;
        }

        .page-header nav button {
          border: none;
          background: transparent;
          padding: 10px 14px;
          border-radius: 8px;
          cursor: pointer;
          color: #64748b;
          font-size: 14px;
        }

        .page-header nav button:hover {
          background: #f1f5f9;
          color: #4f46e5;
        }

        .page-header nav button.active {
          background: #eef2ff;
          color: #4f46e5;
          font-weight: 600;
        }

        /* Container */

        .diagnostic-container {
          width: 90%;
          max-width: 900px;
          margin: 0 auto;
          padding: 45px 0 70px;
        }

        .diagnostic-heading {
          text-align: center;
          margin-bottom: 35px;
        }

        .diagnostic-heading h1 {
          font-size: 36px;
          margin-bottom: 12px;
          color: #111827;
        }

        .diagnostic-heading p {
          max-width: 650px;
          margin: auto;
          color: #64748b;
          line-height: 1.7;
        }

        /* Progress */

        .diagnostic-progress {
          background: white;
          padding: 20px;
          border-radius: 14px;
          margin-bottom: 25px;
          border: 1px solid #e5e7eb;
        }

        .diagnostic-progress > div:first-child {
          display: flex;
          justify-content: space-between;
          margin-bottom: 10px;
        }

        .diagnostic-progress span {
          color: #64748b;
          font-size: 14px;
        }

        .diagnostic-progress strong {
          color: #4f46e5;
        }

        .progress-bar {
          width: 100%;
          height: 8px;
          background: #e5e7eb;
          border-radius: 20px;
          overflow: hidden;
        }

        .progress-bar div {
          height: 100%;
          background: #6366f1;
          border-radius: 20px;
          transition: width 0.3s ease;
        }

        /* Question Card */

        .question-card {
          background: white;
          padding: 28px;
          margin-bottom: 22px;
          border-radius: 16px;
          border: 1px solid #e5e7eb;
          box-shadow: 0 3px 12px rgba(0,0,0,0.04);
        }

        .question-number {
          display: inline-block;
          background: #eef2ff;
          color: #4f46e5;
          padding: 6px 12px;
          border-radius: 20px;
          font-size: 13px;
          font-weight: 600;
          margin-bottom: 14px;
        }

        .question-card h2 {
          font-size: 20px;
          margin: 5px 0 7px;
          color: #111827;
        }

        .concept {
          font-size: 13px;
          color: #94a3b8;
          margin-bottom: 20px;
        }

        /* Options */

        .options {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 12px;
        }

        .option {
          display: flex;
          align-items: center;
          gap: 12px;
          padding: 15px;
          border: 1px solid #e2e8f0;
          border-radius: 10px;
          cursor: pointer;
          transition: 0.2s;
          background: #fff;
        }

        .option:hover {
          border-color: #818cf8;
          background: #f8faff;
        }

        .option.selected {
          border-color: #6366f1;
          background: #eef2ff;
          color: #4338ca;
          font-weight: 600;
        }

        .option input {
          accent-color: #6366f1;
          width: 17px;
          height: 17px;
        }

        /* Submit */

        .submit-section {
          text-align: center;
          margin-top: 30px;
        }

        .submit-diagnostic {
          border: none;
          background: #4f46e5;
          color: white;
          padding: 15px 30px;
          border-radius: 10px;
          font-size: 16px;
          font-weight: 600;
          cursor: pointer;
          transition: 0.2s;
        }

        .submit-diagnostic:hover {
          background: #4338ca;
          transform: translateY(-1px);
        }

        .submit-diagnostic:disabled {
          opacity: 0.7;
          cursor: not-allowed;
        }

        /* Mobile */

        @media (max-width: 700px) {

          .page-header {
            padding: 0 20px;
          }

          .page-header nav {
            display: none;
          }

          .diagnostic-container {
            width: 92%;
            padding-top: 30px;
          }

          .diagnostic-heading h1 {
            font-size: 28px;
          }

          .options {
            grid-template-columns: 1fr;
          }

          .question-card {
            padding: 20px;
          }

        }

      `}</style>

    </div>
  );
}

export default Diagnostic;