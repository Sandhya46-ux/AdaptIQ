import { useState } from "react";
import { useNavigate } from "react-router-dom";

function Login() {
  const navigate = useNavigate();

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();

    // Temporary frontend login.
    // Later this will connect to the backend.
    navigate("/dashboard");
  };

  return (
    <div className="login-page">

      <div className="login-card">

        <div className="brand">
          <h1>
            Adapt<span>IQ</span> 🧠
          </h1>

          <p>
            Learn differently. Learn intelligently.
          </p>
        </div>

        <div className="login-content">

          <h2>Welcome back! 👋</h2>

          <p>
            Let's personalize your learning journey.
          </p>

          <form onSubmit={handleSubmit}>

            <label>Student Name</label>

            <input
              type="text"
              placeholder="Enter your name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
            />

            <label>Email</label>

            <input
              type="email"
              placeholder="Enter your email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />

            <button type="submit">
              Start Learning →
            </button>

          </form>

        </div>

        <div className="login-footer">
          <p>
            AI-powered • Personalized • Student-centric
          </p>
        </div>

      </div>

    </div>
  );
}

export default Login;