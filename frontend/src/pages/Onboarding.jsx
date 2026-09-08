import { useState } from "react";
import { useNavigate } from "react-router-dom";

const interests = [
  "Mathematics",
  "Physics",
  "Chemistry",
  "Biology",
  "Computer Science",
  "English",
  "Reasoning",
  "General Knowledge",
  "Coding",
  "Data Science"
];

const careerOptions = [
  "JEE",
  "NEET",
  "GATE",
  "UPSC",
  "Engineering",
  "Medical",
  "Coding / IT",
  "Banking",
  "School Academics",
  "Other"
];

function Onboarding() {
  const navigate = useNavigate();

  const [studyType, setStudyType] = useState("");
  const [level, setLevel] = useState("");
  const [degree, setDegree] = useState("");
  const [career, setCareer] = useState("");
  const [gapYear, setGapYear] = useState("");
  const [gapYears, setGapYears] = useState("");
  const [selectedInterests, setSelectedInterests] = useState([]);

  const isSchool = studyType === "school";
  const isHigher = studyType === "higher";

  const toggleInterest = (interest) => {
    setSelectedInterests((previous) =>
      previous.includes(interest)
        ? previous.filter((item) => item !== interest)
        : [...previous, interest]
    );
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    const profile = {
      studyType,
      level,
      degree,
      career,
      gapYear,
      gapYears,
      interests: selectedInterests
    };

    localStorage.setItem(
      "adaptIQProfile",
      JSON.stringify(profile)
    );

    navigate("/dashboard");
  };

  return (
    <div className="onboarding-page">

      <div className="onboarding-card">

        <div className="onboarding-header">
          <div className="brand-small">
            Adapt<span>IQ</span> 🧠
          </div>

          <p className="step-text">
            Let's personalize your learning journey
          </p>

          <h1>
            Tell us about yourself 🎯
          </h1>

          <p>
            AdaptIQ will use this information to create
            a personalized learning experience.
          </p>
        </div>

        <form onSubmit={handleSubmit}>

          {/* STUDY TYPE */}

          <section className="onboarding-section">

            <h2>What are you currently studying?</h2>

            <div className="choice-grid two">

              <button
                type="button"
                className={
                  studyType === "school"
                    ? "choice-card active"
                    : "choice-card"
                }
                onClick={() => {
                  setStudyType("school");
                  setDegree("");
                }}
              >
                <span className="choice-icon">🏫</span>

                <strong>School Student</strong>

                <small>
                  Class 9 - 12
                </small>
              </button>

              <button
                type="button"
                className={
                  studyType === "higher"
                    ? "choice-card active"
                    : "choice-card"
                }
                onClick={() => {
                  setStudyType("higher");
                  setLevel("");
                  setGapYear("");
                }}
              >
                <span className="choice-icon">🎓</span>

                <strong>Higher Studies</strong>

                <small>
                  Bachelor's / Master's / Other
                </small>
              </button>

            </div>

          </section>


          {/* SCHOOL */}

          {isSchool && (
            <section className="onboarding-section">

              <h2>Tell us about your school studies</h2>

              <label>Current Class</label>

              <select
                value={level}
                onChange={(e) => setLevel(e.target.value)}
                required
              >
                <option value="">
                  Select class
                </option>

                <option value="Class 9">
                  Class 9
                </option>

                <option value="Class 10">
                  Class 10
                </option>

                <option value="Class 11">
                  Class 11
                </option>

                <option value="Class 12">
                  Class 12
                </option>
              </select>


              <label>What are you preparing for?</label>

              <div className="choice-grid">

                {careerOptions.map((item) => (
                  <button
                    key={item}
                    type="button"
                    className={
                      career === item
                        ? "mini-choice active"
                        : "mini-choice"
                    }
                    onClick={() => setCareer(item)}
                  >
                    {item}
                  </button>
                ))}

              </div>


              <label>Did you take a gap year?</label>

              <div className="gap-buttons">

                <button
                  type="button"
                  className={
                    gapYear === "No"
                      ? "mini-choice active"
                      : "mini-choice"
                  }
                  onClick={() => {
                    setGapYear("No");
                    setGapYears("");
                  }}
                >
                  No
                </button>

                <button
                  type="button"
                  className={
                    gapYear === "Yes"
                      ? "mini-choice active"
                      : "mini-choice"
                  }
                  onClick={() => setGapYear("Yes")}
                >
                  Yes
                </button>

              </div>


              {gapYear === "Yes" && (
                <>
                  <label>How many gap years?</label>

                  <select
                    value={gapYears}
                    onChange={(e) =>
                      setGapYears(e.target.value)
                    }
                    required
                  >
                    <option value="">
                      Select gap years
                    </option>

                    <option value="1">
                      1 Year
                    </option>

                    <option value="2">
                      2 Years
                    </option>

                    <option value="3+">
                      3+ Years
                    </option>
                  </select>
                </>
              )}

            </section>
          )}


          {/* HIGHER STUDIES */}

          {isHigher && (
            <section className="onboarding-section">

              <h2>Tell us about your higher studies</h2>

              <label>Current Level</label>

              <select
                value={level}
                onChange={(e) => setLevel(e.target.value)}
                required
              >
                <option value="">
                  Select level
                </option>

                <option value="Bachelor's">
                  Bachelor's
                </option>

                <option value="Master's">
                  Master's
                </option>

                <option value="Other">
                  Other
                </option>
              </select>


              <label>Field / Degree</label>

              <input
                type="text"
                placeholder="e.g. Computer Science"
                value={degree}
                onChange={(e) =>
                  setDegree(e.target.value)
                }
                required
              />

            </section>
          )}


          {/* INTERESTS */}

          {studyType && (
            <section className="onboarding-section">

              <h2>Select your interests</h2>

              <p className="section-description">
                Choose the subjects you want AdaptIQ
                to focus on.
              </p>

              <div className="interest-grid">

                {interests.map((interest) => (

                  <button
                    type="button"
                    key={interest}
                    className={
                      selectedInterests.includes(interest)
                        ? "interest active"
                        : "interest"
                    }
                    onClick={() =>
                      toggleInterest(interest)
                    }
                  >
                    {selectedInterests.includes(interest)
                      ? "✓ "
                      : "+ "}

                    {interest}
                  </button>

                ))}

              </div>

            </section>
          )}


          {/* SUBMIT */}

          {studyType && selectedInterests.length > 0 && (
            <button
              type="submit"
              className="onboarding-submit"
            >
              Create My Learning Profile →
            </button>
          )}

        </form>

      </div>

    </div>
  );
}

export default Onboarding;