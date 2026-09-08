import { useState } from "react";
import { useNavigate } from "react-router-dom";

function Login() {

  const navigate = useNavigate();

  const [name, setName] = useState("");
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [remember, setRemember] = useState(false);

  const handleSubmit = (e) => {

    e.preventDefault();

    const user = {
      name,
      username,
      email
    };

    /*
      Demo/local session.

      Do NOT store the actual password
      in localStorage in a real application.
    */

    localStorage.setItem(
      "adaptIQUser",
      JSON.stringify(user)
    );

    if (remember) {
      localStorage.setItem(
        "adaptIQRemember",
        "true"
      );
    } else {
      localStorage.removeItem(
        "adaptIQRemember"
      );
    }

    const profile =
      localStorage.getItem("adaptIQProfile");

    if (profile) {
      navigate("/dashboard");
    } else {
      navigate("/onboarding");
    }

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

          <h2>
            Welcome to AdaptIQ 👋
          </h2>

          <p>
            Let's personalize your learning journey.
          </p>


          <form onSubmit={handleSubmit}>

            <label>Full Name</label>

            <input
              type="text"
              placeholder="Enter your full name"
              value={name}
              onChange={(e) =>
                setName(e.target.value)
              }
              required
            />


            <label>Username</label>

            <input
              type="text"
              placeholder="Choose a username"
              value={username}
              onChange={(e) =>
                setUsername(e.target.value)
              }
              required
            />


            <label>Email</label>

            <input
              type="email"
              placeholder="Enter your email"
              value={email}
              onChange={(e) =>
                setEmail(e.target.value)
              }
              required
            />


            <label>Password</label>

            <input
              type="password"
              placeholder="Create your password"
              value={password}
              onChange={(e) =>
                setPassword(e.target.value)
              }
              required
              minLength={6}
            />


            <div className="remember-row">

              <label>

                <input
                  type="checkbox"
                  checked={remember}
                  onChange={(e) =>
                    setRemember(e.target.checked)
                  }
                />

                Remember me

              </label>

            </div>


            <button type="submit">
              Continue →
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