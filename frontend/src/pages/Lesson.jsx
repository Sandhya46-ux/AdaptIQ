import { useParams, useNavigate } from "react-router-dom";

const lessons = {
  1: {
    name: "Fractions",
    level: "Foundation",
    icon: "🔴",
    description:
      "Understand how fractions represent parts of a whole and learn how to add and compare them.",
    objective:
      "By the end of this lesson, you will be able to understand and perform basic fraction operations.",
    concepts: [
      "Numerator and denominator",
      "Equivalent fractions",
      "Adding fractions",
      "Comparing fractions",
    ],
    example: {
      question: "What is 1/4 + 2/4?",
      steps: [
        "The denominators are the same: 4.",
        "Add the numerators: 1 + 2 = 3.",
        "Keep the denominator as 4.",
      ],
      answer: "3/4",
    },
  },

  2: {
    name: "Algebraic Expressions",
    level: "Practice",
    icon: "🟡",
    description:
      "Learn how variables, constants, and coefficients work together in algebraic expressions.",
    objective:
      "By the end of this lesson, you will be able to simplify basic algebraic expressions.",
    concepts: [
      "Variables",
      "Constants",
      "Coefficients",
      "Like terms",
    ],
    example: {
      question: "Simplify: 2x + 3x",
      steps: [
        "Identify the like terms: 2x and 3x.",
        "Add their coefficients: 2 + 3 = 5.",
        "Keep the variable x.",
      ],
      answer: "5x",
    },
  },

  3: {
    name: "Linear Equations",
    level: "Review",
    icon: "🟢",
    description:
      "Understand how to solve equations with one variable using simple algebraic operations.",
    objective:
      "By the end of this lesson, you will be able to solve basic linear equations.",
    concepts: [
      "Variables and constants",
      "Equality",
      "Inverse operations",
      "Solving for x",
    ],
    example: {
      question: "Solve: x + 5 = 12",
      steps: [
        "We need to isolate x.",
        "Subtract 5 from both sides.",
        "x = 12 - 5.",
      ],
      answer: "x = 7",
    },
  },

  4: {
    name: "Quadratic Equations",
    level: "Upcoming",
    icon: "🔵",
    description:
      "Learn the basic structure of quadratic equations and how factorization can be used to solve them.",
    objective:
      "By the end of this lesson, you will understand the basic process of solving simple quadratic equations.",
    concepts: [
      "Quadratic expressions",
      "Factors",
      "Factorization",
      "Roots of an equation",
    ],
    example: {
      question: "Solve: x² - 5x + 6 = 0",
      steps: [
        "Find two numbers whose product is 6.",
        "Their sum should be -5.",
        "The numbers are -2 and -3.",
      ],
      answer: "x = 2 or x = 3",
    },
  },
};

function Lesson() {
  const { id } = useParams();
  const navigate = useNavigate();

  const lesson = lessons[id] || lessons[1];

  return (
    <div className="lesson-page">

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

          <button onClick={() => navigate("/progress")}>
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


      {/* MAIN */}
      <main className="lesson-container">

        {/* HEADER */}
        <section className="lesson-header">

          <div className="lesson-breadcrumb">
            Learning Path → {lesson.name}
          </div>

          <div className="lesson-title-row">

            <div className="lesson-icon">
              {lesson.icon}
            </div>

            <div>
              <p className="card-label">
                {lesson.level}
              </p>

              <h1>
                {lesson.name}
              </h1>

              <p>
                {lesson.description}
              </p>
            </div>

          </div>

        </section>


        {/* LEARNING OBJECTIVE */}
        <section className="lesson-objective">

          <div className="objective-icon">
            🎯
          </div>

          <div>
            <p className="card-label">
              LEARNING OBJECTIVE
            </p>

            <h2>
              What you will learn
            </h2>

            <p>
              {lesson.objective}
            </p>
          </div>

        </section>


        {/* CONCEPTS */}
        <section className="lesson-card">

          <div className="lesson-section-heading">

            <div>
              <p className="card-label">
                CORE CONCEPTS
              </p>

              <h2>
                What you need to understand
              </h2>
            </div>

            <span className="ai-badge">
              ✨ Personalized
            </span>

          </div>


          <div className="concept-learning-grid">

            {lesson.concepts.map((concept, index) => (

              <div
                className="concept-learning-card"
                key={concept}
              >

                <div className="concept-index">
                  {index + 1}
                </div>

                <div>
                  <h3>
                    {concept}
                  </h3>

                  <p>
                    Build your understanding of {concept.toLowerCase()}.
                  </p>
                </div>

              </div>

            ))}

          </div>

        </section>


        {/* EXAMPLE */}
        <section className="lesson-card example-card">

          <div className="lesson-section-heading">

            <div>
              <p className="card-label">
                WORKED EXAMPLE
              </p>

              <h2>
                Let's solve one together ✏️
              </h2>
            </div>

          </div>


          <div className="example-question">

            <span>
              Question
            </span>

            <h3>
              {lesson.example.question}
            </h3>

          </div>


          <div className="example-steps">

            {lesson.example.steps.map((step, index) => (

              <div
                className="example-step"
                key={index}
              >

                <div className="step-number">
                  {index + 1}
                </div>

                <p>
                  {step}
                </p>

              </div>

            ))}

          </div>


          <div className="example-answer">

            <span>
              ✓ Answer
            </span>

            <strong>
              {lesson.example.answer}
            </strong>

          </div>

        </section>


        {/* AI TUTOR */}
        <section className="lesson-ai-card">

          <div className="lesson-ai-icon">
            🤖
          </div>

          <div className="lesson-ai-content">

            <p className="card-label">
              ADAPTIQ AI TUTOR
            </p>

            <h2>
              Need help understanding this concept?
            </h2>

            <p>
              Ask the AI Tutor for a simpler explanation, a hint,
              or another example based on your learning level.
            </p>

          </div>

          <button
            onClick={() => navigate("/tutor")}
          >
            Ask AI Tutor →
          </button>

        </section>


        {/* COMPLETE */}
        <section className="lesson-footer">

          <div>

            <h2>
              Ready to test your understanding? 🎯
            </h2>

            <p>
              Take a short adaptive quiz and let AdaptIQ update
              your mastery.
            </p>

          </div>

          <button
            onClick={() => navigate("/quiz", {
              state: {
                concept: lesson.name,
                lessonId: id
              }
            })}
          >
            Start Adaptive Quiz →
          </button>

        </section>

      </main>

    </div>
  );
}

export default Lesson;