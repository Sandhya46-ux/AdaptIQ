import { useNavigate } from "react-router-dom";

function Dashboard() {
  const navigate = useNavigate();

  // Get logged-in student information
  const user = JSON.parse(
    localStorage.getItem("adaptIQUser") || "{}"
  );

  const username = user.username || "Student";

  return (
    <div className="dashboard-page">

      {/* ================= NAVBAR ================= */}

      <nav className="dashboard-navbar">

        {/* Logo */}
        <div className="dashboard-logo">
          Adapt<span>IQ</span> 🧠
        </div>

        {/* Navigation */}
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

        {/* ================= CLICKABLE PROFILE ================= */}

        <button
          className="student-profile-button"
          onClick={() => navigate("/learner-profile")}
          title="Open your profile"
        >

          <div className="student-avatar">
            👩‍🎓
          </div>

          <div className="student-profile-name">
            {username}
          </div>

        </button>

      </nav>


      {/* ================= MAIN CONTENT ================= */}

      <main className="dashboard-container">

        {/* ================= WELCOME SECTION ================= */}

        <section className="welcome-section">

          <div>

            <p className="welcome-label">
              Welcome back to AdaptIQ 👋
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

          {/* Overall Mastery */}

          <div className="stat-card">

            <div className="stat-icon">
              🎯
            </div>

            <div>

              <p>
                Overall Mastery
              </p>

              <h2>
                72%
              </h2>

            </div>

          </div>


          {/* Topics Completed */}

          <div className="stat-card">

            <div className="stat-icon">
              📚
            </div>

            <div>

              <p>
                Topics Completed
              </p>

              <h2>
                12
              </h2>

            </div>

          </div>


          {/* Learning Streak */}

          <div className="stat-card">

            <div className="stat-icon">
              🔥
            </div>

            <div>

              <p>
                Learning Streak
              </p>

              <h2>
                7 Days
              </h2>

            </div>

          </div>


          {/* Quiz Accuracy */}

          <div className="stat-card">

            <div className="stat-icon">
              📝
            </div>

            <div>

              <p>
                Quiz Accuracy
              </p>

              <h2>
                84%
              </h2>

            </div>

          </div>

        </section>


        {/* ================= MAIN GRID ================= */}

        <section className="dashboard-grid">


          {/* ================= CURRENT LEARNING ================= */}

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
                style={{
                  width: "72%"
                }}
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


          {/* ================= AI RECOMMENDATION ================= */}

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


            {/* Fractions */}

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


            {/* Algebra */}

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


      {/* ================= PROFILE STYLES ================= */}

      <style>{`

        /* Clickable student profile */

        .student-profile-button {
          display: flex;
          align-items: center;
          gap: 10px;

          border: none;
          background: transparent;

          padding: 6px 10px;
          border-radius: 12px;

          cursor: pointer;

          transition: all 0.2s ease;
        }


        .student-profile-button:hover {
          background: #f1f5f9;
          transform: translateY(-1px);
        }


        /* Student circular avatar */

        .student-avatar {
          width: 42px;
          height: 42px;

          display: flex;
          align-items: center;
          justify-content: center;

          border-radius: 50%;

          background: #eef2ff;

          font-size: 23px;

          border: 2px solid #c7d2fe;

          transition: all 0.2s ease;
        }


        .student-profile-button:hover .student-avatar {
          background: #e0e7ff;
          border-color: #818cf8;
        }


        /* Username */

        .student-profile-name {
          max-width: 130px;

          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;

          color: #475569;

          font-size: 16px;
          font-weight: 700;
        }


        /* Mobile */

        @media (max-width: 700px) {

          .student-profile-name {
            display: none;
          }

          .student-profile-button {
            padding: 4px;
          }

          .student-avatar {
            width: 40px;
            height: 40px;
            font-size: 21px;
          }

        }

      `}</style>

    </div>
  );
}

export default Dashboard;