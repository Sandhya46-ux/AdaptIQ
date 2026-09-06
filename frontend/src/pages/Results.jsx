import { useLocation, useNavigate } from "react-router-dom";

function Results() {
  const location = useLocation();
  const navigate = useNavigate();

  // Data coming from Diagnostic.jsx
  const score = location.state?.score ?? 2;
  const total = location.state?.total ?? 4;

  const mastery = location.state?.mastery ?? {
    Fractions: 0,
    "Linear Equations": 100,
    "Algebraic Expressions": 100,
    "Quadratic Equations": 0
  };

  const percentage = Math.round((score / total) * 100);

  // Find weak concepts
  const weakConcepts = Object.entries(mastery)
    .filter(([_, value]) => value < 50)
    .map(([concept]) => concept);

  // Find medium concepts
  const mediumConcepts = Object.entries(mastery)
    .filter(([_, value]) => value >= 50 && value < 80)
    .map(([concept]) => concept);

  // Find strong concepts
  const strongConcepts = Object.entries(mastery)
    .filter(([_, value]) => value >= 80)
    .map(([concept]) => concept);

  return (
    <div className="results-page">

      {/* ================= NAVBAR ================= */}

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


      {/* ================= MAIN ================= */}

      <main className="results-container">

        {/* Header */}

        <section className="results-header">

          <div className="result-success-icon">
            🎯
          </div>

          <p className="card-label">
            ASSESSMENT COMPLETE
          </p>

          <h1>
            Here's what we learned about you 🧠
          </h1>

          <p>
            AdaptIQ analyzed your answers to understand
            your current knowledge and learning gaps.
          </p>

        </section>


        {/* ================= SCORE ================= */}

        <section className="score-card">

          <div className="score-circle">

            <div>
              <strong>{percentage}%</strong>
              <span>Score</span>
            </div>

          </div>

          <div className="score-details">

            <p className="card-label">
              DIAGNOSTIC RESULT
            </p>

            <h2>
              {score} out of {total} correct
            </h2>

            <p>
              Your result helps AdaptIQ create a
              learning path specifically for you.
            </p>

          </div>

        </section>


        {/* ================= KNOWLEDGE MAP ================= */}

        <section className="knowledge-section">

          <div className="section-heading">

            <div>
              <p className="card-label">
                KNOWLEDGE MAP
              </p>

              <h2>
                Your Concept Mastery
              </h2>
            </div>

            <span className="ai-badge">
              ✨ AI ANALYZED
            </span>

          </div>


          <div className="concept-grid">

            {Object.entries(mastery).map(
              ([concept, value]) => {

                let status = "Strong";
                let statusClass = "strong";

                if (value < 50) {
                  status = "Needs Attention";
                  statusClass = "weak";
                } else if (value < 80) {
                  status = "Needs Practice";
                  statusClass = "medium";
                }

                return (

                  <div
                    className="concept-card"
                    key={concept}
                  >

                    <div className="concept-top">

                      <div>
                        <h3>{concept}</h3>

                        <span
                          className={`concept-status ${statusClass}`}
                        >
                          {status}
                        </span>
                      </div>

                      <strong
                        className={`concept-score ${statusClass}`}
                      >
                        {value}%
                      </strong>

                    </div>


                    <div className="concept-progress">

                      <div
                        className={`concept-progress-fill ${statusClass}`}
                        style={{
                          width: `${value}%`
                        }}
                      ></div>

                    </div>

                  </div>

                );
              }
            )}

          </div>

        </section>


        {/* ================= GAP DETECTION ================= */}

        <section className="gap-card">

          <div className="gap-icon">
            ⚠️
          </div>

          <div className="gap-content">

            <p className="card-label">
              PREREQUISITE GAP DETECTED
            </p>

            <h2>
              {weakConcepts.length > 0
                ? `Let's strengthen ${weakConcepts[0]} first.`
                : "Your foundation looks strong!"}
            </h2>

            <p>

              {weakConcepts.length > 0
                ? `Your diagnostic responses suggest that ${weakConcepts[0]} needs more attention. Strengthening this foundation can help you perform better in advanced concepts.`
                : "You demonstrated strong understanding across the assessed concepts. AdaptIQ can now move you toward more advanced learning."}

            </p>

          </div>

        </section>


        {/* ================= INSIGHTS ================= */}

        <section className="insights-grid">

          <div className="insight-box">

            <span className="insight-number">
              🔴
            </span>

            <div>

              <h3>
                Needs Attention
              </h3>

              <p>
                {weakConcepts.length > 0
                  ? weakConcepts.join(", ")
                  : "None detected"}
              </p>

            </div>

          </div>


          <div className="insight-box">

            <span className="insight-number">
              🟡
            </span>

            <div>

              <h3>
                Practice Recommended
              </h3>

              <p>
                {mediumConcepts.length > 0
                  ? mediumConcepts.join(", ")
                  : "None detected"}
              </p>

            </div>

          </div>


          <div className="insight-box">

            <span className="insight-number">
              🟢
            </span>

            <div>

              <h3>
                Strong Concepts
              </h3>

              <p>
                {strongConcepts.length > 0
                  ? strongConcepts.join(", ")
                  : "None detected"}
              </p>

            </div>

          </div>

        </section>


        {/* ================= ACTION ================= */}

        <section className="results-action">

          <h2>
            Ready for your personalized path? 🎯
          </h2>

          <p>
            AdaptIQ will use your results to decide
            what you should learn next.
          </p>

          <button
            className="primary-result-button"
            onClick={() => navigate("/learning-path")}
          >
            Generate My Learning Path →
          </button>

        </section>

      </main>

    </div>
  );
}

export default Results;