import { useNavigate } from "react-router-dom";

function Dashboard() {
  const navigate = useNavigate();

  return (
    <div className="dashboard-page">

      {/* ================= NAVBAR ================= */}

      <nav className="dashboard-navbar">

        <div className="dashboard-logo">
          Adapt<span>IQ</span> 🧠
        </div>

        <div className="nav-links">

          <button className="active">
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
          👩‍🎓 <span>Student</span>
        </div>

      </nav>


      {/* ================= MAIN CONTENT ================= */}

      <main className="dashboard-container">

        {/* Welcome Section */}

        <section className="welcome-section">

          <div>

            <p className="welcome-label">
              Welcome back 👋
            </p>

            <h1>
              Ready to learn smarter?
            </h1>

            <p className="welcome-text">
              AdaptIQ has personalized your learning
              journey based on your strengths and
              learning gaps.
            </p>

          </div>

          <button
            className="diagnostic-button"
            onClick={() => navigate("/diagnostic")}
          >
            Take Diagnostic Test →
          </button>

        </section>


        {/* ================= STATS ================= */}

        <section className="stats-grid">

          <div className="stat-card">

            <div className="stat-icon">
              🎯
            </div>

            <div>
              <p>Overall Mastery</p>
              <h2>72%</h2>
            </div>

          </div>


          <div className="stat-card">

            <div className="stat-icon">
              📚
            </div>

            <div>
              <p>Topics Completed</p>
              <h2>12</h2>
            </div>

          </div>


          <div className="stat-card">

            <div className="stat-icon">
              🔥
            </div>

            <div>
              <p>Learning Streak</p>
              <h2>7 Days</h2>
            </div>

          </div>


          <div className="stat-card">

            <div className="stat-icon">
              📝
            </div>

            <div>
              <p>Quiz Accuracy</p>
              <h2>84%</h2>
            </div>

          </div>

        </section>


        {/* ================= MAIN GRID ================= */}

        <section className="dashboard-grid">


          {/* Current Learning */}

          <div className="dashboard-card">

            <div className="card-header">

              <div>
                <p className="card-label">
                  CURRENT LEARNING
                </p>

                <h2>
                  Linear Equations
                </h2>
              </div>

              <span className="status-badge">
                In Progress
              </span>

            </div>


            <p className="card-description">
              Continue your personalized lesson
              on solving linear equations.
            </p>


            <div className="mastery-info">

              <span>
                Mastery
              </span>

              <strong>
                72%
              </strong>

            </div>


            <div className="progress-track">

              <div
                className="progress-fill"
                style={{ width: "72%" }}
              ></div>

            </div>


            <button
              className="card-button"
              onClick={() =>
                navigate("/lesson/linear-equations")
              }
            >
              Continue Lesson →
            </button>

          </div>


          {/* Recommended */}

          <div className="dashboard-card">

            <div className="card-header">

              <div>
                <p className="card-label">
                  AI RECOMMENDATION
                </p>

                <h2>
                  Focus Areas
                </h2>
              </div>

              <span className="ai-badge">
                ✨ AI
              </span>

            </div>


            <p className="card-description">
              Based on your recent performance,
              AdaptIQ recommends strengthening
              these concepts.
            </p>


            <div className="recommendation-item">

              <div className="recommendation-icon">
                ⚠️
              </div>

              <div>
                <strong>
                  Fractions
                </strong>

                <p>
                  Prerequisite gap
                </p>
              </div>

              <span className="weak-score">
                45%
              </span>

            </div>


            <div className="recommendation-item">

              <div className="recommendation-icon">
                📖
              </div>

              <div>
                <strong>
                  Algebraic Expressions
                </strong>

                <p>
                  Practice recommended
                </p>
              </div>

              <span className="medium-score">
                68%
              </span>

            </div>


            <button
              className="card-button secondary"
              onClick={() =>
                navigate("/learning-path")
              }
            >
              View Personalized Path →
            </button>

          </div>

        </section>


        {/* ================= LEARNING INSIGHT ================= */}

        <section className="insight-card">

          <div className="insight-icon">
            🧠
          </div>

          <div>

            <p className="card-label">
              ADAPTIQ INSIGHT
            </p>

            <h2>
              Your learning path adapts to you.
            </h2>

            <p>
              You are strong in Linear Equations,
              but improving your understanding of
              Fractions can help strengthen your
              Algebra foundation.
            </p>

          </div>

        </section>

      </main>

    </div>
  );
}

export default Dashboard;