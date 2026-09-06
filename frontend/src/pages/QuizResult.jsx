import { useLocation, useNavigate } from "react-router-dom";

function QuizResult() {
  const location = useLocation();
  const navigate = useNavigate();

  const concept =
    location.state?.concept || "Fractions";

  const score =
    location.state?.score ?? 2;

  const total =
    location.state?.total ?? 3;

  const percentage =
    location.state?.percentage ??
    Math.round((score / total) * 100);


  /* ==========================================
     PREVIOUS MASTERY
  ========================================== */

  const previousMastery = {
    Fractions: 25,
    "Algebraic Expressions": 68,
    "Linear Equations": 72,
    "Quadratic Equations": 0,
  };

  const oldMastery =
    previousMastery[concept] ?? 25;


  /* ==========================================
     UPDATED MASTERY
  ========================================== */

  const masteryIncrease = Math.max(
    5,
    Math.round(percentage * 0.2)
  );

  const updatedMastery = Math.min(
    100,
    oldMastery + masteryIncrease
  );

  const masteryImproved =
    updatedMastery - oldMastery;


  /* ==========================================
     PERFORMANCE
  ========================================== */

  let performanceTitle;
  let performanceMessage;

  if (percentage >= 80) {

    performanceTitle =
      "Excellent understanding! 🎉";

    performanceMessage =
      `You demonstrated strong understanding of ${concept}. AdaptIQ can now move you toward more advanced concepts.`;

  } else if (percentage >= 50) {

    performanceTitle =
      "Good progress! 👍";

    performanceMessage =
      `You understand the basics of ${concept}, but a little more practice will help strengthen your mastery.`;

  } else {

    performanceTitle =
      "Let's strengthen the foundation. 💡";

    performanceMessage =
      `Your answers suggest that ${concept} needs more practice before moving to advanced concepts.`;
  }


  /* ==========================================
     MISCONCEPTION
  ========================================== */

  let misconception;

  if (concept === "Fractions") {

    misconception =
      "You may be confusing how numerators and denominators are handled during fraction operations.";

  } else if (
    concept === "Algebraic Expressions"
  ) {

    misconception =
      "You may need more practice identifying and combining like terms.";

  } else if (
    concept === "Linear Equations"
  ) {

    misconception =
      "You may need more practice applying inverse operations to isolate the variable.";

  } else {

    misconception =
      "You may need more practice identifying the correct factors when solving quadratic equations.";
  }


  /* ==========================================
     INTERVENTION
  ========================================== */

  let intervention;

  if (percentage < 50) {

    intervention =
      "Review the foundation concept";

  } else if (percentage < 80) {

    intervention =
      "Practice with targeted examples";

  } else {

    intervention =
      "Move to the next concept";
  }


  /* ==========================================
     LESSON ID
  ========================================== */

  let lessonId = 1;

  if (concept === "Algebraic Expressions") {
    lessonId = 2;
  }

  if (concept === "Linear Equations") {
    lessonId = 3;
  }

  if (concept === "Quadratic Equations") {
    lessonId = 4;
  }


  return (
    <div className="quiz-result-page">

      {/* ======================================
          NAVBAR
      ====================================== */}

      <nav className="dashboard-navbar">

        <div
          className="dashboard-logo"
          onClick={() =>
            navigate("/dashboard")
          }
          style={{
            cursor: "pointer",
          }}
        >
          Adapt<span>IQ</span> 🧠
        </div>


        <div className="nav-links">

          <button
            onClick={() =>
              navigate("/dashboard")
            }
          >
            Dashboard
          </button>

          <button
            onClick={() =>
              navigate("/learning-path")
            }
          >
            Learning Path
          </button>

          <button
            onClick={() =>
              navigate("/progress")
            }
          >
            Progress
          </button>

          <button
            onClick={() =>
              navigate("/tutor")
            }
          >
            AI Tutor
          </button>

        </div>


        <div className="student-info">
          👩‍🎓 Student
        </div>

      </nav>


      {/* ======================================
          MAIN
      ====================================== */}

      <main className="quiz-result-container">


        {/* HEADER */}

        <section className="quiz-result-header">

          <div className="result-success-icon">
            🎯
          </div>

          <p className="card-label">
            ADAPTIVE QUIZ COMPLETE
          </p>

          <h1>
            Here's what AdaptIQ learned 🧠
          </h1>

          <p>
            Your quiz performance has been analyzed
            to update your learning profile.
          </p>

        </section>


        {/* SCORE */}

        <section className="quiz-score-card">

          <div className="quiz-score-circle">

            <div>

              <strong>
                {percentage}%
              </strong>

              <span>
                Score
              </span>

            </div>

          </div>


          <div className="quiz-score-details">

            <p className="card-label">
              {concept.toUpperCase()}
            </p>

            <h2>
              {score} out of {total} correct
            </h2>

            <p>
              {performanceMessage}
            </p>

          </div>

        </section>


        {/* PERFORMANCE */}

        <section className="performance-card">

          <div className="performance-icon">
            {percentage >= 80
              ? "🎉"
              : percentage >= 50
              ? "👍"
              : "💡"}
          </div>


          <div>

            <p className="card-label">
              PERFORMANCE INSIGHT
            </p>

            <h2>
              {performanceTitle}
            </h2>

            <p>
              {performanceMessage}
            </p>

          </div>

        </section>


        {/* MASTERY */}

        <section className="mastery-update-card">

          <div className="result-section-heading">

            <div>

              <p className="card-label">
                LEARNER MODEL UPDATED
              </p>

              <h2>
                Your mastery has changed 📈
              </h2>

            </div>


            <span className="ai-result-badge">
              ✨ AI ANALYZED
            </span>

          </div>


          <div className="mastery-comparison">

            <div className="mastery-box">

              <span>
                Before Quiz
              </span>

              <strong>
                {oldMastery}%
              </strong>

            </div>


            <div className="mastery-arrow">
              →
            </div>


            <div className="mastery-box updated">

              <span>
                After Quiz
              </span>

              <strong>
                {updatedMastery}%
              </strong>

            </div>


            <div className="mastery-growth">

              <span>
                Improvement
              </span>

              <strong>
                +{masteryImproved}%
              </strong>

            </div>

          </div>


          <div className="result-mastery-progress">

            <div className="result-progress-label">

              <span>
                {concept} mastery
              </span>

              <span>
                {updatedMastery}%
              </span>

            </div>


            <div className="result-progress-track">

              <div
                className="result-progress-fill"
                style={{
                  width: `${updatedMastery}%`,
                }}
              ></div>

            </div>

          </div>

        </section>


        {/* MISCONCEPTION */}

        <section className="misconception-card">

          <div className="misconception-icon">
            ⚠️
          </div>


          <div className="misconception-content">

            <p className="card-label">
              MISCONCEPTION DETECTED
            </p>

            <h2>
              A learning gap was identified
            </h2>

            <p>
              {misconception}
            </p>

          </div>

        </section>


        {/* INTERVENTION */}

        <section className="intervention-card">

          <div className="intervention-icon">
            💡
          </div>


          <div className="intervention-content">

            <p className="card-label">
              ADAPTIQ INTERVENTION
            </p>

            <h2>
              {intervention}
            </h2>

            <p>
              Based on your performance,
              AdaptIQ recommends a targeted
              learning activity before deciding
              what you should learn next.
            </p>

          </div>


          <button
            onClick={() =>
              navigate(
                `/lesson/${lessonId}`
              )
            }
          >
            Review Concept →
          </button>

        </section>


        {/* NEXT STEP */}

        <section className="next-learning-card">

          <div>

            <p className="card-label">
              RECOMMENDED NEXT STEP
            </p>

            <h2>
              Continue your personalized
              journey 🚀
            </h2>

            <p>
              Your learning path will adapt
              based on your updated mastery
              and identified gaps.
            </p>

          </div>


          <button
            onClick={() =>
              navigate(
                "/learning-path"
              )
            }
          >
            View Updated Path →
          </button>

        </section>

      </main>

    </div>
  );
}

export default QuizResult;