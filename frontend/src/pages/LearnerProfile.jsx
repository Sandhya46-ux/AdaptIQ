import { useNavigate } from "react-router-dom";

function LearnerProfile() {
  const navigate = useNavigate();

  const user = JSON.parse(
    localStorage.getItem("adaptIQUser") || "{}"
  );

  const profile = JSON.parse(
    localStorage.getItem("adaptIQProfile") || "{}"
  );

  const diagnostic = JSON.parse(
    localStorage.getItem("adaptIQDiagnostic") || "{}"
  );

  return (
    <div className="profile-page">

      <div className="profile-container">

        <div className="profile-header">

          <p className="card-label">
            LEARNER PROFILE
          </p>

          <h1>
            Your Learning Profile 🧠
          </h1>

          <p>
            AdaptIQ created this profile from
            your goals and diagnostic performance.
          </p>

        </div>


        <div className="profile-grid">

          <div className="profile-card">

            <span>👤</span>

            <h3>Student</h3>

            <strong>
              {user.name || "Student"}
            </strong>

            <p>
              {user.email || "No email provided"}
            </p>

          </div>


          <div className="profile-card">

            <span>🎯</span>

            <h3>Learning Goal</h3>

            <strong>
              {profile.career ||
                profile.degree ||
                "General Learning"}
            </strong>

            <p>
              {profile.level || ""}
            </p>

          </div>


          <div className="profile-card">

            <span>📊</span>

            <h3>Diagnostic Score</h3>

            <strong>
              {diagnostic.percentage ?? "--"}%
            </strong>

            <p>
              Initial assessment
            </p>

          </div>


          <div className="profile-card">

            <span>📚</span>

            <h3>Learning Style</h3>

            <strong>
              Adaptive
            </strong>

            <p>
              Based on performance
            </p>

          </div>

        </div>


        <div className="profile-card wide">

          <h2>
            Your Interests
          </h2>

          <div className="profile-tags">

            {(profile.interests || []).map(
              (interest) => (
                <span key={interest}>
                  {interest}
                </span>
              )
            )}

          </div>

        </div>


        <div className="profile-card wide recommendation">

          <div>

            <p className="card-label">
              ADAPTIQ RECOMMENDATION
            </p>

            <h2>
              Your personalized path is ready 🚀
            </h2>

            <p>
              AdaptIQ will use your profile and
              performance to recommend what you
              should learn next.
            </p>

          </div>

          <button
            onClick={() =>
              navigate("/learning-path")
            }
          >
            View Learning Path →
          </button>

        </div>

      </div>

    </div>
  );
}

export default LearnerProfile;