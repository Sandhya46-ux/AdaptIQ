import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";

function Tutor() {
  const navigate = useNavigate();
  const location = useLocation();

  const concept = location.state?.concept || "Linear Equations";
  const mastery = location.state?.mastery || 72;

  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: "ai",
      text: `Hi! 👋 I'm your AdaptIQ AI Tutor. I know you're currently working on ${concept}. Let's learn it step by step.`,
    },
    {
      id: 2,
      sender: "ai",
      text:
        "You can ask me a question, request a hint, or ask me to explain a concept differently. I will guide you instead of simply giving you the answer.",
    },
  ]);

  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [language, setLanguage] = useState("English");

  const generateResponse = (userMessage) => {
    const message = userMessage.toLowerCase();

    if (
      message.includes("hint") ||
      message.includes("help") ||
      message.includes("stuck")
    ) {
      return `💡 Here's a hint:

Don't try to solve everything at once.

For ${concept}, first identify what is known and what you need to find. Then perform one operation at a time.

Try the next step yourself and I'll check your reasoning.`;
    }

    if (
      message.includes("explain") ||
      message.includes("understand") ||
      message.includes("confused")
    ) {
      return `📚 Let's simplify ${concept}.

Think of the concept as a sequence of small steps rather than one big problem.

Your current mastery is ${mastery}%, so I'll keep the explanation at a level that helps strengthen your understanding.

Would you like to try a simple example next?`;
    }

    if (
      message.includes("example") ||
      message.includes("practice")
    ) {
      return `🎯 Let's practice.

Try this:

Solve:
x + 7 = 15

Don't worry about getting it right immediately.

Think about what operation can isolate x.

Send me your answer and I'll guide you through it.`;
    }

    if (
      message.includes("fraction") ||
      message.includes("fractions")
    ) {
      return `🧩 Fractions are an important prerequisite for several algebra concepts.

Remember:

When adding or subtracting fractions, first make sure they have a common denominator.

For example:

1/4 + 2/4 = 3/4

Would you like a practice question on fractions?`;
    }

    if (
      message.includes("linear equation") ||
      message.includes("linear equations")
    ) {
      return `🧠 A linear equation is an equation where the variable has a power of 1.

For example:

x + 5 = 12

The goal is to isolate x.

Ask yourself:
"What operation can remove +5 from the left side?"

Try it yourself first. I'll check your answer.`;
    }

    if (
      message.includes("quadratic") ||
      message.includes("quadratic equation")
    ) {
      return `📐 A quadratic equation contains a variable raised to the power of 2.

A common form is:

ax² + bx + c = 0

For example:

x² - 5x + 6 = 0

We can solve many simple quadratic equations by factoring them.

Would you like me to demonstrate the steps?`;
    }

    if (
      message.includes("algebra") ||
      message.includes("expression")
    ) {
      return `🔢 Let's work with algebraic expressions.

Remember that like terms can be combined.

For example:

4x + 2x = 6x

The important idea is that both terms contain the same variable.

Try simplifying:

5x + 3x

What do you get?`;
    }

    if (
      message.includes("thank") ||
      message.includes("thanks")
    ) {
      return `You're welcome! 😊

Keep practicing. Every attempt helps AdaptIQ understand your learning pattern and improve your personalized learning path.`;
    }

    return `🧠 Good question!

Let's break it down step by step instead of jumping directly to the answer.

You're currently learning ${concept}, and your current mastery is ${mastery}%.

First, tell me what part of the problem you already understand.

I'll use that to guide you from there.`;
  };

  const sendMessage = () => {
    if (!input.trim() || isTyping) {
      return;
    }

    const userMessage = input.trim();

    const newUserMessage = {
      id: Date.now(),
      sender: "user",
      text: userMessage,
    };

    setMessages((previous) => [...previous, newUserMessage]);
    setInput("");
    setIsTyping(true);

    setTimeout(() => {
      const response = generateResponse(userMessage);

      const aiMessage = {
        id: Date.now() + 1,
        sender: "ai",
        text: response,
      };

      setMessages((previous) => [...previous, aiMessage]);
      setIsTyping(false);
    }, 900);
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  };

  const askHint = () => {
    setInput("Give me a hint");
  };

  const explainDifferently = () => {
    setInput("Explain this concept differently");
  };

  const startPractice = () => {
    navigate("/quiz", {
      state: {
        concept: concept,
      },
    });
  };

  const clearConversation = () => {
    setMessages([
      {
        id: Date.now(),
        sender: "ai",
        text: `Conversation restarted. 👋 Let's continue learning ${concept} together.`,
      },
    ]);
  };

  return (
    <div className="tutor-page">

      {/* ================= NAVBAR ================= */}

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

          <button className="active-nav">
            AI Tutor
          </button>

        </div>

        <div className="student-info">
          👩‍🎓 Student
        </div>

      </nav>


      {/* ================= MAIN ================= */}

      <main className="tutor-container">

        {/* HEADER */}

        <section className="tutor-header">

          <div>

            <p className="card-label">
              PERSONALIZED AI TUTOR
            </p>

            <h1>
              Learn with AdaptIQ 🧠
            </h1>

            <p>
              Ask questions, get hints, and learn at your own pace.
              AdaptIQ adapts its guidance based on your learning progress.
            </p>

          </div>

          <div className="tutor-concept-info">

            <span>
              CURRENT CONCEPT
            </span>

            <strong>
              🧠 {concept}
            </strong>

            <small>
              Mastery: {mastery}%
            </small>

          </div>

        </section>


        {/* ================= TUTOR LAYOUT ================= */}

        <section className="tutor-layout">


          {/* ================= CHAT ================= */}

          <div className="tutor-chat-card">

            {/* CHAT HEADER */}

            <div className="tutor-chat-header">

              <div className="tutor-profile">

                <div className="tutor-avatar">
                  🧠
                </div>

                <div>

                  <strong>
                    AdaptIQ Tutor
                  </strong>

                  <span>
                    ● Online
                  </span>

                </div>

              </div>

              <button
                className="clear-chat-button"
                onClick={clearConversation}
              >
                ↻ New Chat
              </button>

            </div>


            {/* MESSAGES */}

            <div className="tutor-messages">

              {messages.map((message) => (

                <div
                  key={message.id}
                  className={`tutor-message-row ${
                    message.sender === "user"
                      ? "user-message-row"
                      : "ai-message-row"
                  }`}
                >

                  {message.sender === "ai" && (
                    <div className="message-avatar">
                      🧠
                    </div>
                  )}

                  <div
                    className={`tutor-message ${
                      message.sender === "user"
                        ? "user-message"
                        : "ai-message"
                    }`}
                  >
                    {message.text.split("\n").map((line, index) => (
                      <span key={index}>
                        {line}
                        {index < message.text.split("\n").length - 1 && (
                          <br />
                        )}
                      </span>
                    ))}
                  </div>

                  {message.sender === "user" && (
                    <div className="message-avatar user-avatar">
                      👩‍🎓
                    </div>
                  )}

                </div>

              ))}


              {/* TYPING INDICATOR */}

              {isTyping && (

                <div className="tutor-message-row ai-message-row">

                  <div className="message-avatar">
                    🧠
                  </div>

                  <div className="typing-indicator">

                    <span></span>
                    <span></span>
                    <span></span>

                  </div>

                </div>

              )}

            </div>


            {/* QUICK ACTIONS */}

            <div className="tutor-quick-actions">

              <button onClick={askHint}>
                💡 Give me a hint
              </button>

              <button onClick={explainDifferently}>
                🔄 Explain differently
              </button>

              <button onClick={startPractice}>
                🎯 Practice
              </button>

            </div>


            {/* INPUT */}

            <div className="tutor-input-area">

              <textarea
                value={input}
                onChange={(event) => setInput(event.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Ask me anything about your lesson..."
                rows="2"
              />

              <button
                className="send-message-button"
                onClick={sendMessage}
                disabled={!input.trim() || isTyping}
              >
                ➤
              </button>

            </div>

            <div className="tutor-input-hint">
              Press Enter to send • Shift + Enter for a new line
            </div>

          </div>


          {/* ================= RIGHT PANEL ================= */}

          <aside className="tutor-sidebar">


            {/* LEARNER PROFILE */}

            <div className="tutor-sidebar-card">

              <p className="card-label">
                YOUR LEARNER PROFILE
              </p>

              <h3>
                Current Understanding
              </h3>

              <div className="tutor-mastery">

                <div className="tutor-mastery-top">

                  <span>
                    {concept}
                  </span>

                  <strong>
                    {mastery}%
                  </strong>

                </div>

                <div className="tutor-mastery-track">

                  <div
                    className="tutor-mastery-fill"
                    style={{
                      width: `${mastery}%`,
                    }}
                  ></div>

                </div>

              </div>

              <div className="learner-stat">

                <span>
                  🎯 Learning level
                </span>

                <strong>
                  {mastery < 50
                    ? "Beginner"
                    : mastery < 80
                    ? "Developing"
                    : "Strong"}
                </strong>

              </div>

              <div className="learner-stat">

                <span>
                  📚 Current focus
                </span>

                <strong>
                  {concept}
                </strong>

              </div>

            </div>


            {/* LANGUAGE */}

            <div className="tutor-sidebar-card">

              <p className="card-label">
                LANGUAGE
              </p>

              <h3>
                Choose explanation language
              </h3>

              <div className="language-buttons">

                <button
                  className={
                    language === "English"
                      ? "language-active"
                      : ""
                  }
                  onClick={() => setLanguage("English")}
                >
                  🇬🇧 English
                </button>

                <button
                  className={
                    language === "Hindi"
                      ? "language-active"
                      : ""
                  }
                  onClick={() => setLanguage("Hindi")}
                >
                  🇮🇳 Hindi
                </button>

              </div>

              <p className="language-note">
                Current language: <strong>{language}</strong>
              </p>

            </div>


            {/* TUTOR APPROACH */}

            <div className="tutor-sidebar-card tutor-approach-card">

              <div className="approach-icon">
                💡
              </div>

              <p className="card-label">
                HOW ADAPTIQ TEACHES
              </p>

              <h3>
                We guide, not just answer.
              </h3>

              <ul>

                <li>
                  Gives hints before answers
                </li>

                <li>
                  Adapts explanations to your level
                </li>

                <li>
                  Detects repeated mistakes
                </li>

                <li>
                  Recommends targeted practice
                </li>

              </ul>

            </div>


            {/* BACK */}

            <button
              className="tutor-back-button"
              onClick={() => navigate("/learning-path")}
            >
              ← Back to Learning Path
            </button>

          </aside>

        </section>

      </main>

    </div>
  );
}

export default Tutor;