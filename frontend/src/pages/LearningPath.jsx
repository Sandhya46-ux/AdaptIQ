import { useLocation, useNavigate } from "react-router-dom";

function LearningPath() {
  const navigate = useNavigate();
  const location = useLocation();

  // Receive mastery from Results page
  const mastery = location.state?.mastery || {
    Fractions: 0,
    "Algebraic Expressions": 100,
    "Linear Equations": 100,
    "Quadratic Equations": 0,
  };

  // Create learning path
  const topics = [
    {
      id: 1,
      name: "Fractions",
      description:
        "Strengthen your foundation with fractions before moving to advanced algebra.",
      mastery: mastery["Fractions"] ?? 0,
      priority: "High Priority",
      status: "Start Here",
      icon: "🔴",
    },
    {
      id: 2,
      name: "Algebraic Expressions",
      description:
        "Practice simplifying and manipulating algebraic expressions.",
      mastery: mastery["Algebraic Expressions"] ?? 0,
      priority: "Medium Priority",
      status: "Practice",
      icon: "🟡",
    },
    {
      id: 3,
      name: "Linear Equations",
      description:
        "Build confidence in solving equations with one variable.",
      mastery: mastery["Linear Equations"] ?? 0,
      priority: "Ready",
      status: "Continue",
      icon: "🟢",
    },
    {
      id: 4,
      name: "Quadratic Equations",
      description:
        "Move to quadratic equations after strengthening your foundation.",
      mastery: mastery["Quadratic Equations"] ?? 0,
      priority: "Next Topic",
      status: "Upcoming",
      icon: "🔵",
    },
  ];

  return (
    <div className="learning-path-page">

      {/* ================= NAVBAR ================= */}

      <nav className="dashboard-navbar">

        <div
          className="dashboard-logo"
          onClick={() => navigate("/dashboard")}
        >
          Adapt<span>IQ</span> 🧠
        </div>

        <div className="nav-links">

          <button
            onClick={() => navigate("/dashboard")}
          >
            Dashboard
          </button>

          <button className="active">
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


      {/* ================= MAIN ================= */}

      <main className="learning-path-container">

        {/* Header */}

        <section className="learning-path-header">

          <div>

            <p className="card-label">
              PERSONALIZED LEARNING
            </p>

            <h1>
              Your Learning Path 🎯
            </h1>

            <p>
              AdaptIQ has arranged your learning journey
              based on your current mastery and knowledge gaps.
            </p>

          </div>

          <div className="path-ai-badge">
            ✨ AI Personalized
          </div>

        </section>


        {/* ================= AI INSIGHT ================= */}

        <section className="path-insight">

          <div className="path-insight-icon">
            🧠
          </div>

          <div>

            <p className="card-label">
              ADAPTIQ RECOMMENDATION
            </p>

            <h2>
              Start with your foundation
            </h2>

            <p>
              Your diagnostic shows that some prerequisite
              concepts need strengthening. AdaptIQ prioritizes
              these topics before moving you to more advanced
              concepts.
            </p>

          </div>

        </section>


        {/* ================= LEARNING PATH ================= */}

        <section className="learning-path-section">

          <div className="path-section-title">

            <div>
              <p className="card-label">
                YOUR JOURNEY
              </p>

              <h2>
                Follow this path
              </h2>
            </div>

            <span>
              4 Concepts
            </span>

          </div>


          <div className="learning-timeline">

            {topics.map((topic, index) => (

              <div
                className="timeline-item"
                key={topic.id}
              >

                {/* Timeline */}

                <div className="timeline-side">

                  <div className="timeline-number">
                    {index + 1}
                  </div>

                  {index !== topics.length - 1 && (
                    <div className="timeline-line"></div>
                  )}

                </div>


                {/* Card */}

                <div
                  className={`learning-topic-card ${
                    topic.mastery < 50
                      ? "high-priority"
                      : ""
                  }`}
                >

                  <div className="topic-top">

                    <div className="topic-title">

                      <span className="topic-icon">
                        {topic.icon}
                      </span>

                      <div>

                        <h2>
                          {topic.name}
                        </h2>

                        <span
                          className={`topic-priority ${
                            topic.mastery < 50
                              ? "priority-high"
                              : topic.mastery < 80
                              ? "priority-medium"
                              : "priority-low"
                          }`}
                        >
                          {topic.priority}
                        </span>

                      </div>

                    </div>


                    <div className="topic-mastery">

                      <strong>
                        {topic.mastery}%
                      </strong>

                      <span>
                        Mastery
                      </span>

                    </div>

                  </div>


                  <p className="topic-description">
                    {topic.description}
                  </p>


                  {/* Progress */}

                  <div className="topic-progress-info">

                    <span>
                      Current mastery
                    </span>

                    <span>
                      {topic.mastery}%
                    </span>

                  </div>

                  <div className="topic-progress">

                    <div
                      className={`topic-progress-fill ${
                        topic.mastery < 50
                          ? "fill-low"
                          : topic.mastery < 80
                          ? "fill-medium"
                          : "fill-high"
                      }`}
                      style={{
                        width: `${topic.mastery}%`,
                      }}
                    ></div>

                  </div>


                  {/* Action */}

                  <div className="topic-bottom">

                    <span>
                      {topic.status}
                    </span>

                    <button
                      onClick={() =>
                        navigate(
                          `/lesson/${topic.id}`
                        )
                      }
                    >
                      {topic.mastery < 50
                        ? "Start Learning →"
                        : topic.mastery < 80
                        ? "Practice →"
                        : "Review →"}
                    </button>

                  </div>

                </div>

              </div>

            ))}

          </div>

        </section>


        {/* ================= BOTTOM ================= */}

        <section className="path-footer">

          <div>

            <h2>
              Learning path adapts as you learn. 🔄
            </h2>

            <p>
              Your mastery will be updated after every
              lesson and quiz. AdaptIQ can then adjust
              what you should learn next.
            </p>

          </div>

          <button
            onClick={() => navigate("/dashboard")}
          >
            Back to Dashboard
          </button>

        </section>

      </main>

    </div>
  );
}

export default LearningPath;