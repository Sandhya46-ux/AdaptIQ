import { useNavigate } from "react-router-dom";

function Progress() {
  const navigate = useNavigate();

  const concepts = [
    {
      name: "Fractions",
      mastery: 45,
      status: "Needs Practice",
      statusClass: "weak",
    },
    {
      name: "Algebraic Expressions",
      mastery: 68,
      status: "Improving",
      statusClass: "medium",
    },
    {
      name: "Linear Equations",
      mastery: 78,
      status: "Good",
      statusClass: "strong",
    },
    {
      name: "Quadratic Equations",
      mastery: 30,
      status: "Needs Attention",
      statusClass: "weak",
    },
  ];

  return (
    <div className="progress-page">

      {/* NAVBAR */}
      <nav className="dashboard-navbar">

        <div
          className="dashboard-logo"
          onClick={() => navigate("/dashboard")}
          style={{ cursor: "pointer" }}
        >
          Adapt<span>IQ</span> 🧠
        </div>

        <div className="nav-links">
          <button onClick={() => navigate("/dashboard")}>
            Dashboard
          </button>

          <button onClick={() => navigate("/learning-path")}>
            Learning Path
          </button>

          <button className="active-nav">
            Progress
          </button>

          <button onClick={() => navigate("/tutor")}>
            AI Tutor
          </button>
        </div>

        <div className="student-info">
          👩‍🎓 Student
        </div>

      </nav>

      {/* MAIN CONTENT */}
      <main className="progress-container">

        {/* HEADER */}
        <section className="progress-header">

          <div>
            <p className="card-label">
              LEARNING ANALYTICS
            </p>

            <h1>
              Your Learning Progress 📈
            </h1>

            <p>
              Track your mastery, identify learning gaps,
              and see how AdaptIQ is improving your learning path.
            </p>
          </div>

          <div className="progress-header-icon">
            📊
          </div>

        </section>


        {/* OVERALL MASTERY */}
        <section className="overall-mastery-card">

          <div className="mastery-card-top">

            <div>
              <p className="card-label">
                OVERALL MASTERY
              </p>

              <h2>
                72%
              </h2>

              <p>
                Your overall understanding across all concepts
              </p>
            </div>

            <div className="mastery-circle">
              <span>72%</span>
            </div>

          </div>

          <div className="mastery-progress-track">
            <div
              className="mastery-progress-fill"
              style={{ width: "72%" }}
            ></div>
          </div>

          <div className="mastery-footer">
            <span>Starting point: 48%</span>
            <strong>+24% improvement</strong>
          </div>

        </section>


        {/* CONCEPT MASTERY */}
        <section className="concept-section">

          <div className="section-heading">

            <div>
              <p className="card-label">
                CONCEPT MASTERY
              </p>

              <h2>
                How well do you understand each topic?
              </h2>
            </div>

          </div>


          <div className="concept-grid">

            {concepts.map((concept) => (

              <div
                className="concept-progress-card"
                key={concept.name}
              >

                <div className="concept-card-header">

                  <div>
                    <h3>
                      {concept.name}
                    </h3>

                    <span
                      className={`concept-status ${concept.statusClass}`}
                    >
                      {concept.status}
                    </span>
                  </div>

                  <strong>
                    {concept.mastery}%
                  </strong>

                </div>


                <div className="concept-progress-track">

                  <div
                    className={`concept-progress-fill ${concept.statusClass}`}
                    style={{
                      width: `${concept.mastery}%`,
                    }}
                  ></div>

                </div>


                <div className="concept-card-footer">

                  {concept.mastery < 50 ? (
                    <span>
                      ⚠️ More practice recommended
                    </span>
                  ) : concept.mastery < 80 ? (
                    <span>
                      📈 Keep practicing
                    </span>
                  ) : (
                    <span>
                      ✅ Strong understanding
                    </span>
                  )}

                </div>

              </div>

            ))}

          </div>

        </section>


        {/* LEARNING TREND */}
        <section className="learning-trend-card">

          <div className="trend-header">

            <div>
              <p className="card-label">
                LEARNING TREND
              </p>

              <h2>
                Your mastery is improving
              </h2>

              <p>
                AdaptIQ continuously updates your learner profile
                based on your assessments and practice.
              </p>
            </div>

            <div className="trend-badge">
              ↗️ +24%
            </div>

          </div>


          <div className="trend-chart">

            <div className="chart-y-axis">
              <span>100%</span>
              <span>75%</span>
              <span>50%</span>
              <span>25%</span>
              <span>0%</span>
            </div>

            <div className="chart-area">

              <div className="chart-line">

                <div className="chart-point point-1">
                  <span>48%</span>
                </div>

                <div className="chart-point point-2">
                  <span>55%</span>
                </div>

                <div className="chart-point point-3">
                  <span>61%</span>
                </div>

                <div className="chart-point point-4">
                  <span>68%</span>
                </div>

                <div className="chart-point point-5">
                  <span>72%</span>
                </div>

              </div>

              <div className="chart-labels">
                <span>Week 1</span>
                <span>Week 2</span>
                <span>Week 3</span>
                <span>Week 4</span>
                <span>Current</span>
              </div>

            </div>

          </div>

        </section>


        {/* AI INSIGHT */}
        <section className="progress-ai-insight">

          <div className="ai-insight-icon">
            🧠
          </div>

          <div className="ai-insight-content">

            <p className="card-label">
              ADAPTIQ INSIGHT
            </p>

            <h2>
              Your learning pattern
            </h2>

            <p>
              Your Linear Equations mastery has improved significantly.
              However, Fractions and Quadratic Equations remain areas
              that need attention.
            </p>

            <div className="insight-recommendation">

              <span>
                🎯 Recommended next step
              </span>

              <strong>
                Review Fractions before continuing with advanced equations.
              </strong>

            </div>

          </div>

        </section>


        {/* ACTIONS */}
        <section className="progress-actions">

          <button
            className="secondary-action-button"
            onClick={() => navigate("/learning-path")}
          >
            ← View Learning Path
          </button>

          <button
            className="primary-action-button"
            onClick={() => navigate("/tutor")}
          >
            Ask AI Tutor →
          </button>

        </section>

      </main>

    </div>
  );
}

export default Progress;